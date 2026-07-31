#!/usr/bin/env python3
"""
Horse Star RDV/STUD Stub Server v21
Handles the full login flow:
  RDV: SYN handshake → AuthRequest → AuthResponse → GetPeerRequest → GetPeerResponse
  STUD: SYN handshake → ConfirmReconnectionRequest → ConfirmReconnectionResponse
        → LoginRequest → LoginResponse
  
  Key insight: the ConfirmReconnectionResponse (0x06 0x01) sets PeerContainer.isChecked
  on the client, which unblocks ActionDirectConnectPOMPeer → POMPeerEvent.CONNECT
  → NotifyStudServerConnection → SendLoginRequest.
"""

import select
import socket
import struct
import sys
import uuid
from datetime import datetime

# ── Network config ────────────────────────────────────────────────
HOST      = "127.0.0.1"
RDV_PORT  = 15250   # Client.txt <RdvPort>
STUD_PORT = 1025    # Where we told the client STUD lives (via GetPeerResponse)
LOG_FILE  = "rdv_stub_log.txt"

# ── OUDP block type constants (high nibble of the type byte) ──────
TYPE_ACK = 0x10   # Acknowledge
TYPE_CHK = 0x20   # Check/keepalive
TYPE_DAT = 0x30   # Data
TYPE_ERR = 0x40   # Error
TYPE_FDB = 0x50   # Feedback
TYPE_FIN = 0x60   # Finish/close
TYPE_SYN = 0x70   # Synchronise (handshake)
TYPE_MASK = 0xF0  # Mask to extract the high nibble

OPT_REL    = 0x01  # Low bit: this block carries a 4-byte big-endian block ID
OPT_SINGLE = 0x02  # ACK option: single-ID ack
OPT_RANGE  = 0x04  # ACK option: range ack
OPT_MPD    = 0x02  # DAT option: multipart data

# ── POM message opcodes (confirmed from DLL GetIdentifier methods) ─
# These are the first byte of every DAT payload.
OPCODE_AUTH_REQUEST            = 0x01  # Client → server: "here is my name, authenticate me"
OPCODE_GET_PEER_REQUEST        = 0x02  # Client → RDV: "where is peer X?"
OPCODE_CLOSE_REQUEST           = 0x03
OPCODE_CLOSE_RESPONSE          = 0x04
OPCODE_CONFIRM_RECONNECT_REQ   = 0x05
OPCODE_CONFIRM_RECONNECT_RES   = 0x06
OPCODE_AUTH_RESPONSE           = 0x81  # Server → client: "you are authenticated"
OPCODE_GET_PEER_RESPONSE       = 0x82  # Server → client: "that peer is at this address"
OPCODE_LOGIN_RESPONSE          = 0x06  # Server → client on STUD: login result
                                       # (LoginResponse.Result.Validated = 6 = 0x06)

# The STUD identification message the client sends right after the STUD SYN
# handshake completes. Wire format:
#   0x02 (same opcode as GetPeerRequest but on STUD, no GUID, no response expected)
#   0x00 (isReconnecting flag = false)
#   1-byte length + name bytes    (e.g. "rim")
#   1-byte length + rdvId bytes   (e.g. "rdv01")
OPCODE_STUD_IDENTIFY = 0x02


# ── Logging ───────────────────────────────────────────────────────
def log_line(f, line: str):
    print(line)
    f.write(line + "\n")
    f.flush()


# ── Hex dump helper ───────────────────────────────────────────────
def hex_dump(data: bytes, indent: str = "  ") -> str:
    if not data:
        return f"{indent}(empty)"
    lines = []
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk).ljust(47)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{indent}{offset:04x}: {hex_part}  {ascii_part}")
    return "\n".join(lines)


# ── OUDP wire format builders ─────────────────────────────────────
def pack_syn(block_id: int) -> bytes:
    """Build a reliable SYN block: 0x71 + 4-byte big-endian block ID."""
    return bytes([TYPE_SYN | OPT_REL]) + struct.pack(">I", block_id)


def pack_ack_single(acked_id: int) -> bytes:
    """Build a single-ID ACK block: 0x12 + 4-byte big-endian acked ID."""
    return bytes([TYPE_ACK | OPT_SINGLE]) + struct.pack(">I", acked_id)


def pack_dat_single(block_id: int, message_id: int, payload: bytes) -> bytes:
    """Build a reliable DAT block wrapping a message payload.

    Wire format:
        0x31              type byte (DAT | reliable, not multipart)
        4 bytes           block ID (big-endian)
        4 bytes           message ID (big-endian)
        2 bytes           payload length (big-endian)
        N bytes           payload
    """
    header = (bytes([TYPE_DAT | OPT_REL])
              + struct.pack(">I", block_id)
              + struct.pack(">I", message_id)
              + struct.pack(">H", len(payload)))
    return header + payload


# ── DAT payload parser ────────────────────────────────────────────
def decode_dat_payload(data: bytes, pos: int, type_byte: int, log_f, indent="    "):
    """Parse the payload section of a DAT block.

    Returns (new_pos, info_dict) or (None, None) on parse error.
    info_dict has keys: message_id, payload
    """
    multipart = bool(type_byte & OPT_MPD)

    # message_id (4 bytes)
    if pos + 4 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: not enough bytes for message_id")
        return None, None
    message_id = struct.unpack(">I", data[pos:pos+4])[0]
    log_line(log_f, f"{indent}[DAT] messageId @ offset {pos}: {message_id} "
                     f"(bytes: {data[pos:pos+4].hex()})")
    pos += 4

    # data_length (2 bytes)
    if pos + 2 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: not enough bytes for dataLength")
        return None, None
    data_length = struct.unpack(">H", data[pos:pos+2])[0]
    log_line(log_f, f"{indent}[DAT] dataLength @ offset {pos}: {data_length} "
                     f"(bytes: {data[pos:pos+2].hex()})")
    pos += 2

    # payload
    if pos + data_length > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: declared {data_length} bytes "
                         f"but only {len(data)-pos} remain")
        return None, None
    payload = data[pos:pos+data_length]
    log_line(log_f, f"{indent}[DAT] payload @ offset {pos}, {data_length} bytes:")
    log_line(log_f, hex_dump(payload, indent=indent + "  "))
    pos += data_length

    return pos, {"message_id": message_id, "payload": payload}


# ══════════════════════════════════════════════════════════════════
#  MESSAGE DECODERS
# ══════════════════════════════════════════════════════════════════

def try_decode_auth_request(payload: bytes, log_f, indent="      "):
    """Decode a full AuthRequest (opcode 0x01, ≥18 bytes, has a 16-byte GUID).

    CONFIRMED from DLL IL disassembly:
    Wire format (inside DAT payload):
        1 byte   : 0x01 (opcode)
        16 bytes : request GUID (random per attempt)
        1 byte   : name length N
        N bytes  : name ASCII (e.g. "rim")
        7 bytes  : endpoint info (port + addr-type + 4-byte IPv4)

    Returns None if the payload doesn't match this format.
    """
    if len(payload) < 18:
        return None
    if payload[0] != OPCODE_AUTH_REQUEST:
        return None

    opcode     = payload[0]
    guid_bytes = payload[1:17]
    try:
        guid_obj = uuid.UUID(bytes_le=guid_bytes)
    except Exception:
        guid_obj = None

    if len(payload) < 18:
        return None
    name_len   = payload[17]
    name_end   = 18 + name_len
    if name_end > len(payload):
        return None
    name_bytes = payload[18:name_end]
    remainder  = payload[name_end:]

    try:
        name_str = name_bytes.decode("ascii")
    except UnicodeDecodeError:
        name_str = name_bytes.hex()

    log_line(log_f, f"{indent}[auth] opcode byte: 0x{opcode:02x}")
    log_line(log_f, f"{indent}[auth] requestId (raw bytes): {guid_bytes.hex()}"
                     + (f"  (as GUID: {guid_obj})" if guid_obj else ""))
    log_line(log_f, f"{indent}[auth] name length: {name_len}")
    log_line(log_f, f"{indent}[auth] name bytes: {name_bytes.hex()}  (ASCII: {name_str!r})")
    log_line(log_f, f"{indent}[auth] remainder ({len(remainder)} bytes): {remainder.hex()}")

    return {"guid_bytes": guid_bytes, "name": name_str}


def try_decode_stud_identify(payload: bytes, log_f, indent="      "):
    """Decode the short STUD identification message (opcode 0x02, no GUID).

    This arrives on the STUD port right after the SYN handshake completes.
    It is NOT a GetPeerRequest (which also uses 0x02 but has a 16-byte GUID).
    The STUD version is shorter: opcode + isReconnecting flag + name + rdvId.

    CONFIRMED by packet capture:
        02 00 03 72 69 6d 05 72 64 76 30 31
        ^  ^  ^  ^^^^^^^^  ^  ^^^^^^^^^^^^^
        |  |  |  "rim"     |  "rdv01"
        |  |  name_len     rdvId_len
        |  isReconnecting=0
        opcode=0x02

    Wire format:
        1 byte   : 0x02
        1 byte   : isReconnecting (0 = fresh connect)
        1 byte   : name length
        N bytes  : name (e.g. "rim")
        1 byte   : rdvId length
        N bytes  : rdvId (e.g. "rdv01")

    We reply with opcode 0x82 + same content to acknowledge.
    """
    if len(payload) < 4:
        return None
    if payload[0] != OPCODE_STUD_IDENTIFY:
        return None
    # Distinguish from full GetPeerRequest (also 0x02 but ≥18 bytes with GUID)
    # A real GetPeerRequest always has 16 GUID bytes after the opcode.
    # The STUD identify message is short (12 bytes in our capture).
    if len(payload) >= 18:
        return None  # This is a GetPeerRequest, not a STUD identify

    is_reconnecting = payload[1]
    pos = 2

    fields = {}
    for field_name in ("name", "rdvId"):
        if pos >= len(payload):
            break
        field_len = payload[pos]
        pos += 1
        field_bytes = payload[pos:pos + field_len]
        pos += field_len
        try:
            fields[field_name] = field_bytes.decode("utf-8")
        except Exception:
            fields[field_name] = field_bytes.hex()

    log_line(log_f, f"{indent}[stud_id] opcode=0x02 (STUD identification)")
    log_line(log_f, f"{indent}[stud_id] isReconnecting={is_reconnecting}")
    for k, v in fields.items():
        log_line(log_f, f"{indent}[stud_id] {k}: {v!r}")

    return {"is_reconnecting": is_reconnecting, "fields": fields}


def try_decode_get_peer_request(payload: bytes, log_f, indent="      "):
    """Decode a GetPeerRequest (opcode 0x02, ≥18 bytes, has 16-byte GUID).

    CONFIRMED from DLL IL disassembly:
    Wire format:
        1 byte   : 0x02 (opcode)
        16 bytes : request GUID
        1 byte   : length of peerToAsk
        N bytes  : peerToAsk (UTF-8, e.g. "127.0.0.1")
        1 byte   : length of rdvLocation
        N bytes  : rdvLocation (UTF-8, e.g. "rdv01")
    """
    if len(payload) < 18:
        return None
    if payload[0] != OPCODE_GET_PEER_REQUEST:
        return None

    guid_bytes = payload[1:17]
    try:
        guid_obj = uuid.UUID(bytes_le=guid_bytes)
    except Exception:
        guid_obj = None

    pos = 17
    fields = {}
    for field_name in ("peerToAsk", "rdvLocation"):
        if pos >= len(payload):
            break
        field_len = payload[pos]
        pos += 1
        field_bytes = payload[pos:pos + field_len]
        pos += field_len
        try:
            fields[field_name] = field_bytes.decode("utf-8")
        except Exception:
            fields[field_name] = field_bytes.hex()

    log_line(log_f, f"{indent}[getpeer] opcode=0x02 (GetPeerRequest)")
    log_line(log_f, f"{indent}[getpeer] requestId: {guid_bytes.hex()}"
                     + (f"  ({guid_obj})" if guid_obj else ""))
    for k, v in fields.items():
        log_line(log_f, f"{indent}[getpeer] {k}: {v!r}")

    return {"guid_bytes": guid_bytes, "fields": fields}


def try_decode_login_request(payload: bytes, log_f, indent="      "):
    """Decode a LoginRequest sent by the client to the STUD server.

    CONFIRMED from DLL IL disassembly of LoginRequest.EncodeRequest:
    Wire format (no opcode prefix at this layer — framed by the Requester):
        16 bytes : requestId GUID
        1 byte   : length of login string
        N bytes  : login (UTF-8)
        1 byte   : length of password string
        N bytes  : password (UTF-8)
        1 byte   : length of sessionId (e.g. "rim")
        N bytes  : sessionId (UTF-8)
        1 byte   : length of rdvId (e.g. "rdv01")
        N bytes  : rdvId (UTF-8)
    """
    if len(payload) < 17:
        return None
    # LoginRequest has no opcode byte — starts directly with the GUID.
    # Guard: if the first byte is a known opcode, this isn't a LoginRequest.
    if payload[0] in (OPCODE_AUTH_REQUEST, OPCODE_GET_PEER_REQUEST,
                      OPCODE_CLOSE_REQUEST, OPCODE_CLOSE_RESPONSE,
                      OPCODE_CONFIRM_RECONNECT_REQ, OPCODE_STUD_IDENTIFY):
        return None

    guid_bytes = payload[0:16]
    try:
        guid_obj = uuid.UUID(bytes_le=guid_bytes)
    except Exception:
        guid_obj = None

    pos = 16
    fields = {}
    for field_name in ("login", "password", "sessionId", "rdvId"):
        if pos >= len(payload):
            log_line(log_f, f"{indent}[login] ran out of bytes before '{field_name}'")
            break
        field_len = payload[pos]
        pos += 1
        field_bytes = payload[pos:pos + field_len]
        pos += field_len
        try:
            fields[field_name] = field_bytes.decode("utf-8")
        except Exception:
            fields[field_name] = field_bytes.hex()

    remainder = payload[pos:]

    log_line(log_f, f"{indent}[login] requestId: {guid_bytes.hex()}"
                     + (f"  ({guid_obj})" if guid_obj else ""))
    for k, v in fields.items():
        log_line(log_f, f"{indent}[login] {k}: {v!r}")
    if remainder:
        log_line(log_f, f"{indent}[login] remainder ({len(remainder)} bytes): {remainder.hex()}")

    return {"guid_bytes": guid_bytes, "fields": fields}


# ══════════════════════════════════════════════════════════════════
#  RESPONSE BUILDERS
# ══════════════════════════════════════════════════════════════════

def build_auth_response(request_guid_bytes: bytes) -> bytes:
    """Build an AuthResponse payload.

    CONFIRMED from DLL: RendezVous.HandleMessage checks ReadByte() == 129 (0x81)
    before treating the payload as an AuthResponse.

    Wire format:
        1 byte   : 0x81 (response opcode)
        16 bytes : requestId (copied from request)
        1 byte   : 0x01 (validated = true)
        1 byte   : 0x05 (length of "rdv01")
        5 bytes  : "rdv01"
    """
    return bytes([OPCODE_AUTH_RESPONSE]) + request_guid_bytes + bytes([0x01, 0x05]) + b"rdv01"


def build_stud_identify_response(public_ip: str = "127.0.0.1",
                                  rdv_location: str = "rdv01") -> bytes:
    """Build a type-2 identification response sent back to the STUD peer.

    CONFIRMED via ActionHandlePeerInternalMessage.DoAction C# decompile:

    In case 2, after setting isChecked, the handler calls:
        string text2 = InternalMsgs.ReceiveId(this.evnt.Message);
        POMPeer_v1 pompeer_v2 = (POMPeer_v1)this.rdv.pomClient.TouchPeer(text2);
        if (pompeer_v2 == null) { this.evnt.Peer.Close(); return; }

    InternalMsgs.ReceiveId reads two length-prefixed strings and joins them
    as "first@second". TouchPeer looks up the POMPeer by that name.

    The STUD peer was registered as "127.0.0.1@rdv01" (StudServerName from
    Client.txt = "127.0.0.1@rdv01"). So we must encode "127.0.0.1" and "rdv01"
    so ReceiveId produces "127.0.0.1@rdv01" and TouchPeer finds the peer.

    Previous bug: we were sending "127.0.0.1" + "1025" → joined as
    "127.0.0.1@1025" → TouchPeer returned null → peer closed → no CONNECT event.

    Wire format:
        1 byte  : 0x02 (type identifier)
        1 byte  : 0x00 (isReconnecting = false, read by DoAction before ReceiveId)
        1 byte  : length of first string (host)
        N bytes : host (e.g. "127.0.0.1")
        1 byte  : length of second string (rdv location)
        N bytes : rdv location (e.g. "rdv01")
    """
    host_bytes = public_ip.encode("utf-8")
    rdv_bytes  = rdv_location.encode("utf-8")
    return (bytes([0x02, 0x00]) +
            bytes([len(host_bytes)]) + host_bytes +
            bytes([len(rdv_bytes)]) + rdv_bytes)


def build_get_peer_response(request_guid_bytes: bytes,
                             public_ip: str = "127.0.0.1",
                             public_port: int = STUD_PORT) -> bytes:
    """Build a GetPeerResponse payload.

    CONFIRMED from DLL: GetPeerRes.DecodeResponse reads:
        ReadEndPoint()  → publicAddress
            ReadUInt16()        : port (little-endian)
            ReadTinyByteArray() : IP (1-byte length + N bytes)
        ReadByte()      : 0x00 = no private address

    Wire format:
        1 byte   : 0x82 (GetPeerResponse opcode)
        16 bytes : requestId (copied from request)
        2 bytes  : port (little-endian uint16)
        1 byte   : IP byte count (4 for IPv4)
        4 bytes  : IP address octets
        1 byte   : 0x00 (no private address)
    """
    ip_bytes   = bytes(int(x) for x in public_ip.split("."))
    port_bytes = struct.pack("<H", public_port)
    endpoint   = port_bytes + bytes([len(ip_bytes)]) + ip_bytes
    return bytes([OPCODE_GET_PEER_RESPONSE]) + request_guid_bytes + endpoint + bytes([0x00])


def build_login_response(request_guid_bytes: bytes) -> bytes:
    """Build a LoginResponse payload.

    CONFIRMED from DLL: LoginResponse.DecodeResponse reads:
        m_identified = reader.ReadByte()
        if m_identified == 6:  ← Validated
            m_playerProfile = ReadLargeString()  ← ReadUInt32() length + bytes

    LoginResponse.Result enum (confirmed from metadata):
        Unknown        = 0
        NotFound       = 1
        BadPassword    = 2
        NotActivated   = 3
        Suspended      = 4
        WaitingForCluf = 5
        Validated      = 6  ← this flips LoginStatus to OK and unlocks the UI

    Wire format we send:
        16 bytes : requestId (copied from LoginRequest)
        1 byte   : 0x06 (Validated)
        4 bytes  : player profile length (uint32 little-endian) = 2
        2 bytes  : "{}" (minimal placeholder JSON)

    Note: The game will almost certainly request real player data via
    GetPlayerDataRequest immediately after. The "{}" placeholder keeps
    the client alive long enough to see what comes next.
    """
    player_profile = b"{}"
    profile_len    = struct.pack("<I", len(player_profile))
    return request_guid_bytes + bytes([0x06]) + profile_len + player_profile


# ══════════════════════════════════════════════════════════════════
#  MAIN PACKET DISPATCH
# ══════════════════════════════════════════════════════════════════

def parse_and_respond(data: bytes, state_key, sock, stud_sock, log_f, state):
    """Parse one incoming UDP datagram and return the bytes to send back.

    state_key = (id(sock), (ip, port)) — unique per physical connection
    state["phase"][state_key] tracks where each connection is in the flow:
        None             → brand new, haven't seen a SYN yet
        "rdv_connecting" → saw RDV SYN, waiting for auth
        "rdv_established"→ RDV auth complete, keepalive + GetPeer phase
        "stud_connecting"→ STUD SYN received, waiting for identification
        "stud_identified"→ STUD identification acknowledged, waiting for login
        "stud_established"→ login complete
    """
    pos      = 0
    response = b""

    while pos < len(data):
        type_byte  = data[pos]
        block_start = pos
        pos        += 1
        reliable   = bool(type_byte & OPT_REL)
        base_type  = type_byte & TYPE_MASK

        block_id = None
        if reliable:
            if pos + 4 > len(data):
                log_line(log_f, f"  [parse] truncated reliable header at offset {pos-1}")
                break
            block_id = struct.unpack(">I", data[pos:pos+4])[0]
            pos += 4

        # ── ACK ──────────────────────────────────────────────────
        if base_type == TYPE_ACK:
            if pos + 4 > len(data):
                log_line(log_f, f"  [parse] truncated ACK at offset {pos}")
                break
            offset = struct.unpack(">I", data[pos:pos+4])[0]
            pos += 4
            is_range = bool(type_byte & OPT_RANGE)
            limit = offset
            if is_range:
                if pos + 4 > len(data):
                    break
                limit = struct.unpack(">I", data[pos:pos+4])[0]
                pos += 4
            log_line(log_f, f"  -> ACK reliable={reliable} offset={offset} limit={limit}")

        # ── SYN ──────────────────────────────────────────────────
        elif base_type == TYPE_SYN:
            log_line(log_f, f"  -> SYN reliable={reliable} id={block_id}")
            if reliable:
                log_line(log_f, f"  [handshake] acking SYN id={block_id}")
                response += pack_ack_single(block_id)

                phase = state["phase"].get(state_key)

                if phase is None:
                    # Brand new connection — determine phase from which socket
                    if sock == stud_sock:
                        state["phase"][state_key] = "stud_connecting"
                    else:
                        state["phase"][state_key] = "rdv_connecting"
                    new_phase = state["phase"][state_key]
                    log_line(log_f, f"  [handshake] new connection → phase={new_phase!r}, "
                                     f"sending our SYN id={state['our_block_id']}")
                    response += pack_syn(state["our_block_id"])
                    state["our_block_id"] += 1

                elif phase in ("rdv_connecting", "stud_connecting"):
                    log_line(log_f, f"  [handshake] retransmission in {phase!r}, re-acking only")

                elif phase == "rdv_established" and block_id == 0:
                    # A fresh SYN id=0 after RDV is up = STUD peer connecting on RDV port
                    # (fallback path if STUD traffic comes to RDV port for some reason)
                    state["phase"][state_key] = "stud_connecting"
                    log_line(log_f, f"  [handshake] new SYN id=0 after RDV established "
                                     f"→ STUD connecting, sending SYN id={state['our_block_id']}")
                    response += pack_syn(state["our_block_id"])
                    state["our_block_id"] += 1

                else:
                    log_line(log_f, f"  [handshake] SYN in phase={phase!r}, re-acking only")

        # ── CHK (keepalive) ───────────────────────────────────────
        elif base_type == TYPE_CHK:
            log_line(log_f, f"  -> CHK reliable={reliable} id={block_id}")
            if reliable and block_id is not None:
                log_line(log_f, f"  [keepalive] acking CHK id={block_id}")
                response += pack_ack_single(block_id)

        # ── FIN ───────────────────────────────────────────────────
        elif base_type == TYPE_FIN:
            log_line(log_f, f"  -> FIN reliable={reliable} id={block_id}")

        # ── ERR ───────────────────────────────────────────────────
        elif base_type == TYPE_ERR:
            log_line(log_f, f"  -> ERR reliable={reliable} id={block_id} "
                             f"(consuming rest of datagram)")
            pos = len(data)

        # ── FDB (feedback) ────────────────────────────────────────
        elif base_type == TYPE_FDB:
            # FDB has a fixed 4-byte payload confirmed from packet analysis.
            # Must consume exactly 4 bytes so subsequent blocks in the same
            # datagram (e.g. ACK + DAT bundled after FDB) are still parsed.
            if pos + 4 > len(data):
                log_line(log_f, f"  -> FDB reliable={reliable} id={block_id} (truncated)")
                break
            fdb_payload = data[pos:pos + 4]
            pos += 4
            log_line(log_f, f"  -> FDB reliable={reliable} id={block_id} "
                             f"payload={fdb_payload.hex()}")

        # ── DAT (data — the interesting one) ─────────────────────
        elif base_type == TYPE_DAT:
            log_line(log_f, f"  -> DAT reliable={reliable} id={block_id} "
                             f"(type_byte=0x{type_byte:02x}, "
                             f"multipart={bool(type_byte & OPT_MPD)})")
            new_pos, info = decode_dat_payload(data, pos, type_byte, log_f)
            if new_pos is None:
                break
            pos = new_pos

            # Always ACK reliable DATs
            if reliable and block_id is not None:
                log_line(log_f, f"  [handshake] acking DAT id={block_id}")
                response += pack_ack_single(block_id)

            phase   = state["phase"].get(state_key)
            payload = info["payload"]

            # ── RDV AUTH ─────────────────────────────────────────
            auth_info = try_decode_auth_request(payload, log_f)
            if auth_info is not None:
                log_line(log_f, f"  [auth] sending AuthResponse for "
                                 f"requestId={auth_info['guid_bytes'].hex()}")
                resp_payload = build_auth_response(auth_info["guid_bytes"])
                log_line(log_f, hex_dump(resp_payload, indent="    "))
                dat_block = pack_dat_single(
                    state["our_block_id"], info["message_id"], resp_payload)
                state["our_block_id"] += 1
                response += dat_block
                # Advance phase
                if phase == "stud_connecting":
                    state["phase"][state_key] = "stud_authed"
                    log_line(log_f, f"  [auth] phase → stud_authed")
                else:
                    state["phase"][state_key] = "rdv_established"
                    log_line(log_f, f"  [auth] phase → rdv_established")
                continue

            # ── RDV: GET PEER REQUEST ─────────────────────────────
            if phase == "rdv_established":
                get_peer_info = try_decode_get_peer_request(payload, log_f)
                if get_peer_info is not None:
                    log_line(log_f, f"  [getpeer] sending GetPeerResponse "
                                     f"(STUD at {HOST}:{STUD_PORT})")
                    resp_payload = build_get_peer_response(
                        get_peer_info["guid_bytes"],
                        public_ip=HOST,
                        public_port=STUD_PORT)
                    log_line(log_f, hex_dump(resp_payload, indent="    "))
                    dat_block = pack_dat_single(
                        state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    log_line(log_f, f"  [getpeer] done")
                else:
                    log_line(log_f, f"  [dat] unrecognized RDV payload "
                                     f"({len(payload)} bytes):")
                    log_line(log_f, hex_dump(payload, indent="    "))

            # ── STUD: IDENTIFICATION (opcode 0x02, short, no GUID) ─
            elif phase == "stud_connecting":
                stud_id = try_decode_stud_identify(payload, log_f)
                if stud_id is not None:
                    log_line(log_f, f"  [stud_id] sending identification acknowledgement")
                    resp_payload = build_stud_identify_response(
                        public_ip=HOST, rdv_location="rdv01")
                    log_line(log_f, hex_dump(resp_payload, indent="    "))
                    dat_block = pack_dat_single(
                        state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    state["phase"][state_key] = "stud_identified"
                    log_line(log_f, f"  [stud_id] phase → stud_identified "
                                     f"(waiting for LoginRequest)")
                else:
                    log_line(log_f, f"  [dat] unrecognized STUD payload "
                                     f"({len(payload)} bytes):")
                    log_line(log_f, hex_dump(payload, indent="    "))

            # ── STUD: LOGIN REQUEST ───────────────────────────────
            elif phase in ("stud_identified", "stud_authed", "stud_established"):
                login_info = try_decode_login_request(payload, log_f)
                if login_info is not None:
                    log_line(log_f, f"  [login] sending LoginResponse (Validated) for "
                                     f"requestId={login_info['guid_bytes'].hex()}")
                    resp_payload = build_login_response(login_info["guid_bytes"])
                    log_line(log_f, hex_dump(resp_payload, indent="    "))
                    dat_block = pack_dat_single(
                        state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    state["phase"][state_key] = "stud_established"
                    log_line(log_f, f"  [login] phase → stud_established "
                                     f"(LoginStatus should flip to OK!)")
                else:
                    log_line(log_f, f"  [dat] unrecognized login-phase payload "
                                     f"({len(payload)} bytes):")
                    log_line(log_f, hex_dump(payload, indent="    "))

            else:
                log_line(log_f, f"  [dat] unrecognized payload in phase={phase!r} "
                                 f"({len(payload)} bytes):")
                log_line(log_f, hex_dump(payload, indent="    "))

        # ── Unknown block type ────────────────────────────────────
        else:
            log_line(log_f, f"  [parse] unknown type byte 0x{type_byte:02x} "
                             f"at offset {block_start}, stopping")
            break

    return response


# ══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Horse Star RDV/STUD Stub Server v21")
    print("=" * 60)
    print(f"Binding RDV  socket to {HOST}:{RDV_PORT}")
    print(f"Binding STUD socket to {HOST}:{STUD_PORT}")
    print(f"Logging to {LOG_FILE}")
    print("Start the asset server, then launch Horse Star and log in.")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    rdv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        rdv_sock.bind((HOST, RDV_PORT))
    except OSError as e:
        print(f"FAILED to bind RDV socket {HOST}:{RDV_PORT} → {e}")
        sys.exit(1)

    stud_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        stud_sock.bind((HOST, STUD_PORT))
    except OSError as e:
        print(f"FAILED to bind STUD socket {HOST}:{STUD_PORT} → {e}")
        rdv_sock.close()
        sys.exit(1)

    sock_labels = {
        rdv_sock:  f"RDV:{RDV_PORT}",
        stud_sock: f"STUD:{STUD_PORT}",
    }

    log_f = open(LOG_FILE, "a", encoding="utf-8")
    session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_f.write("\n" + "=" * 70 + "\n")
    log_f.write(f"SESSION START: {session_start}\n")
    log_f.write("=" * 70 + "\n")
    log_f.flush()

    # Shared state across all connections.
    # phase dict is keyed by (id(sock), (ip, port)) so RDV and STUD connections
    # from the same client address are always treated independently.
    state = {
        "our_block_id": 0,
        "phase": {},
    }

    packet_count = 0

    try:
        while True:
            readable, _, _ = select.select([rdv_sock, stud_sock], [], [], 5.0)
            for sock in readable:
                data, addr = sock.recvfrom(65535)
                packet_count += 1
                now   = datetime.now().strftime("%H:%M:%S.%f")
                label = sock_labels[sock]
                state_key = (id(sock), addr)

                log_line(log_f, f"[{now}] PACKET #{packet_count} [{label}] "
                                 f"from {addr[0]}:{addr[1]} ({len(data)} bytes):")
                log_line(log_f, hex_dump(data))

                try:
                    response = parse_and_respond(
                        data, state_key, sock, stud_sock, log_f, state)
                    if response:
                        sock.sendto(response, addr)
                        log_line(log_f, f"  [send] → {addr} ({len(response)} bytes):")
                        log_line(log_f, hex_dump(response))
                    else:
                        log_line(log_f, "  [send] (nothing to send)")
                except Exception as e:
                    import traceback
                    err = traceback.format_exc()
                    log_line(log_f, f"  [CRASH] Exception: {e}")
                    log_line(log_f, err)
                    print(f"[CRASH] {e}")

                log_line(log_f, "")

    except KeyboardInterrupt:
        print(f"\nStopped. Total packets received: {packet_count}")
        log_f.write(f"\nSESSION END. Total packets: {packet_count}\n")
        log_f.close()
        rdv_sock.close()
        stud_sock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()

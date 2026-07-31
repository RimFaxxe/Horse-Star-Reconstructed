"""
Horse Star RDV Stub Server v6
Handles transport handshake, AuthResponse and LoginResponse to unblock unity3d asset loading.
"""
import socket
import struct
import sys
import uuid
from datetime import datetime

HOST = "127.0.0.1"
RDV_PORT = 15250
LOG_FILE = "rdv_stub_log.txt"

TYPE_ACK = 0x10
TYPE_CHK = 0x20
TYPE_DAT = 0x30
TYPE_ERR = 0x40
TYPE_FDB = 0x50
TYPE_FIN = 0x60
TYPE_SYN = 0x70

OPT_REL = 0x01
OPT_SINGLE = 0x02
OPT_RANGE = 0x04
OPT_MPD = 0x02  
TYPE_MASK = 0xF0

def log_line(f, line: str):
    print(line)
    f.write(line + "\n")
    f.flush()

def hex_dump(data: bytes, indent: str = "  ") -> str:
    lines = []
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk).ljust(47)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{indent}{offset:04x}: {hex_part}  {ascii_part}")
    if not data:
        lines.append(f"{indent}(empty payload)")
    return "\n".join(lines)

def pack_syn(block_id: int) -> bytes:
    return struct.pack(">BI", TYPE_SYN | OPT_REL, block_id)

def pack_ack_single(acked_id: int) -> bytes:
    return struct.pack(">BI", TYPE_ACK | OPT_SINGLE, acked_id)

def pack_dat_single(block_id: int, message_id: int, payload: bytes) -> bytes:
    type_byte = TYPE_DAT | OPT_REL
    header = struct.pack(">BI", type_byte, block_id)
    body = struct.pack(">IH", message_id, len(payload)) + payload
    return header + body

def decode_dat_payload(data: bytes, pos: int, type_byte: int, log_f, indent="    "):
    is_multipart = bool(type_byte & OPT_MPD)
    start = pos

    if pos + 4 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated message_id at {pos}")
        return None, None
    message_id = struct.unpack(">I", data[pos:pos+4])[0]
    log_line(log_f, f"{indent}[DAT] msg id @ {pos}: {message_id} ({data[pos:pos+4].hex()})")
    pos += 4

    message_length = None
    block_offset = None
    if is_multipart:
        if pos + 4 > len(data):
            log_line(log_f, f"{indent}[DAT] truncated message_len at {pos}")
            return None, None
        message_length = struct.unpack(">I", data[pos:pos+4])[0]
        pos += 4

        if pos + 4 > len(data):
            log_line(log_f, f"{indent}[DAT] truncated block_offset at {pos}")
            return None, None
        block_offset = struct.unpack(">I", data[pos:pos+4])[0]
        pos += 4

    if pos + 2 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated data_len at {pos}")
        return None, None
    data_len = struct.unpack(">H", data[pos:pos+2])[0]
    pos += 2

    if pos + data_len > len(data):
        log_line(log_f, f"{indent}[DAT] declared length {data_len} exceeds remaining bytes - clipping")
        data_len = len(data) - pos

    payload = data[pos:pos+data_len]
    log_line(log_f, f"{indent}[DAT] payload @ {pos} ({len(payload)} bytes):")
    log_line(log_f, hex_dump(payload, indent=indent + "  "))
    pos += data_len

    info = {
        "is_multipart": is_multipart,
        "message_id": message_id,
        "message_length": message_length,
        "block_offset": block_offset,
        "payload": payload,
        "consumed": pos - start,
    }
    return pos, info
def try_decode_auth_request(payload: bytes, log_f, indent="      "):
    if len(payload) < 18:
        return None

    opcode = payload[0]
    guid_bytes = payload[1:17]
    try:
        guid_obj = uuid.UUID(bytes_le=guid_bytes)
    except Exception:
        guid_obj = None

    name_len = payload[17]
    name_start = 18
    name_end = name_start + name_len
    if name_end > len(payload):
        return None
        
    name_bytes = payload[name_start:name_end]
    try:
        name_str = name_bytes.decode("ascii")
    except UnicodeDecodeError:
        name_str = None

    remainder = payload[name_end:]
    log_line(log_f, f"{indent}[auth] opcode: 0x{opcode:02x}, name: {name_str!r}, guid: {guid_obj}")
    return {
        "opcode": opcode,
        "guid_bytes": guid_bytes,
        "name": name_str,
        "remainder": remainder,
    }

def try_decode_login_request(payload: bytes, log_f, indent="      "):
    if len(payload) < 16:
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
            break
        field_len = payload[pos]
        pos += 1
        field_end = pos + field_len
        if field_end > len(payload):
            break
        field_bytes = payload[pos:field_end]
        try:
            fields[field_name] = field_bytes.decode("utf-8")
        except UnicodeDecodeError:
            fields[field_name] = field_bytes.hex()
        pos = field_end

    remainder = payload[pos:]
    log_line(log_f, f"{indent}[login] guid: {guid_obj}, fields: {fields}")
    return {
        "guid_bytes": guid_bytes,
        "fields": fields,
        "remainder": remainder,
    }

def build_login_response(request_guid_bytes: bytes) -> bytes:
    # returns result code 6 (Validated) + placeholder json profile
    player_profile = b"{}"  
    profile_len = struct.pack("<I", len(player_profile))
    return request_guid_bytes + bytes([0x06]) + profile_len + player_profile

def build_auth_response(request_guid_bytes: bytes) -> bytes:
    # 0x81 response opcode + guid + validated(true) + target location rdv01
    return bytes([0x81]) + request_guid_bytes + bytes([0x01, 0x05]) + b"rdv01"

def parse_and_respond(data: bytes, addr, sock, log_f, state):
    pos = 0
    response = b""

    while pos < len(data):
        type_byte = data[pos]
        block_start = pos
        pos += 1
        reliable = bool(type_byte & OPT_REL)
        base_type = type_byte & TYPE_MASK

        block_id = None
        if reliable:
            if pos + 4 > len(data):
                break
            block_id = struct.unpack(">I", data[pos:pos+4])[0]
            pos += 4

        if base_type == TYPE_ACK:
            if pos + 4 > len(data):
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

        elif base_type == TYPE_SYN:
            log_line(log_f, f"  -> SYN reliable={reliable} id={block_id}")
            if reliable:
                response += pack_ack_single(block_id)
                phase = state["phase"].get(addr)
                
                if phase is None:
                    state["phase"][addr] = "rdv_connecting"
                    log_line(log_f, f"  [handshake] new connection -> sending SYN id={state['our_block_id']}")
                    response += pack_syn(state["our_block_id"])
                    state["our_block_id"] += 1
                elif phase == "rdv_established" and block_id == 0:
                    # fresh syn 0 after rdv is up indicates client triggered stud connect via TouchPeer
                    state["phase"][addr] = "stud_connecting"
                    log_line(log_f, f"  [handshake] stud handshake initiated -> sending SYN id={state['our_block_id']}")
                    response += pack_syn(state["our_block_id"])
                    state["our_block_id"] += 1

        elif base_type == TYPE_CHK:
            if reliable and block_id is not None:
                response += pack_ack_single(block_id)

        elif base_type == TYPE_FIN:
            log_line(log_f, f"  -> FIN reliable={reliable} id={block_id}")

        elif base_type == TYPE_DAT:
            new_pos, info = decode_dat_payload(data, pos, type_byte, log_f)
            if new_pos is None:
                pos = len(data)
                break
            pos = new_pos

            if reliable and block_id is not None:
                response += pack_ack_single(block_id)

            auth_info = try_decode_auth_request(info["payload"], log_f)
            if auth_info is not None:
                auth_response_payload = build_auth_response(auth_info["guid_bytes"])
                dat_block = pack_dat_single(state["our_block_id"], info["message_id"], auth_response_payload)
                state["our_block_id"] += 1
                response += dat_block
                state["phase"][addr] = "rdv_established"
                continue

            login_info = None
            if state["phase"].get(addr) in ("stud_connecting", "stud_established"):
                login_info = try_decode_login_request(info["payload"], log_f)

            if login_info is not None:
                login_response_payload = build_login_response(login_info["guid_bytes"])
                dat_block = pack_dat_single(state["our_block_id"], info["message_id"], login_response_payload)
                state["our_block_id"] += 1
                response += dat_block
                state["phase"][addr] = "stud_established"

        elif base_type == TYPE_ERR or base_type == TYPE_FDB:
            pos = len(data)
        else:
            break

    return response

def main():
    print("============================================================")
    print("Horse Star RDV/STUD Stub Server v6")
    print("============================================================")
    print(f"Binding to {HOST}:{RDV_PORT}")
    print("Press Ctrl+C to stop.")
    print("============================================================")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((HOST, RDV_PORT))
    except OSError as e:
        print(f"FAILED to bind socket: {e}")
        sys.exit(1)

    log_f = open(LOG_FILE, "a", encoding="utf-8")
    session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_f.write(f"\n--- SESSION START: {session_start} ---\n")
    log_f.flush()

    state = {"our_block_id": 0, "phase": {}}
    packet_count = 0

    try:
        while True:
            data, addr = sock.recvfrom(65535)
            packet_count += 1
            now = datetime.now().strftime("%H:%M:%S.%f")

            log_line(log_f, f"[{now}] PACKET #{packet_count} from {addr[0]}:{addr[1]} ({len(data)} bytes):")
            log_line(log_f, hex_dump(data))

            response = parse_and_respond(data, addr, sock, log_f, state)
            if response:
                sock.sendto(response, addr)
                log_line(log_f, f"  [send] -> {addr} ({len(response)} bytes):")
                log_line(log_f, hex_dump(response))
            log_line(log_f, "")

    except KeyboardInterrupt:
        print(f"\nStopping server. Received total packets: {packet_count}")
        log_f.write(f"--- SESSION END. Total packets: {packet_count} ---\n")
        log_f.close()
        sock.close()
        sys.exit(0)

if __name__ == "__main__":
    main()


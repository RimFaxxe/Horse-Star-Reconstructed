"""
Horse Star RDV/STUD Stub Server v23
Handles the full login flow:
RDV: SYN handshake -> AuthRequest -> AuthResponse -> GetPeerRequest -> GetPeerResponse
STUD: SYN handshake -> ConfirmReconnectionRequest -> ConfirmReconnectionResponse -> LoginRequest -> LoginResponse
"""
import select
import socket
import struct
import sys
import uuid
from datetime import datetime

# network configurations
HOST = "127.0.0.1"
RDV_PORT = 15250 
STUD_PORT = 1025 
LOG_FILE = "rdv_stub_log.txt"

# oudp constants
TYPE_ACK = 0x10 
TYPE_CHK = 0x20 
TYPE_DAT = 0x30 
TYPE_ERR = 0x40 
TYPE_FDB = 0x50 
TYPE_FIN = 0x60 
TYPE_SYN = 0x70 
TYPE_MASK = 0xF0 
OPT_REL = 0x01 
OPT_SINGLE = 0x02 
OPT_RANGE = 0x04 
OPT_MPD = 0x02 

# pom message opcodes
OPCODE_AUTH_REQUEST = 0x01 
OPCODE_GET_PEER_REQUEST = 0x02 
OPCODE_CLOSE_REQUEST = 0x03
OPCODE_CLOSE_RESPONSE = 0x04
OPCODE_CONFIRM_RECONNECT_REQ = 0x05
OPCODE_CONFIRM_RECONNECT_RES = 0x06
OPCODE_AUTH_RESPONSE = 0x81 
OPCODE_GET_PEER_RESPONSE = 0x82 
OPCODE_LOGIN_RESPONSE = 0x06 
OPCODE_STUD_IDENTIFY = 0x02

def log_line(f, line: str):
    print(line)
    f.write(line + "\n")
    f.flush()

def hex_dump(data: bytes, indent: str = " ") -> str:
    if not data:
        return f"{indent}(empty)"
    lines = []
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk).ljust(47)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{indent}{offset:04x}: {hex_part} {ascii_part}")
    return "\n".join(lines)

# network pack helpers
def pack_syn(block_id: int) -> bytes:
    return bytes([TYPE_SYN | OPT_REL]) + struct.pack(">I", block_id)

def pack_ack_single(acked_id: int) -> bytes:
    return bytes([TYPE_ACK | OPT_SINGLE]) + struct.pack(">I", acked_id)

def pack_dat_single(block_id: int, message_id: int, payload: bytes) -> bytes:
    header = (bytes([TYPE_DAT | OPT_REL])
              + struct.pack(">I", block_id)
              + struct.pack(">I", message_id)
              + struct.pack(">H", len(payload)))
    return header + payload

def decode_dat_payload(data: bytes, pos: int, type_byte: int, log_f, indent=" "):
    multipart = bool(type_byte & OPT_MPD)
    if pos + 4 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: not enough bytes for message_id")
        return None, None
    message_id = struct.unpack(">I", data[pos:pos+4])[0]
    log_line(log_f, f"{indent}[DAT] messageId @ offset {pos}: {message_id} (bytes: {data[pos:pos+4].hex()})")
    pos += 4
    if pos + 2 > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: not enough bytes for dataLength")
        return None, None
    data_length = struct.unpack(">H", data[pos:pos+2])[0]
    log_line(log_f, f"{indent}[DAT] dataLength @ offset {pos}: {data_length} (bytes: {data[pos:pos+2].hex()})")
    pos += 2
    if pos + data_length > len(data):
        log_line(log_f, f"{indent}[DAT] truncated: declared {data_length} bytes but only {len(data)-pos} remain")
        return None, None
    payload = data[pos:pos+data_length]
    log_line(log_f, f"{indent}[DAT] payload @ offset {pos}, {data_length} bytes:")
    log_line(log_f, hex_dump(payload, indent=indent + " "))
    pos += data_length
    return pos, {"message_id": message_id, "payload": payload}

# message parsers
def try_decode_auth_request(payload: bytes, log_f, indent=" "):
    if len(payload) < 18 or payload[0] != OPCODE_AUTH_REQUEST:
        return None
    opcode = payload[0]
    guid_bytes = payload[1:17]
    try:
        guid_obj = uuid.UUID(bytes_le=guid_bytes)
    except Exception:
        guid_obj = None
    name_len = payload[17]
    name_end = 18 + name_len
    if name_end > len(payload):
        return None
    name_bytes = payload[18:name_end]
    try:
        name_str = name_bytes.decode("ascii")
    except UnicodeDecodeError:
        name_str = name_bytes.hex()
    log_line(log_f, f"{indent}[auth] opcode byte: 0x{opcode:02x}")
    log_line(log_f, f"{indent}[auth] name bytes: {name_bytes.hex()} (ASCII: {name_str!r})")
    return {"guid_bytes": guid_bytes, "name": name_str}

def try_decode_stud_identify(payload: bytes, log_f, indent=" "):
    if len(payload) < 4 or payload[0] != OPCODE_STUD_IDENTIFY or len(payload) >= 18:
        return None
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
    for k, v in fields.items():
        log_line(log_f, f"{indent}[stud_id] {k}: {v!r}")
    return {"is_reconnecting": is_reconnecting, "fields": fields}

def try_decode_get_peer_request(payload: bytes, log_f, indent=" "):
    if len(payload) < 18 or payload[0] != OPCODE_GET_PEER_REQUEST:
        return None
    guid_bytes = payload[1:17]
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
    return {"guid_bytes": guid_bytes, "fields": fields}

def try_decode_login_request(payload: bytes, log_f, indent=" "):
    if len(payload) < 17:
        return None
    if payload[0] in (OPCODE_AUTH_REQUEST, OPCODE_GET_PEER_REQUEST,
                      OPCODE_CLOSE_REQUEST, OPCODE_CLOSE_RESPONSE,
                      OPCODE_CONFIRM_RECONNECT_REQ, OPCODE_STUD_IDENTIFY):
        return None
    guid_bytes = payload[0:16]
    pos = 16
    fields = {}
    for field_name in ("login", "password", "sessionId", "rdvId"):
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
    return {"guid_bytes": guid_bytes, "fields": fields}

# packet factories
def build_auth_response(request_guid_bytes: bytes) -> bytes:
    return bytes([OPCODE_AUTH_RESPONSE]) + request_guid_bytes + bytes([0x01, 0x05]) + b"rdv01"

def build_stud_identify_response(public_ip: str = "127.0.0.1", rdv_location: str = "rdv01") -> bytes:
    host_bytes = public_ip.encode("utf-8")
    rdv_bytes = rdv_location.encode("utf-8")
    return (bytes([0x02, 0x00]) +
            bytes([len(host_bytes)]) + host_bytes +
            bytes([len(rdv_bytes)]) + rdv_bytes)

def build_get_peer_response(request_guid_bytes: bytes, public_ip: str = "127.0.0.1", public_port: int = STUD_PORT) -> bytes:
    ip_bytes = bytes(int(x) for x in public_ip.split("."))
    port_bytes = struct.pack("<H", public_port)
    endpoint = port_bytes + bytes([len(ip_bytes)]) + ip_bytes
    return bytes([OPCODE_GET_PEER_RESPONSE]) + request_guid_bytes + endpoint + bytes([0x00])

def build_login_response(request_guid_bytes: bytes) -> bytes:
    player_profile = b"{}"
    profile_len = struct.pack("<I", len(player_profile))
    return request_guid_bytes + bytes([0x06]) + profile_len + player_profile

# packet router
def parse_and_respond(data: bytes, state_key, sock, stud_sock, log_f, state):
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
                
        elif base_type == TYPE_SYN:
            if reliable:
                response += pack_ack_single(block_id)
            phase = state["phase"].get(state_key)
            if phase is None:
                if sock == stud_sock:
                    state["phase"][state_key] = "stud_connecting"
                else:
                    state["phase"][state_key] = "rdv_connecting"
                response += pack_syn(state["our_block_id"])
                state["our_block_id"] += 1
            elif phase == "rdv_established" and block_id == 0:
                state["phase"][state_key] = "stud_connecting"
                response += pack_syn(state["our_block_id"])
                state["our_block_id"] += 1
                
        elif base_type == TYPE_CHK:
            if reliable and block_id is not None:
                response += pack_ack_single(block_id)
                
        elif base_type == TYPE_FIN:
            pass
        elif base_type == TYPE_ERR:
            pos = len(data)
        elif base_type == TYPE_FDB:
            if pos + 4 > len(data):
                break
            pos += 4
            
        elif base_type == TYPE_DAT:
            new_pos, info = decode_dat_payload(data, pos, type_byte, log_f)
            if new_pos is None:
                break
            pos = new_pos
            if reliable and block_id is not None:
                response += pack_ack_single(block_id)
            phase = state["phase"].get(state_key)
            payload = info["payload"]
            
            # auth handling
            auth_info = try_decode_auth_request(payload, log_f)
            if auth_info is not None:
                resp_payload = build_auth_response(auth_info["guid_bytes"])
                dat_block = pack_dat_single(state["our_block_id"], info["message_id"], resp_payload)
                state["our_block_id"] += 1
                response += dat_block
                if phase == "stud_connecting":
                    state["phase"][state_key] = "stud_authed"
                else:
                    state["phase"][state_key] = "rdv_established"
                continue
                
            # peer discovery logic
            if phase == "rdv_established":
                get_peer_info = try_decode_get_peer_request(payload, log_f)
                if get_peer_info is not None:
                    resp_payload = build_get_peer_response(get_peer_info["guid_bytes"], public_ip=HOST, public_port=STUD_PORT)
                    dat_block = pack_dat_single(state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    
            # peer identification
            elif phase == "stud_connecting":
                stud_id = try_decode_stud_identify(payload, log_f)
                if stud_id is not None:
                    resp_payload = build_stud_identify_response(public_ip=HOST, rdv_location="rdv01")
                    dat_block = pack_dat_single(state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    state["phase"][state_key] = "stud_identified"
                    
            # login handling
            elif phase in ("stud_identified", "stud_authed", "stud_established"):
                login_info = try_decode_login_request(payload, log_f)
                if login_info is not None:
                    resp_payload = build_login_response(login_info["guid_bytes"])
                    dat_block = pack_dat_single(state["our_block_id"], info["message_id"], resp_payload)
                    state["our_block_id"] += 1
                    response += dat_block
                    state["phase"][state_key] = "stud_established"
        else:
            break
    return response

def main():
    print("=========================================")
    print("Horse Star RDV/STUD Stub Server")
    print("=========================================")
    
    rdv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        rdv_sock.bind((HOST, RDV_PORT))
    except OSError as e:
        print(f"FAILED to bind RDV socket {HOST}:{RDV_PORT} -> {e}")
        sys.exit(1)
        
    stud_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        stud_sock.bind((HOST, STUD_PORT))
    except OSError as e:
        print(f"FAILED to bind STUD socket {HOST}:{STUD_PORT} -> {e}")
        rdv_sock.close()
        sys.exit(1)
        
    sock_labels = {rdv_sock: f"RDV:{RDV_PORT}", stud_sock: f"STUD:{STUD_PORT}"}
    log_f = open(LOG_FILE, "a", encoding="utf-8")
    
    state = {"our_block_id": 0, "phase": {}}
    packet_count = 0
    
                log_line(log_f, f"[{now}] PACKET #{packet_count} [{sock_labels[sock]}] from {addr[0]}:{addr[1]} ({len(data)} bytes):")
                try:
                    response = parse_and_respond(data, state_key, sock, stud_sock, log_f, state)
                    if response:
                        sock.sendto(response, addr)
                except Exception as e:
                    import traceback
                    log_line(log_f, f" [CRASH] Exception: {e}\n{traceback.format_exc()}")
    except KeyboardInterrupt:
        print("\nStopping stub server...")
    finally:
        log_f.close()
        rdv_sock.close()
        stud_sock.close()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import socket, struct, time

# ===================== CONFIG (EDIT HOST/PORT) =====================
SERVER_HOST = '127.0.0.1'   # server IP or hostname
ASSIGNED_PORT = 30069       # <-- keep your assigned UDP port
SERVER = (SERVER_HOST, ASSIGNED_PORT)
# ==================================================================

# Timing/reliability parameters
RTO = 0.5        # retransmission timeout (seconds)
RETRIES = 10     # max retries per send (bumped to ensure visible retransmits)
CHUNK = 200      # bytes per DATA chunk

# --- Protocol type codes (1 byte) ---
SYN, SYN_ACK, ACK, DATA, DATA_ACK, FIN, FIN_ACK = 1,2,3,4,5,6,7

# Header format: type(1B) | seq(4B) | len(2B)
HDR = '!B I H'
HDR_SZ = struct.calcsize(HDR)

# A larger message to force multiple DATA/ACK pairs.
MESSAGE = (
    'Hello from student RUDP client!\n'
    'This demo implements handshake, DATA+ACK with stop-and-wait, '
    'and FIN teardown over UDP.\n'
    'Below are numbered lines to create many packets.\n'
    + 'Line ' + '\nLine '.join(str(i) for i in range(1, 101)) + '\n'
)

def pack_msg(tp: int, seq: int, payload: bytes = b'') -> bytes:
    if isinstance(payload, str):
        payload = payload.encode()
    return struct.pack(HDR, tp, seq, len(payload)) + payload

def unpack_msg(pkt: bytes):
    if len(pkt) < HDR_SZ:
        return None, None, b''
    tp, seq, ln = struct.unpack(HDR, pkt[:HDR_SZ])
    return tp, seq, pkt[HDR_SZ:HDR_SZ+ln]

def send_recv_with_retry(sock, pkt, expect_types, expect_seq=None):
    """
    Send 'pkt', then wait (with timeout) for a response in expect_types,
    optionally matching expect_seq. Retry up to RETRIES on timeout.
    Returns (tp, seq) on success, (None, None) on failure.
    """
    for attempt in range(1, RETRIES + 1):
        sock.sendto(pkt, SERVER)
        sock.settimeout(RTO)
        try:
            resp, _ = sock.recvfrom(2048)
            tp, s, _ = unpack_msg(resp)
            if tp in expect_types and (expect_seq is None or s == expect_seq):
                return tp, s
        except socket.timeout:
            # On timeout, loop and retransmit
            pass
    return None, None

def main():
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ============ PHASE 1: HANDSHAKE ============
    print('[CLIENT] SYN')
    tp, s = send_recv_with_retry(cli, pack_msg(SYN, 0, b''), expect_types={SYN_ACK})
    if tp != SYN_ACK:
        print('[CLIENT] Handshake failed: no SYN-ACK')
        cli.close()
        return
    print('[CLIENT] SYN-ACK')
    cli.sendto(pack_msg(ACK, 0, b''), SERVER)
    print('[CLIENT] Connection established')

    # ============ PHASE 2: DATA SEND LOOP (stop-and-wait) =========
    data = MESSAGE.encode()
    seq = 0
    for off in range(0, len(data), CHUNK):
        chunk = data[off:off+CHUNK]
        print(f'[CLIENT] DATA seq={seq} (len={len(chunk)})')
        tp, s = send_recv_with_retry(cli, pack_msg(DATA, seq, chunk),
                                     expect_types={DATA_ACK}, expect_seq=seq)
        if tp != DATA_ACK:
            print(f'[CLIENT] Failed to deliver seq={seq} after retries')
            cli.close()
            return
        print(f'[CLIENT] ACK seq={seq}')
        seq += 1

    # ============ PHASE 3: TEARDOWN ============
    print('[CLIENT] FIN')
    tp, s = send_recv_with_retry(cli, pack_msg(FIN, 0, b''), expect_types={FIN_ACK})
    if tp == FIN_ACK:
        print('[CLIENT] Connection closed')
    else:
        print('[CLIENT] Teardown failed: no FIN-ACK')

    cli.close()

if __name__ == '__main__':
    main()

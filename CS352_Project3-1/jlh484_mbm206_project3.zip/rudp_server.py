#!/usr/bin/env python3
import socket, struct, time, random

# ===================== CONFIG (EDIT YOUR PORT) =====================
ASSIGNED_PORT = 30069  # <-- keep your assigned UDP port
# ==================================================================

# --- Protocol type codes (1 byte) ---
SYN, SYN_ACK, ACK, DATA, DATA_ACK, FIN, FIN_ACK = 1,2,3,4,5,6,7

# Header format: type(1B) | seq(4B) | len(2B)
HDR = '!B I H'
HDR_SZ = struct.calcsize(HDR)

def pack_msg(tp: int, seq: int, payload: bytes = b'') -> bytes:
    if isinstance(payload, str):
        payload = payload.encode()
    return struct.pack(HDR, tp, seq, len(payload)) + payload

def unpack_msg(pkt: bytes):
    if len(pkt) < HDR_SZ:
        return None, None, b''
    tp, seq, ln = struct.unpack(HDR, pkt[:HDR_SZ])
    return tp, seq, pkt[HDR_SZ:HDR_SZ+ln]

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', ASSIGNED_PORT))
    print(f'[SERVER] Listening on 0.0.0.0:{ASSIGNED_PORT} (UDP)')

    client_addr = None
    established = False
    expect_seq = 0  # next in-order DATA seq we expect

    while True:
        pkt, addr = sock.recvfrom(2048)
        tp, seq, pl = unpack_msg(pkt)
        if tp is None:
            continue

        # ============ PHASE 1: HANDSHAKE ============
        if not established:
            # Accept handshake only from the first client that sends SYN
            if tp == SYN and client_addr is None:
                client_addr = addr
                print('[SERVER] got SYN from', addr)
                sock.sendto(pack_msg(SYN_ACK, 0, b''), client_addr)
                continue
            # Finish handshake when the same client sends ACK
            if tp == ACK and addr == client_addr:
                print('[SERVER] handshake complete')
                established = True
                expect_seq = 0
                continue
            # Ignore others until we've established
            continue

        # Ignore packets from other addresses once a client is set
        if client_addr is not None and addr != client_addr:
            continue

        # ============ PHASE 2: DATA =================
        if tp == DATA:
            if seq == expect_seq:
                # In-order packet: apply random ACK delay to induce client timeouts/retries
                # Required: insert a random ACK delay before replying (per project requirements)
                delay_ms = random.randint(100, 1000)
                time.sleep(delay_ms / 1000.0)
                
                # "Deliver" payload (optional: print so you can see ordering)
                try:
                    text = pl.decode(errors='replace')
                except Exception:
                    text = repr(pl)
                print(f'[SERVER] DATA seq={seq} (delivered, len={len(pl)})')

                # ACK this exact seq
                sock.sendto(pack_msg(DATA_ACK, seq, b''), client_addr)
                expect_seq += 1
            else:
                # Out-of-order (likely duplicate/retransmission): handle immediately without delay
                # This ensures reliability - retransmissions should be ACKed quickly
                # Re-ACK the last in-order seq (expect_seq-1), keeping stop-and-wait happy
                ack_seq = expect_seq - 1 if expect_seq > 0 else 0
                print(f'[SERVER] out-of-order DATA seq={seq} (expect {expect_seq}); re-ACK {ack_seq}')
                sock.sendto(pack_msg(DATA_ACK, ack_seq, b''), client_addr)
            continue

        # ============ PHASE 3: TEARDOWN =============
        if tp == FIN:
            print('[SERVER] FIN received, closing')
            sock.sendto(pack_msg(FIN_ACK, 0, b''), client_addr)
            # Reset to allow a fresh client next time
            established = False
            client_addr  = None
            expect_seq   = 0
            continue

if __name__ == '__main__':
    main()

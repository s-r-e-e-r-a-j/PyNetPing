import socket
import struct
from typing import Optional
from .utils import now, packet_id

def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"

    total: int = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i + 1]

    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    return ~total & 0xFFFF

def icmp4_ping(host: str, timeout: float, seq: int) -> Optional[float]:
    sock: socket.socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW,
        socket.IPPROTO_ICMP
    )
    sock.settimeout(timeout)

    ident: int = packet_id()
    header: bytes = struct.pack("!BBHHH", 8, 0, 0, ident, seq)
    payload: bytes = struct.pack("!d", now())
    chksum: int = checksum(header + payload)
    packet: bytes = struct.pack("!BBHHH", 8, 0, chksum, ident, seq) + payload

    start: float = now()
    try:
        sock.sendto(packet, (host, 1))
        data, _ = sock.recvfrom(1024)
    except Exception:
        return None
    finally:
        sock.close()

    icmp_header: bytes = data[20:28]
    _, _, _, rid, rseq = struct.unpack("!BBHHH", icmp_header)

    if rid != ident or rseq != seq:
        return None

    return (now() - start) * 1000.0

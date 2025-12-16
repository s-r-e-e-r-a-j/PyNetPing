import socket
import struct
from typing import Optional
from .utils import now, packet_id

def icmp6_ping(host: str, timeout: float, seq: int) -> Optional[float]:
    try:
        sock: socket.socket = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
    except Exception:
        return None

    sock.settimeout(timeout)
    ident: int = packet_id()
    packet: bytes = struct.pack("!BBHHH", 128, 0, 0, ident, seq)

    start: float = now()
    try:
        sock.sendto(packet, (host, 0, 0, 0))
        data, _ = sock.recvfrom(1024)
    except Exception:
        return None
    finally:
        sock.close()

    if len(data) < 8:
        return None

    _, _, _, rid, rseq = struct.unpack("!BBHHH", data[:8])
    if rid != ident or rseq != seq:
        return None

    return (now() - start) * 1000.0

import socket
import struct
import random
from typing import Optional
from .utils import now, is_ipv6

def dns_ping(server: str, timeout: float) -> Optional[float]:
    try:
        family: int = socket.AF_INET6 if is_ipv6(server) else socket.AF_INET
    except Exception:
        return None

    sock: socket.socket = socket.socket(family, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    tid: int = random.randint(0, 65535)
    query: bytes = struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0) \
                    + b"\x03www\x06google\x03com\x00\x00\x01\x00\x01"

    start: float = now()
    try:
        sock.sendto(query, (server, 53))
        sock.recvfrom(512)
    except Exception:
        return None
    finally:
        sock.close()

    return (now() - start) * 1000.0

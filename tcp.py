import socket
from typing import Optional
from .utils import now, is_ipv6

def tcp_ping(host: str, port: int, timeout: float) -> Optional[float]:
    family: int = socket.AF_INET6 if is_ipv6(host) else socket.AF_INET
    sock: socket.socket = socket.socket(family, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    start: float = now()
    try:
        sock.connect((host, port))
    except Exception:
        return None
    finally:
        sock.close()

    return (now() - start) * 1000.0

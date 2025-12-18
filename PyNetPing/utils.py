# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import time
import os
import socket
import sys

def now() -> float:
    return time.perf_counter()

def packet_id() -> int:
    return os.getpid() & 0xFFFF

def is_ipv6(host: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, host)
        return True
    except OSError:
        return False

def has_raw_privileges() -> bool:
    if sys.platform.startswith("win"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.close()
            return True
        except Exception:
            return False
    else:
        return os.geteuid() == 0

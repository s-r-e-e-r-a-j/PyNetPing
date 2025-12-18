# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from .icmp4 import icmp4_ping
from .icmp6 import icmp6_ping
from .tcp import tcp_ping
from .http import http_ping
from .dns import dns_ping
from .stats import loss, jitter
from .result import PingResult
from .utils import is_ipv6, has_raw_privileges
from .rate import RateLimiter

def ping(
    host: str,
    count: int = 4,
    timeout: float = 1.0,
    port: int = 80,
    rate: float = 10.0,
    use_dns: bool = False
) -> PingResult:

    limiter: RateLimiter = RateLimiter(rate)
    times: list[float] = []
    ipv6: bool = is_ipv6(host)
    protocol_used: str = "none"
    error_reason: str | None = None

    for seq in range(count):
        limiter.wait()
        delay: float | None = None

        if has_raw_privileges():
            if ipv6:
                delay = icmp6_ping(host, timeout, seq)
                protocol_used = "icmp6"
            else:
                delay = icmp4_ping(host, timeout, seq)
                protocol_used = "icmp4"
        else:
            protocol_used = "tcp/http/dns"

        if delay is None:
            delay = tcp_ping(host, port, timeout)
            protocol_used = "tcp"

        if delay is None:
            delay = http_ping(host, timeout)
            protocol_used = "http"

        if delay is None and use_dns:
            delay = dns_ping(host, timeout)
            protocol_used = "dns"

        if delay is not None:
            times.append(delay)
        else:
            error_reason = "timeout/unreachable"

    received: int = len(times)

    return PingResult(
        host=host,
        sent=count,
        received=received,
        loss=loss(count, received),
        min_ms=min(times) if times else 0.0,
        avg_ms=sum(times) / received if received else 0.0,
        max_ms=max(times) if times else 0.0,
        jitter_ms=jitter(times),
        protocol=protocol_used,
        ip_version=6 if ipv6 else 4,
        error=error_reason
    )

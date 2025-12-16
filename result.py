from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class PingResult:
    host: str
    sent: int
    received: int
    loss: float
    min_ms: float
    avg_ms: float
    max_ms: float
    jitter_ms: float
    protocol: str = "icmp"
    ip_version: int = 4
    timestamp: str = datetime.utcnow().isoformat()
    error: str | None = None

# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from typing import Sequence
import statistics

def loss(sent: int, received: int) -> float:
    return ((sent - received) / sent) * 100.0 if sent else 100.0

def jitter(times: Sequence[float]) -> float:
    if len(times) < 2:
        return 0.0
    diffs: list[float] = [abs(times[i] - times[i-1]) for i in range(1, len(times))]
    return sum(diffs) / len(diffs)

def median(times: Sequence[float]) -> float:
    if not times:
        return 0.0
    return statistics.median(times)

def stdev(times: Sequence[float]) -> float:
    if len(times) < 2:
        return 0.0
    return statistics.stdev(times)

def p95(times: Sequence[float]) -> float:
    if not times:
        return 0.0
    return sorted(times)[int(len(times)*0.95)-1]

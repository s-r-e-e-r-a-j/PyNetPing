# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import time

class RateLimiter:
    def __init__(self, rate: float) -> None:
        self.rate: float = rate
        self.last: float = time.monotonic()

    def wait(self) -> None:
        delta: float = 1.0 / self.rate
        now: float = time.monotonic()
        diff: float = now - self.last

        if diff < delta:
            time.sleep(delta - diff)

        self.last = time.monotonic()

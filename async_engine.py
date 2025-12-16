# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import asyncio
from typing import Iterable
from .ping import ping
from .result import PingResult

async def ping_hosts(
    hosts: Iterable[str],
    count: int = 4,
    timeout: float = 1.0,
    limit: int = 100
) -> list[PingResult]:

    sem: asyncio.Semaphore = asyncio.Semaphore(limit)

    async def run(host: str) -> PingResult:
        async with sem:
            return await asyncio.to_thread(ping, host, count, timeout)

    return await asyncio.gather(*(run(h) for h in hosts))

# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import json
import csv
from typing import Iterable
from dataclasses import asdict
from .result import PingResult

def to_json(results: Iterable[PingResult]) -> str:
    return json.dumps([asdict(r) for r in results], indent=2)

def to_csv(results: Iterable[PingResult], path: str) -> None:
    items = list(results)
    if not items:
        return

    rows = [asdict(r) for r in items]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import argparse
from .ping import ping
from .output import to_json, to_csv
import sys
import os

def main() -> None:
    parser = argparse.ArgumentParser(prog="pynetping")

    parser.add_argument("host", help="Target host to ping")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout in seconds")
    parser.add_argument("-r", "--rate", type=float, default=10.0, help="Requests per second")
    parser.add_argument("--dns", action="store_true", help="Use DNS ping if other protocols fail")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--csv", help="Output CSV file path")

    args = parser.parse_args()

    if os.name != "nt" and os.geteuid() != 0:
        print("WARNING: Run as root for full ICMP coverage")

    result = ping(
        host=args.host,
        count=args.count,
        timeout=args.timeout,
        rate=args.rate,
        use_dns=args.dns
    )

    if args.json:
        print(to_json([result]))
    elif args.csv:
        to_csv([result], args.csv)
        print(f"CSV saved: {args.csv}")
    else:
        print(result)

    # Exit codes for automation
    if result.received == 0:
        sys.exit(2)  # unreachable
    elif result.loss > 0:
        sys.exit(1)  # partial loss
    else:
        sys.exit(0)  # success

if __name__ == "__main__":
    main()

# PyNetPing

**PyNetPing** is a Python library and CLI tool for host reachability testing. It supports ICMP, TCP, HTTP, and DNS pings over IPv4 and IPv6, with automatic fallback if one method fails.


---

## Features

- Ping hosts using multiple protocols:

  - ICMP (IPv4 & IPv6)

  - TCP (IPv4 & IPv6)

  - HTTP (IPv4 & IPv6)

  - DNS (IPv4 & IPv6)

- **Automatic fallback if a protocol fails:** ICMP → TCP → HTTP → DNS

- Automatic IP version detection based on host address
  
- **Detailed Statistics:**

  - Packets sent / received

  - Packet loss (%)

  - Minimum, maximum, and average latency (ms)

  - Jitter (ms) – variation in latency


- **Concurrent Pings:** Ping multiple hosts at the same time using the async engine.

- **Output Options:**

  - JSON output for easy integration

  - Save results as CSV files


- **CLI Tool:** Use PyNetPing directly from the command line with all the above features.

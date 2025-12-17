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

---

## Requirements

- **Python 3.10 or higher**

- Privileges:

  - **ICMP requires elevated privileges:**

    - Linux / macOS: run as root

    - Windows: run as Administrator


 - If ICMP is unavailable, PyNetPing automatically falls back to TCP, HTTP, or DNS

---

## IPv6 Notes

- All ping methods support IPv6

- IPv6 availability depends on:
   - Network configuration

   - OS support

- If IPv6 is unreachable, fallback mechanisms apply automatically

--- 

## Installation

**Clone the repository:**
```bash
git clone https://github.com/s-r-e-e-r-a-j/PyNetPing.git
```

This will create a folder named PyNetPing.

---

## Using PyNetPing as a Library

**To use PyNetPing as a library:**

 - The `PyNetPing` folder must be in the same directory as your Python script

**Example Directory Structure**

```md
project/
├── PyNetPing/
│   ├── ping.py
│   ├── cli.py
│   └── ...
└── test.py
```

### The `ping()` Function

PyNetPing exposes a single main function for reachability testing: `ping()`.

It automatically selects the best available method and falls back if one method fails.

#### Function Signature:
```python
ping(
    host: str, # required
    count: int = 4,
    timeout: float = 1.0,
    port: int = 80,
    rate: float = 10.0,
    use_dns: bool = False
) -> PingResult
```

#### ping() Arguments:

| Argument | Required  | Default | Description                                    |
|-----------|----------|---------|------------------------------------------------|
| `host`    | **Yes**  | —       | Target hostname or IP address (IPv4 or IPv6)   |
| `count`   | No       | `4`     | Number of ping attempts                        |
| `timeout` | No       | `1.0`   | Timeout per request in seconds                 |
| `port`    | No       | `80`    | TCP port used **only for TCP fallback**        |
| `rate`    | No       | `10.0`  | Requests per second (rate limiting)            |
| `use_dns` | No       | `False` | Enable DNS ping fallback if other methods fail |

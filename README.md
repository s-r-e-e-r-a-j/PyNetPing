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

--- 

## Examples

### Basic Ping Usage (Library)

The simplest way to check if a host is reachable.

```python
from PyNetPing import ping

result = ping("8.8.8.8")
print(result)
```

- Automatically selects IPv4 or IPv6
- Uses ICMP if available
- Falls back to TCP → HTTP if needed

### Advanced Usage (Library)

Custom Ping Count, Timeout, and Rate

```python
from PyNetPing import ping

result = ping(
    host="8.8.8.8",
    count=10,
    timeout=2.0,
    rate=5.0
)

print(result)
```

**Explanation:**

- Sends 10 ping requests

- Waits up to 2 seconds per request

- Limits sending speed to 5 requests per second

### Enable DNS Fallback (Library) (Optional)

DNS ping is disabled by default and only used if explicitly enabled.

```python
from PyNetPing import ping

result = ping(
    host="8.8.8.8",
    use_dns=True
)

print(result)
```
- DNS is attempted only if ICMP, TCP, and HTTP fail

### Specify TCP Port for Fallback (Library)

TCP fallback uses port 80 by default. You can override it:

```python
from PyNetPing import ping

result = ping(
    host="8.8.8.8",
    port=443
)

print(result)
```
- TCP fallback will try port 443 instead of 80

### Save Output as JSON (Library)

```python
from PyNetPing import ping
from PyNetPing import to_json

result = ping("8.8.8.8")
json_data = to_json([result])

print(json_data)
```

### Save Output as CSV (Library)

```python
from PyNetPing import ping
from PyNetPing import to_csv

result = ping("8.8.8.8")
to_csv([result], "results.csv")
```

### Ping Multiple Hosts (Async) (Library)

```python
import asyncio
from PyNetPing import ping_hosts

hosts = ["8.8.8.8", "1.1.1.1", "google.com"]

results = asyncio.run(
    ping_hosts(
        hosts,
        count=3, # number of ping requests per host (default 4)
        timeout=1.5,  # max wait per ping in seconds (default 1.0)
        port=443, # Fallback TCP ping port if ICMP fails (default: 80)
        limit=50  # max number of concurrent pings (default 100)
    )
)

for r in results:
    print(r)
```

## Using PyNetPing as a CLI Tool

PyNetPing also works as a command-line tool. The PyNetPing folder must be in the current working directory when running the CLI.

CLI automatically selects the best protocol: ICMP → TCP → HTTP → DNS (if `--dns` is enabled).

Run as root/admin to use ICMP ping fully. On Linux/macOS.in windows run as administrator:

**Exit codes for automation:**

| Exit Code | Meaning                      |
|-----------|------------------------------|
| 0         | Success (all pings received) |
| 1         | Partial packet loss          |
| 2         | Host unreachable             |

### Basic Usage:
```bash
python3 -m PyNetPing.cli 8.8.8.8
```

### Options:

| Option           | Type  | Default | Description                                      |
|------------------|-------|---------|--------------------------------------------------|
| host             | str   | —       | Target host to ping (required)                   |
| -c, --count      | int   | 4       | Number of ping requests to send                  |
| -t, --timeout    | float | 1.0     | Timeout in seconds for each request              |
| -r, --rate       | float | 10.0    | Maximum requests per second                      |
| --dns            | flag  | False   | Use DNS ping if other protocols fail             |
| --json           | flag  | False   | Output results in JSON format                    |
| --csv            | str   | —       | Save output to the specified CSV file            |

### Examples:

1. **Basic ping:**
```bash
python3 -m PyNetPing.cli 8.8.8.8
```

2. **Ping with 10 Requests, 2-Second Timeout, and Custom Rate**
```bash
python3 -m PyNetPing.cli 8.8.8.8 -c 10 -t 2 -r 5
```
Explanation:

- `-c 10` → Send 10 ping requests

- `-t 2` → Wait up to 2 seconds for each request

- `-r 5` → Send 5 requests per second

- `8.8.8.8` → Target host

3. **print output in JSON format:**
```bash
python3 -m PyNetPing.cli 8.8.8.8 --json
```

4. **Save output to CSV file:**
```bash
python3 -m PyNetPing.cli 8.8.8.8 --csv output.csv
```

## License
This project is licensed under the MIT License

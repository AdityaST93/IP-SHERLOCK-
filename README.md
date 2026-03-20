# IP Intelligence & Network Awareness Dashboard

## Overview

The **IP Intelligence & Network Awareness Dashboard** is a Python-based, educational networking tool designed for **defensive cybersecurity training**, **network visibility**, and **academic experimentation**.

The dashboard provides:

- **Public IP detection** using a secure external API.
- **IP information lookup** via a free geolocation service.
- **Educational, controlled port scanning** of a small set of common ports.
- A **simple, interactive CLI** with clear formatting and error handling.

This project is deliberately conservative in scope and performance. It is **not** designed for offensive security testing or large-scale scanning.

---

## Features

- **Public IP Detection**
  - Uses `https://api.ipify.org?format=json`.
  - Shows your current public IPv4 address as seen from the internet.
  - Handles timeouts and API failures gracefully.

- **IP Information Lookup**
  - Uses the free `ip-api.com` service.
  - Displays:
    - Country, region, city
    - ISP and organization
    - Latitude, longitude (approximate)
    - Timezone
    - ASN (Autonomous System Number), when available
  - Validates IP format before sending the request.
  - Handles invalid or failed responses robustly.

- **Educational Port Scanner**
  - Uses Python's built-in `socket` library.
  - Scans **only a fixed list of common TCP ports**: `21, 22, 80, 443, 8080`.
  - Single-threaded by design (no performance optimization for abuse).
  - 1-second per-port timeout, with a small delay between probes.
  - Prints **only open ports** from the scanned list.
  - Optional CSV export of scan results (`scan_results.csv`).
  - Displays a **strong legal/ethical disclaimer** before any scan.

- **CLI Interface**
  - Interactive text menu:
    1. Detect my public IP
    2. Lookup IP information
    3. Scan common ports
    4. Exit
  - Loops until the user explicitly chooses to exit.
  - Clean, formatted output sections.
  - Optional color output via `colorama` (falls back to plain text if missing).

- **Logging**
  - Logs errors and events to `app.log`.
  - Helpful for understanding proper error handling in production-like tools.

---

## Installation

### Requirements

- **Python**: 3.10 or newer
- **Libraries**:
  - Standard library: `socket`, `re`, `csv`, `logging`, `sys`, `time`, `datetime`
  - Third-party:
    - `requests`
    - `colorama` (optional, for colored CLI output)

### Setup Steps

1. **Clone or copy the project files** into a directory, for example:

   ```bash
   cd c:\ip
   ```

2. **Create a virtual environment (recommended)**:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install requests colorama
   ```

   > `colorama` is optional. If it is not installed, the application will still work with plain text output.

---

## How to Run

From the project directory:

```bash
python main.py
```

You will see a banner and a menu with four options:

1. **Detect my public IP** – queries a secure public IP API.
2. **Lookup IP information** – asks for an IP and retrieves geolocation data.
3. **Scan common ports (educational)** – runs a safe, small-port scan.
4. **Exit** – quits the application.

Use the number keys `1`–`4` followed by Enter to navigate.

---

## Educational Networking Concepts

This project includes docstrings and inline comments explaining several key network concepts:

### What is an IP address?

An **Internet Protocol (IP) address** is a numerical label assigned to devices on a network. It acts as both:

- An **identifier**: who the device is on the network.
- A **locator**: where that device is, from a routing perspective.

There are **public IPs** (visible on the internet, usually assigned to your router or gateway) and **private IPs** (used only inside local networks).

### What is a port?

A **port** is a 16-bit number associated with an IP address that identifies a particular process or network service on a host.

Examples:

- HTTP: TCP port 80
- HTTPS: TCP port 443
- SSH: TCP port 22

Ports allow many networked applications to share a single IP address while keeping traffic properly routed to the correct process.

### What is a TCP connection?

**Transmission Control Protocol (TCP)** is a connection-oriented transport protocol that provides reliable, ordered delivery of bytes between two endpoints.

The classic **three-way handshake**:

1. **SYN** – Client asks to start a connection.
2. **SYN-ACK** – Server acknowledges and agrees.
3. **ACK** – Client confirms, and the connection is established.

If the port is closed or filtered, this handshake fails or times out, which is what simple port scanners detect.

### What is an IP geolocation database?

An **IP geolocation database** maps IP ranges to:

- Geographic information (country, region, city).
- Approximate coordinates (latitude, longitude).
- Network owner and routing details (ISP, organization, ASN).

Key points:

- Geolocation data is **approximate**, not exact.
- It can be **inaccurate or outdated**.
- It should be used alongside other information, not as the sole basis for critical decisions.

---

## Legal & Ethical Usage Notice

This project is provided **solely for educational and defensive purposes**:

- Only scan systems and networks that you **own** or for which you have **explicit, written permission** to test.
- Unauthorized scanning of networks or systems may violate laws, terms of service, or acceptable use policies.
- The authors and distributors of this tool are **not responsible** for misuse, damages, or any legal consequences arising from its use.

By running this code, you agree to use it **responsibly, ethically, and within the boundaries of all applicable laws and regulations**.

---

## Architecture & Code Quality

- **Modular structure**:
  - `main.py`: CLI interface and control flow.
  - `ip_lookup.py`: Public IP retrieval and geolocation lookups.
  - `port_scanner.py`: Educational port scanner.
  - `utils.py`: Validation, formatting, logging, and shared helpers.

- **Design principles**:
  - Separation of concerns between **logic** and **interface**.
  - Clear, function-based design.
  - Strong error handling and logging.
  - Adherence to **PEP 8** style guidelines.
  - No heavy frameworks; only minimal, well-known libraries.

This makes the codebase a good reference for building safe, maintainable networking tools in Python.


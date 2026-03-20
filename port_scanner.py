"""
Educational, controlled port scanner.

This module implements a deliberately simple, single-threaded TCP port
scanner for a small, fixed set of common ports. It is designed for
educational and defensive security training only, not for offensive use.
"""

from __future__ import annotations

import csv
import socket
import time
from datetime import datetime
from typing import Iterable, List, Optional

from utils import is_valid_ipv4, safe_get_logger

logger = safe_get_logger(__name__)

# The only hardcoded values: a small, fixed list of common ports.
COMMON_PORTS = [21, 22, 80, 443, 8080]

DEFAULT_TIMEOUT_SECONDS = 1.0
INTER_PORT_DELAY_SECONDS = 0.1  # Light rate limiting between port probes


def scan_common_ports(
    target_ip: str,
    ports: Optional[Iterable[int]] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    save_to_csv: bool = False,
) -> List[int]:
    """
    Scan a small, fixed set of TCP ports on a target IPv4 address.

    What is a port?
    ---------------
    A port is a 16-bit number that, together with an IP address, identifies
    a specific process or service on a host (for example, HTTP typically
    uses TCP port 80, HTTPS uses 443). Ports allow multiple networked
    applications to share a single IP address.

    What is a TCP connection?
    -------------------------
    Transmission Control Protocol (TCP) is a connection-oriented transport
    protocol. To establish a TCP connection, a client and server perform a
    three-way handshake:
      1. Client sends SYN
      2. Server replies with SYN-ACK if the port is listening
      3. Client sends ACK to confirm
    If the port is closed or filtered, this handshake fails.

    Scanner characteristics (defensive, not offensive):
    - Only scans a very small list of predefined ports.
    - Uses conservative timeouts (default 1 second).
    - Runs single-threaded with a small delay between each probe.
    - Intended for local lab environments and systems you own or manage.
    """
    target_ip = target_ip.strip()

    if not is_valid_ipv4(target_ip):
        logger.warning("Refused to scan invalid IPv4 address: %s", target_ip)
        return []

    ports_to_scan = list(ports) if ports is not None else list(COMMON_PORTS)
    open_ports: List[int] = []

    for port in ports_to_scan:
        if not isinstance(port, int) or port <= 0 or port > 65535:
            logger.debug("Skipping invalid port value: %s", port)
            continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
                logger.info("Port %s is open on %s", port, target_ip)
        except OSError as exc:
            logger.error("Socket error while scanning %s:%s - %s", target_ip, port, exc)
        finally:
            sock.close()

        # Gentle rate limiting between probes.
        time.sleep(INTER_PORT_DELAY_SECONDS)

    if save_to_csv:
        _save_scan_results_to_csv(target_ip, open_ports)

    return open_ports


def _save_scan_results_to_csv(target_ip: str, open_ports: List[int], path: str = "scan_results.csv") -> None:
    """
    Persist scan results to a CSV file for later analysis.

    The CSV contains:
    - Timestamp
    - Target IP
    - Comma-separated list of open ports
    """
    try:
        fieldnames = ["timestamp", "target_ip", "open_ports"]
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        open_ports_str = ",".join(str(p) for p in open_ports) if open_ports else ""

        try:
            file_exists = False
            try:
                with open(path, "r", encoding="utf-8") as _:
                    file_exists = True
            except FileNotFoundError:
                file_exists = False

            with open(path, "a", encoding="utf-8", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(
                    {
                        "timestamp": timestamp,
                        "target_ip": target_ip,
                        "open_ports": open_ports_str,
                    }
                )
        except OSError as exc:
            logger.error("Failed to write scan results to CSV: %s", exc)
    except Exception as exc:  # Defensive catch-all, should not normally trigger
        logger.error("Unexpected error saving CSV results: %s", exc)


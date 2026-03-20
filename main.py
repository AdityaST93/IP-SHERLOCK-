"""
IP Intelligence & Network Awareness Dashboard

Interactive CLI entrypoint that ties together:
- Public IP detection
- IP geolocation lookup
- Educational port scanning

The design deliberately separates business logic from user interface code:
the CLI handles input/output, while dedicated modules perform the
networking work.
"""

from __future__ import annotations

import sys

from ip_lookup import get_ip_geolocation, get_public_ip
from port_scanner import COMMON_PORTS, scan_common_ports
from utils import (
    color_text,
    configure_logging,
    format_key_value,
    format_section_title,
    is_valid_ipv4,
    print_disclaimer,
    prompt_yes_no,
)


def print_banner() -> None:
    """
    Display a simple branded banner for the dashboard.
    """
    title = "IP Intelligence & Network Awareness Dashboard"
    subtitle = "Educational Cybersecurity & Network Visibility Tool"
    print("=" * len(title))
    print(color_text(title, "bold"))
    print(color_text(subtitle, "cyan"))
    print("=" * len(title))


def detect_public_ip_flow() -> None:
    """
    CLI flow for public IP detection.
    """
    print(format_section_title("Public IP Detection"))

    ip = get_public_ip()
    if ip:
        print(format_key_value("Public IP", color_text(ip, "green")))
    else:
        print(
            color_text(
                "Unable to determine your public IP address. "
                "Please check your internet connection or try again later.",
                "red",
            )
        )


def lookup_ip_information_flow() -> None:
    """
    CLI flow for IP geolocation and metadata lookup.
    """
    print(format_section_title("IP Information Lookup"))
    ip = input("Enter an IPv4 address to look up: ").strip()

    if not is_valid_ipv4(ip):
        print(color_text("The value you entered is not a valid IPv4 address.", "red"))
        return

    info = get_ip_geolocation(ip)
    if not info:
        print(
            color_text(
                "No geolocation information could be retrieved for this IP.", "red"
            )
        )
        return

    print()
    print(color_text("Geolocation & Network Metadata", "bold"))
    print("-" * 40)

    # Mapping for display order and friendly labels
    display_order = [
        ("ip", "IP Address"),
        ("country", "Country"),
        ("region", "Region"),
        ("city", "City"),
        ("timezone", "Timezone"),
        ("latitude", "Latitude"),
        ("longitude", "Longitude"),
        ("isp", "ISP"),
        ("organization", "Organization"),
        ("asn", "ASN"),
    ]

    for key, label in display_order:
        value = info.get(key)
        if isinstance(value, (float, int)):
            value_str = f"{value}"
        else:
            value_str = value
        print(format_key_value(label, value_str))

    print()
    print(
        color_text(
            "Note: Geolocation data is approximate and may be inaccurate.",
            "yellow",
        )
    )


def scan_ports_flow() -> None:
    """
    CLI flow for controlled, educational port scanning.
    """
    print_disclaimer()
    if not prompt_yes_no("Do you understand and agree to these terms?"):
        print(color_text("Scan cancelled.", "yellow"))
        return

    print(format_section_title("Educational Port Scanner"))
    target_ip = input("Enter the IPv4 address you wish to scan: ").strip()

    if not is_valid_ipv4(target_ip):
        print(color_text("The value you entered is not a valid IPv4 address.", "red"))
        return

    print()
    print(
        color_text(
            f"Scanning the following common TCP ports on {target_ip}: {COMMON_PORTS}",
            "cyan",
        )
    )
    print(
        color_text(
            "This is a slow, single-threaded scan with conservative timeouts.",
            "yellow",
        )
    )

    save_to_csv = prompt_yes_no("Save scan results to scan_results.csv?")

    open_ports = scan_common_ports(
        target_ip=target_ip,
        ports=COMMON_PORTS,
        timeout=1.0,
        save_to_csv=save_to_csv,
    )

    print()
    if open_ports:
        print(color_text("Open ports detected:", "green"))
        for port in open_ports:
            print(f" - TCP {port}")
    else:
        print(color_text("No open ports were detected on the scanned set.", "yellow"))


def main() -> None:
    """
    Main interactive loop for the CLI dashboard.
    """
    configure_logging()
    print_banner()

    while True:
        print()
        print(color_text("Main Menu", "bold"))
        print("-" * 20)
        print("1) Detect my public IP")
        print("2) Lookup IP information")
        print("3) Scan common ports (educational)")
        print("4) Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            detect_public_ip_flow()
        elif choice == "2":
            lookup_ip_information_flow()
        elif choice == "3":
            scan_ports_flow()
        elif choice == "4":
            print(color_text("Exiting. Stay safe and scan responsibly.", "cyan"))
            break
        else:
            print(color_text("Invalid selection. Please choose 1, 2, 3, or 4.", "red"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + color_text("Interrupted by user. Goodbye.", "yellow"))
        sys.exit(0)


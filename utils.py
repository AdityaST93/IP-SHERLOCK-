"""
Utility helpers for the IP Intelligence & Network Awareness Dashboard.

This module centralizes input validation, console formatting, logging setup,
and reusable helper functions that are shared across the application.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

# --- Optional color support (colorama) ---------------------------------------

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except Exception:  # colorama not installed or failed to init
    COLOR_ENABLED = False

    class _Dummy:
        def __getattr__(self, _name: str) -> str:
            return ""

    Fore = Style = _Dummy()  # type: ignore


# --- Logging configuration ----------------------------------------------------


def configure_logging(log_file: str = "app.log") -> None:
    """
    Configure application-wide logging.

    Logs are helpful for educational purposes to show how network tools
    should record errors and events in a production-like environment.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


# --- Input validation ---------------------------------------------------------


_IPV4_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d{1,2})$"
)


def is_valid_ipv4(ip_address: str) -> bool:
    """
    Validate whether a string is a syntactically correct IPv4 address.

    What is an IP?
    --------------
    An Internet Protocol (IP) address is a numerical label assigned to each
    device connected to a computer network that uses the Internet Protocol
    for communication. It functions as both an identifier (who you are on
    the network) and a locator (where you are on the network).
    """
    if not isinstance(ip_address, str):
        return False
    ip_address = ip_address.strip()
    if not _IPV4_REGEX.match(ip_address):
        return False

    # Extra safety: ensure each octet is in 0–255, even if regex passes.
    try:
        return all(0 <= int(part) <= 255 for part in ip_address.split("."))
    except ValueError:
        return False


# --- Console formatting helpers ----------------------------------------------


def color_text(text: str, color: str) -> str:
    """
    Wrap text in ANSI color codes if color support is available.
    """
    if not COLOR_ENABLED:
        return text

    mapping = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "bold": Style.BRIGHT,
    }
    prefix = mapping.get(color.lower())
    if not prefix:
        return text
    return f"{prefix}{text}{Style.RESET_ALL}"


def format_section_title(title: str) -> str:
    """
    Create a visually distinct section title for CLI output.
    """
    border = "=" * len(title)
    return f"\n{color_text(border, 'cyan')}\n{color_text(title, 'bold')}\n{color_text(border, 'cyan')}"


def format_key_value(key: str, value: Optional[str]) -> str:
    """
    Nicely format a key/value pair for aligned CLI display.
    """
    key_display = f"{key}:".ljust(15)
    value_display = value if value is not None else "N/A"
    return f"{color_text(key_display, 'yellow')}{value_display}"


def print_disclaimer() -> None:
    """
    Print an ethical usage disclaimer for port scanning and network analysis.

    This reinforces that the tool is for defensive, educational, and
    permission-based use only.
    """
    message_lines = [
        "LEGAL & ETHICAL USAGE NOTICE",
        "",
        "This educational tool is intended strictly for defensive cybersecurity",
        "training and network awareness. Only scan systems that you own or for",
        "which you have received explicit, written permission to test.",
        "",
        "Unauthorized scanning of networks or systems may be illegal and is",
        "strictly prohibited. By continuing, you acknowledge that you will use",
        "this tool responsibly and in compliance with all applicable laws.",
    ]
    print(format_section_title("Disclaimer"))
    for line in message_lines:
        print(color_text(line, "red"))


def prompt_yes_no(prompt: str) -> bool:
    """
    Ask the user a yes/no question and return True for 'yes'.

    This function normalizes user input and keeps the CLI flow consistent.
    """
    while True:
        answer = input(f"{prompt} [y/n]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print(color_text("Please enter 'y' or 'n'.", "red"))


def safe_get_logger(name: str) -> logging.Logger:
    """
    Retrieve a logger with a given name, ensuring logging is configured.

    This helper ensures that even if configure_logging was not called yet,
    we still have a usable logger.
    """
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name)


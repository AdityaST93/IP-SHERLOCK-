"""
Public IP detection and IP geolocation lookup.

This module is responsible for:
- Discovering the user's current public IP address using a trusted API.
- Retrieving geolocation and network metadata for given IP addresses
  from a public geolocation API.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests

from utils import is_valid_ipv4, safe_get_logger

logger = safe_get_logger(__name__)

IPIFY_URL = "https://api.ipify.org?format=json"
IP_API_URL = "http://ip-api.com/json/"  # Free tier uses HTTP


def get_public_ip(timeout: float = 5.0) -> Optional[str]:
    """
    Detect the caller's public IP address via api.ipify.org.

    What is a public IP?
    --------------------
    A public IP address is the IP that is visible to other systems on the
    internet. It is usually assigned to your router or gateway by your
    Internet Service Provider (ISP) and is how external services see and
    reach your network.

    The function:
    - Uses HTTPS to query a minimal, privacy-conscious API.
    - Handles network timeouts and unexpected responses gracefully.
    """
    try:
        response = requests.get(IPIFY_URL, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        ip = data.get("ip")
        if ip and is_valid_ipv4(ip):
            return ip
        logger.warning("Received invalid IP from ipify response: %s", data)
        return None
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logger.error("Failed to retrieve public IP: %s", exc)
        return None


def get_ip_geolocation(ip_address: str, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
    """
    Retrieve geolocation and network metadata for an IPv4 address.

    What is a geolocation database?
    -------------------------------
    An IP geolocation database maps IP address ranges to approximate
    real-world locations and network owners, such as:
    - Country, region, and city
    - Latitude and longitude (approximate)
    - Internet Service Provider (ISP) and organization
    - Autonomous System Number (ASN), which identifies a routing domain

    Geolocation data is inherently approximate and may be inaccurate or
    outdated. It should not be used as the sole source of truth for
    security decisions.

    The function:
    - Validates IP format before querying the API.
    - Calls the free ip-api.com service for educational purposes.
    - Handles HTTP errors and invalid responses robustly.
    """
    ip_address = ip_address.strip()
    if not is_valid_ipv4(ip_address):
        logger.warning("Rejected invalid IPv4 address for geolocation: %s", ip_address)
        return None

    url = f"{IP_API_URL}{ip_address}"
    params = {
        "fields": (
            "status,message,country,regionName,city,isp,org,lat,lon,timezone,as,query"
        )
    }

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logger.error("Error querying IP geolocation API: %s", exc)
        return None

    if data.get("status") != "success":
        logger.info("Geolocation lookup failed: %s", data.get("message"))
        return None

    # Normalize important fields
    result = {
        "ip": data.get("query"),
        "country": data.get("country"),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "isp": data.get("isp"),
        "organization": data.get("org"),
        "latitude": data.get("lat"),
        "longitude": data.get("lon"),
        "timezone": data.get("timezone"),
        "asn": data.get("as"),
    }
    return result


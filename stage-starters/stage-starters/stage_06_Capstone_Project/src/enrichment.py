"""Enrichment module for SecureSIEM.

Enrichment adds context to findings by querying an external API.
Course implementation uses ip-api.com (free, no API key required).

We also:
- skip private/reserved IPs (no meaningful geolocation)
- cache results locally to reduce network calls and avoid rate limits
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict, List, Optional

from .cache import cache_get, cache_set
from .models import Finding


API_URL = "http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org"
TIMEOUT = 5  # seconds


def is_private_ip(ip: str) -> bool:
    """Return True if *ip* is in a common private/loopback range."""
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        first = int(parts[0])
        second = int(parts[1])
    except ValueError:
        return False

    if first == 10:
        return True
    if first == 172 and 16 <= second <= 31:
        return True
    if first == 192 and second == 168:
        return True
    if first == 127:
        return True
    return False


def get_ip_info(ip: str, use_cache: bool = True) -> Optional[Dict]:
    """Lookup geolocation/org details for an IP address."""
    if use_cache:
        cached = cache_get(f"geo:{ip}")
        if cached:
            return cached

    if is_private_ip(ip):
        return {"status": "private", "country": "Private Network"}

    try:
        url = API_URL.format(ip=ip)
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))

        if data.get("status") == "success":
            result = {
                "country": data.get("country", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "org": data.get("org", "Unknown"),
            }
            if use_cache:
                cache_set(f"geo:{ip}", result)
            return result
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        return None

    return None


def enrich_findings(findings: List[Finding]) -> List[Finding]:
    """Populate :attr:`~src.models.Finding.geo_info` for each finding."""
    unique_ips = {f.source_ip for f in findings}
    ip_info: Dict[str, Dict] = {}

    for ip in unique_ips:
        info = get_ip_info(ip)
        if info:
            ip_info[ip] = info

    for f in findings:
        if f.source_ip in ip_info:
            f.geo_info = ip_info[f.source_ip]
    return findings

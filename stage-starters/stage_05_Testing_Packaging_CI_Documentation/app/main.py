"""
Stage 05 - Testing, Packaging, CI, and Documentation.

Stage 05 carries forward the production-style CLI behavior from Stage 04 so we can focus on:
- writing unit tests (pytest)
- mocking external dependencies (network, filesystem, time)
- packaging with pyproject.toml
- CI with GitHub Actions
- professional documentation

Implements a production-style CLI that:
- Fetches data from public APIs (weather, currency)
- Uses timeouts and robust error handling on all network calls
- Caches responses to disk with TTL
- Integrates API data with a local JSON file

Standard library only (urllib). No API keys required by default.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# -----------------------------
# Paths / Defaults
# -----------------------------

APP_DIR = Path(__file__).resolve().parent
STAGE_DIR = APP_DIR.parent  # Stage_05_Testing_Packaging_CI_Documentation/
DATA_DIR = STAGE_DIR / "data"
CACHE_DIR = STAGE_DIR / ".cache"

DEFAULT_TIMEOUT_SECS = 10
DEFAULT_CACHE_TTL_SECS = 900  # 15 minutes


# -----------------------------
# Exceptions
# -----------------------------

class NetworkError(RuntimeError):
    pass


class APIError(RuntimeError):
    pass


class DataError(RuntimeError):
    pass


# -----------------------------
# Helpers
# -----------------------------

def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def now_ts() -> int:
    return int(time.time())


def clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DataError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataError(f"Invalid JSON in file: {path}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def http_get_json(url: str, *, timeout: int) -> Any:
    """GET JSON from URL with timeout + safe error handling."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "python-cybersecurity-learning-path-stage-05/1.0",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            raw = resp.read()
    except urllib.error.URLError as exc:
        raise NetworkError(f"Network error while calling API: {exc}") from exc
    except TimeoutError as exc:
        raise NetworkError("Network timeout while calling API") from exc

    if status != 200:
        raise APIError(f"API returned non-200 status: {status}")

    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise APIError("API returned invalid JSON") from exc


# -----------------------------
# Cache
# -----------------------------

@dataclass
class CacheResult:
    hit: bool
    path: Path
    age_seconds: Optional[int] = None


def cache_key_to_path(key: str) -> Path:
    safe = urllib.parse.quote(key, safe="")
    return CACHE_DIR / f"{safe}.json"


def cache_get(key: str, *, ttl: int) -> Tuple[CacheResult, Optional[Any]]:
    safe_mkdir(CACHE_DIR)
    path = cache_key_to_path(key)
    if not path.exists():
        return CacheResult(hit=False, path=path), None

    try:
        payload = read_json(path)
        ts = int(payload.get("_cached_at", 0))
        age = now_ts() - ts
    except Exception:  # noqa: BLE001
        return CacheResult(hit=False, path=path), None

    if ttl <= 0:
        return CacheResult(hit=False, path=path, age_seconds=age), None

    if age <= ttl:
        return CacheResult(hit=True, path=path, age_seconds=age), payload.get("data")

    return CacheResult(hit=False, path=path, age_seconds=age), None


def cache_set(key: str, data: Any) -> Path:
    safe_mkdir(CACHE_DIR)
    path = cache_key_to_path(key)
    payload = {"_cached_at": now_ts(), "data": data}
    write_json(path, payload)
    return path


def cache_status() -> Dict[str, Any]:
    safe_mkdir(CACHE_DIR)
    files = sorted(CACHE_DIR.glob("*.json"))
    total = 0
    newest = None
    oldest = None

    for f in files:
        total += 1
        try:
            payload = read_json(f)
            ts = int(payload.get("_cached_at", 0))
        except Exception:  # noqa: BLE001
            continue
        newest = ts if newest is None else max(newest, ts)
        oldest = ts if oldest is None else min(oldest, ts)

    return {
        "cache_dir": str(CACHE_DIR),
        "entries": total,
        "newest_cached_at": newest,
        "oldest_cached_at": oldest,
    }


def cache_clear() -> int:
    if not CACHE_DIR.exists():
        return 0
    count = 0
    for f in CACHE_DIR.glob("*.json"):
        try:
            f.unlink()
            count += 1
        except Exception:  # noqa: BLE001
            continue
    return count


# -----------------------------
# Geocoding / API Clients
# -----------------------------

def parse_latlon(text: str) -> Optional[Tuple[float, float]]:
    """
    Accepts: "47.6062,-122.3321" or "47.6062 -122.3321"
    """
    s = text.strip()
    if "," in s:
        parts = [p.strip() for p in s.split(",", 1)]
    else:
        parts = s.split()

    if len(parts) != 2:
        return None

    try:
        lat = float(parts[0])
        lon = float(parts[1])
    except ValueError:
        return None

    # Basic sanity bounds
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return None
    return lat, lon


def geocode_city_open_meteo(city: str, *, timeout: int) -> Optional[Tuple[float, float, str]]:
    """
    Primary geocoder: Open-Meteo geocoding endpoint.
    Returns None if no results.
    """
    q = urllib.parse.urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{q}"
    data = http_get_json(url, timeout=timeout)
    results = data.get("results") or []
    if not results:
        return None

    r0 = results[0]
    lat = float(r0["latitude"])
    lon = float(r0["longitude"])
    name = r0.get("name", city)
    admin1 = r0.get("admin1", "")
    country = r0.get("country", "")
    parts = [name]
    if admin1:
        parts.append(admin1)
    if country:
        parts.append(country)
    display = ", ".join(parts)
    return lat, lon, display


def normalize_us_location(raw: str) -> str:
    """
    Converts 'Seattle,WA' -> 'Seattle, Washington'
    If not recognized, returns input untouched (or lightly normalized).
    """
    us_states = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
        "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
        "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
        "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
        "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
        "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
        "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
    }
    s = raw.strip()
    if "," not in s:
        return s

    left, right = [p.strip() for p in s.split(",", 1)]
    st = right.upper()
    if st in us_states:
        return f"{left}, {us_states[st]}"
    return f"{left} {right}".strip()


def geocode_location(location: str, *, timeout: int) -> Tuple[float, float, str]:
    """
    Resolve a location string into lat/lon/display.

    Supports:
      - direct lat/lon: "47.6062,-122.3321"
      - place name via Open-Meteo geocoder
    """
    raw = location.strip()

    direct = parse_latlon(raw)
    if direct:
        lat, lon = direct
        return lat, lon, f"{lat},{lon}"

    # Open-Meteo geocoder (raw)
    res = geocode_city_open_meteo(raw, timeout=timeout)
    if res:
        return res

    # Try a US normalization attempt
    normalized = normalize_us_location(raw)
    if normalized != raw:
        res = geocode_city_open_meteo(normalized, timeout=timeout)
        if res:
            return res

    raise APIError(
        f"No geocoding results for location: {raw!r}. "
        f"Try 'Seattle', 'Seattle,WA', 'Seattle, Washington', or provide lat/lon like '47.6062,-122.3321'."
    )


def fetch_weather(location: str, *, timeout: int) -> Dict[str, Any]:
    lat, lon, display = geocode_location(location, timeout=timeout)

    q = urllib.parse.urlencode(
        {
            "latitude": f"{lat:.4f}",
            "longitude": f"{lon:.4f}",
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto",
        }
    )
    url = f"https://api.open-meteo.com/v1/forecast?{q}"
    data = http_get_json(url, timeout=timeout)

    current = data.get("current") or {}
    return {
        "source": "weather",
        "location_input": location,
        "location_resolved": display,
        "latitude": lat,
        "longitude": lon,
        "current": {
            "time": current.get("time"),
            "temperature_2m": current.get("temperature_2m"),
            "relative_humidity_2m": current.get("relative_humidity_2m"),
            "wind_speed_10m": current.get("wind_speed_10m"),
        },
    }


def fetch_currency(base: str, symbols: str, *, timeout: int) -> Dict[str, Any]:
    """
    Currency rates via Frankfurter (ECB reference rates, no API key).

    Example:
      https://api.frankfurter.app/latest?from=USD&to=EUR,JPY
    """
    base = base.upper().strip()
    symbols_clean = ",".join([s.strip().upper() for s in symbols.split(",") if s.strip()])

    if not base or not symbols_clean:
        raise DataError("Currency requires --base and --symbols (comma-separated).")

    q = urllib.parse.urlencode({"from": base, "to": symbols_clean})
    url = f"https://api.frankfurter.app/latest?{q}"

    data = http_get_json(url, timeout=timeout)

    rates = data.get("rates")
    if not isinstance(rates, dict) or not rates:
        raise APIError("Currency API response missing 'rates'.")

    return {
        "source": "currency",
        "base": data.get("base", base),
        "symbols": symbols_clean.split(","),
        "date": data.get("date"),
        "rates": rates,
    }


# -----------------------------
# Reporting
# -----------------------------

def print_report(payload: Dict[str, Any]) -> None:
    src = payload.get("source")

    if src == "weather":
        loc = payload.get("location_resolved") or payload.get("location_input")
        cur = payload.get("current", {})
        print(f"Weather Report: {loc}")
        print(f"  Time: {cur.get('time')}")
        print(f"  Temp (C): {cur.get('temperature_2m')}")
        print(f"  Humidity (%): {cur.get('relative_humidity_2m')}")
        print(f"  Wind (km/h): {cur.get('wind_speed_10m')}")
        return

    if src == "currency":
        base = payload.get("base")
        date = payload.get("date")
        print(f"Currency Report: base={base} date={date}")
        rates = payload.get("rates", {})
        for k in sorted(rates.keys()):
            print(f"  {k}: {rates[k]}")
        return

    print(json.dumps(payload, indent=2, ensure_ascii=False))


# -----------------------------
# Commands
# -----------------------------

def cmd_fetch(args: argparse.Namespace) -> int:
    timeout = clamp_int(args.timeout, 1, 60)
    ttl = clamp_int(args.cache_ttl, 0, 24 * 60 * 60)

    if args.source == "weather":
        if not args.location:
            eprint("ERROR: weather fetch requires --location.")
            return 2
        key = f"weather|loc={args.location}"
    else:
        key = f"currency|base={args.base}|symbols={args.symbols}"

    if not args.no_cache:
        meta, cached = cache_get(key, ttl=ttl)
        if meta.hit and cached is not None:
            if args.json:
                print(json.dumps(cached, indent=2, ensure_ascii=False))
            else:
                print_report(cached)
            return 0

    try:
        if args.source == "weather":
            data = fetch_weather(args.location, timeout=timeout)
        else:
            data = fetch_currency(args.base, args.symbols, timeout=timeout)
    except (NetworkError, APIError, DataError) as exc:
        eprint(f"ERROR: {exc}")
        return 2

    cache_set(key, data)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_report(data)

    return 0


def cmd_integrate(args: argparse.Namespace) -> int:
    timeout = clamp_int(args.timeout, 1, 60)
    ttl = clamp_int(args.cache_ttl, 0, 24 * 60 * 60)

    input_path = Path(args.input)
    out_path = Path(args.output)

    try:
        local = read_json(input_path)
    except DataError as exc:
        eprint(f"ERROR: {exc}")
        return 2

    try:
        if args.source == "currency":
            api_key = f"currency|base={args.base}|symbols={args.symbols}"
            cached = None
            if not args.no_cache:
                _, cached = cache_get(api_key, ttl=ttl)
            if cached is None:
                cached = fetch_currency(args.base, args.symbols, timeout=timeout)
                cache_set(api_key, cached)
            api_data = cached
        else:
            api_key = f"weather|loc={args.location}"
            cached = None
            if not args.no_cache:
                _, cached = cache_get(api_key, ttl=ttl)
            if cached is None:
                cached = fetch_weather(args.location, timeout=timeout)
                cache_set(api_key, cached)
            api_data = cached
    except (NetworkError, APIError, DataError) as exc:
        eprint(f"ERROR: {exc}")
        return 2

    merged = {
        "generated_at": now_ts(),
        "input_file": str(input_path),
        "api_snapshot": api_data,
        "local_data": local,
    }

    try:
        write_json(out_path, merged)
    except Exception as exc:  # noqa: BLE001
        eprint(f"ERROR: Failed writing output file: {out_path} ({exc})")
        return 2

    print(f"Wrote integrated report: {out_path}")
    return 0


def cmd_cache_status(_: argparse.Namespace) -> int:
    print(json.dumps(cache_status(), indent=2, ensure_ascii=False))
    return 0


def cmd_cache_clear(_: argparse.Namespace) -> int:
    n = cache_clear()
    print(f"Cleared {n} cache entr{'y' if n == 1 else 'ies'}.")
    return 0


# -----------------------------
# CLI
# -----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Stage 05 - Testing, Packaging, CI, and Documentation"
    )
    sub = p.add_subparsers(dest="command", required=True)

    # fetch
    fetch = sub.add_parser("fetch", help="Fetch API data and print a report")
    fetch.add_argument(
        "--source",
        choices=["weather", "currency"],
        required=True,
        help="API source to query",
    )
    fetch.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECS, help="HTTP timeout (seconds)")
    fetch.add_argument("--cache-ttl", type=int, default=DEFAULT_CACHE_TTL_SECS, help="Cache TTL (seconds)")
    fetch.add_argument("--no-cache", action="store_true", help="Ignore cache and force refresh")
    fetch.add_argument("--json", action="store_true", help="Output raw JSON instead of a formatted report")

    fetch.add_argument("--location", default="", help="Location string (weather), e.g., 'Seattle,WA' or '47.6062,-122.3321'")
    fetch.add_argument("--base", default="USD", help="Base currency (currency), e.g., USD")
    fetch.add_argument("--symbols", default="EUR,JPY", help="Comma-separated symbols (currency), e.g., EUR,JPY")

    fetch.set_defaults(func=cmd_fetch)

    # integrate
    integ = sub.add_parser("integrate", help="Merge API output with local JSON data")
    integ.add_argument("--input", required=True, help="Path to local JSON input (e.g., data/sample.json)")
    integ.add_argument("--output", required=True, help="Path to write merged output JSON (e.g., report.json)")
    integ.add_argument(
        "--source",
        choices=["weather", "currency"],
        default="weather",
        help="API source to include in the merged output",
    )
    integ.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECS, help="HTTP timeout (seconds)")
    integ.add_argument("--cache-ttl", type=int, default=DEFAULT_CACHE_TTL_SECS, help="Cache TTL (seconds)")
    integ.add_argument("--no-cache", action="store_true", help="Ignore cache and force refresh")

    integ.add_argument("--location", default="Seattle,WA", help="Location string (weather), or lat/lon like '47.6062,-122.3321'")
    integ.add_argument("--base", default="USD", help="Base currency (currency), e.g., USD")
    integ.add_argument("--symbols", default="EUR,JPY", help="Comma-separated symbols (currency), e.g., EUR,JPY")

    integ.set_defaults(func=cmd_integrate)

    # cache
    cache = sub.add_parser("cache", help="Cache utilities")
    cache_sub = cache.add_subparsers(dest="cache_cmd", required=True)

    cstat = cache_sub.add_parser("status", help="Show cache status")
    cstat.set_defaults(func=cmd_cache_status)

    cclr = cache_sub.add_parser("clear", help="Clear cache entries")
    cclr.set_defaults(func=cmd_cache_clear)

    return p


def main(argv: list[str] | None = None) -> int:
    
    if argv is None:
        import sys as _sys
        argv = _sys.argv[1:]

    parser = build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse already printed the error/usage to stderr.
        # Convert to an integer exit code instead of crashing tests.
        code = e.code
        return int(code) if isinstance(code, int) else 2

    func = getattr(args, "func", None)
    if func is None:
        eprint("ERROR: No command selected. Use --help.")
        return 1

    return int(func(args))

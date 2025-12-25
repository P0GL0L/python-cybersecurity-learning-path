"""File-based caching for SecureSIEM.

Caching is used to reduce repeated API calls for enrichment (e.g., IP geolocation)
and avoid rate limiting.

Implementation notes:
- Cache stored under ~/.securesiem/cache by default
- Each key becomes a JSON file containing:
    - _cached_at (epoch seconds)
    - value (JSON-serializable payload)
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Optional


DEFAULT_TTL = 86400  # 24 hours (seconds)


def _default_cache_dir() -> Path:
    # Allow override for testing / portability.
    env = os.getenv("SECURESIEM_CACHE_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".securesiem" / "cache"


def ensure_cache_dir(cache_dir: Optional[Path] = None) -> Path:
    """Create cache directory if needed and return it."""
    d = cache_dir or _default_cache_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_cache_path(key: str, cache_dir: Optional[Path] = None) -> Path:
    """Map a cache key to a safe filename."""
    safe_key = key.replace(":", "_").replace("/", "_")
    return ensure_cache_dir(cache_dir) / f"{safe_key}.json"


def cache_get(key: str, ttl: int = DEFAULT_TTL, cache_dir: Optional[Path] = None) -> Optional[Any]:
    """Return cached value if present and not expired; else None."""
    p = get_cache_path(key, cache_dir=cache_dir)
    if not p.exists():
        return None

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        cached_at = float(data.get("_cached_at", 0))
        if (time.time() - cached_at) > ttl:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass
            return None
        return data.get("value")
    except Exception:
        return None


def cache_set(key: str, value: Any, cache_dir: Optional[Path] = None) -> bool:
    """Store *value* under *key*. Value must be JSON-serializable."""
    p = get_cache_path(key, cache_dir=cache_dir)
    try:
        payload = {"_cached_at": time.time(), "value": value}
        p.write_text(json.dumps(payload), encoding="utf-8")
        return True
    except Exception:
        return False


def cache_clear(cache_dir: Optional[Path] = None) -> int:
    """Delete all cached files. Returns number of files removed."""
    d = ensure_cache_dir(cache_dir)
    removed = 0
    for f in d.glob("*.json"):
        try:
            f.unlink(missing_ok=True)
            removed += 1
        except Exception:
            pass
    return removed

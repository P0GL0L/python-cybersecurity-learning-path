import os
import time
from pathlib import Path

from src.cache import cache_set, cache_get, cache_clear


def test_cache_set_and_get(tmp_path, monkeypatch):
    monkeypatch.setenv("SECURESIEM_CACHE_DIR", str(tmp_path))
    assert cache_set("geo:1.2.3.4", {"country": "X"})
    assert cache_get("geo:1.2.3.4") == {"country": "X"}


def test_cache_ttl_expiry(tmp_path, monkeypatch):
    monkeypatch.setenv("SECURESIEM_CACHE_DIR", str(tmp_path))
    cache_set("geo:1.2.3.4", {"country": "X"})
    # TTL=0 should force expiry
    assert cache_get("geo:1.2.3.4", ttl=0) is None


def test_cache_clear(tmp_path, monkeypatch):
    monkeypatch.setenv("SECURESIEM_CACHE_DIR", str(tmp_path))
    cache_set("geo:1.2.3.4", {"country": "X"})
    removed = cache_clear()
    assert removed >= 1

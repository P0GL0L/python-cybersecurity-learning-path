import json
from types import SimpleNamespace

from src.enrichment import get_ip_info, is_private_ip


class DummyResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_is_private_ip():
    assert is_private_ip("10.0.0.1")
    assert is_private_ip("192.168.1.2")
    assert is_private_ip("172.16.0.5")
    assert not is_private_ip("8.8.8.8")


def test_get_ip_info_private(monkeypatch, tmp_path):
    monkeypatch.setenv("SECURESIEM_CACHE_DIR", str(tmp_path))
    info = get_ip_info("192.168.1.2", use_cache=True)
    assert info is not None
    assert info["country"] == "Private Network"


def test_get_ip_info_success(monkeypatch, tmp_path):
    monkeypatch.setenv("SECURESIEM_CACHE_DIR", str(tmp_path))

    def fake_urlopen(url, timeout=5):
        return DummyResponse({
            "status": "success",
            "country": "Testland",
            "regionName": "Region",
            "city": "City",
            "isp": "ISP",
            "org": "ORG",
        })

    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    info = get_ip_info("8.8.8.8", use_cache=False)
    assert info["country"] == "Testland"

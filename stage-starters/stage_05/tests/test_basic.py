import json
import types
import urllib.error

import pytest

import app.main as m


# -------------------------
# Basic CLI behavior
# -------------------------

def test_main_returns_0_on_fetch_cached_hit(monkeypatch, capsys):
    # Prevent required subparser error by running a real command.
    # Provide cached hit and ensure no network occurs.
    monkeypatch.setattr(m, "cache_get", lambda key, ttl: (m.CacheResult(hit=True, path=m.Path("x"), age_seconds=1), {"source": "currency", "base": "USD", "date": "2020-01-01", "rates": {"EUR": 1.1}}))
    monkeypatch.setattr(m, "cache_set", lambda key, data: None)

    # If fetch_currency were called, test should fail.
    def _boom(*args, **kwargs):
        raise AssertionError("Network path executed unexpectedly")
    monkeypatch.setattr(m, "fetch_currency", _boom)

    rc = m.main(["fetch", "--source", "currency", "--base", "USD", "--symbols", "EUR"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Currency Report" in out


def test_build_parser_requires_command():
    p = m.build_parser()
    with pytest.raises(SystemExit) as excinfo:
        p.parse_args([])
    assert excinfo.value.code == 2


# -------------------------
# Pure helpers
# -------------------------

def test_clamp_int_bounds():
    assert m.clamp_int(0, 1, 10) == 1
    assert m.clamp_int(50, 1, 10) == 10
    assert m.clamp_int(5, 1, 10) == 5


def test_parse_latlon_valid_comma():
    assert m.parse_latlon("47.6062,-122.3321") == (47.6062, -122.3321)


def test_parse_latlon_valid_space():
    assert m.parse_latlon("47.6062 -122.3321") == (47.6062, -122.3321)


def test_parse_latlon_invalid():
    assert m.parse_latlon("hello world") is None
    assert m.parse_latlon("91,0") is None
    assert m.parse_latlon("0,181") is None


def test_normalize_us_location_state_abbrev():
    assert m.normalize_us_location("Seattle,WA") == "Seattle, Washington"


# -------------------------
# Currency input validation
# -------------------------

def test_fetch_currency_requires_base_and_symbols():
    with pytest.raises(m.DataError):
        m.fetch_currency("", "", timeout=5)
    with pytest.raises(m.DataError):
        m.fetch_currency("USD", "", timeout=5)


def test_fetch_currency_uppercases_and_strips(monkeypatch):
    # Avoid live network: stub http_get_json
    def fake_http(url, timeout):
        return {"base": "USD", "date": "2020-01-01", "rates": {"EUR": 1.23}}
    monkeypatch.setattr(m, "http_get_json", fake_http)

    payload = m.fetch_currency(" usd ", " eur , jpy ", timeout=5)
    assert payload["source"] == "currency"
    assert payload["base"] == "USD"
    assert payload["symbols"] == ["EUR", "JPY"]
    assert "rates" in payload


def test_fetch_currency_missing_rates_raises(monkeypatch):
    monkeypatch.setattr(m, "http_get_json", lambda url, timeout: {"base": "USD", "date": "2020-01-01"})
    with pytest.raises(m.APIError):
        m.fetch_currency("USD", "EUR", timeout=5)


# -------------------------
# http_get_json network mocking
# -------------------------

class _DummyResp:
    def __init__(self, status, body_bytes):
        self.status = status
        self._body = body_bytes

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_http_get_json_success(monkeypatch):
    body = json.dumps({"ok": True}).encode("utf-8")
    monkeypatch.setattr(m.urllib.request, "urlopen", lambda req, timeout: _DummyResp(200, body))
    assert m.http_get_json("https://example.test", timeout=5) == {"ok": True}


def test_http_get_json_non_200_raises(monkeypatch):
    body = json.dumps({"ok": True}).encode("utf-8")
    monkeypatch.setattr(m.urllib.request, "urlopen", lambda req, timeout: _DummyResp(404, body))
    with pytest.raises(m.APIError):
        m.http_get_json("https://example.test", timeout=5)


def test_http_get_json_invalid_json_raises(monkeypatch):
    monkeypatch.setattr(m.urllib.request, "urlopen", lambda req, timeout: _DummyResp(200, b"not-json"))
    with pytest.raises(m.APIError):
        m.http_get_json("https://example.test", timeout=5)


def test_http_get_json_urlerror_raises(monkeypatch):
    def boom(req, timeout):
        raise urllib.error.URLError("nope")
    monkeypatch.setattr(m.urllib.request, "urlopen", boom)
    with pytest.raises(m.NetworkError):
        m.http_get_json("https://example.test", timeout=5)


# -------------------------
# Cache (no real disk outside tmp_path)
# -------------------------

def test_cache_set_and_get_hit(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)

    # Freeze time
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    key = "currency|base=USD|symbols=EUR"
    data = {"hello": "world"}
    m.cache_set(key, data)

    res, cached = m.cache_get(key, ttl=900)
    assert res.hit is True
    assert cached == data
    assert res.age_seconds == 0


def test_cache_get_expired(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)

    # Write at t=1000
    monkeypatch.setattr(m, "now_ts", lambda: 1000)
    key = "weather|loc=Seattle"
    m.cache_set(key, {"x": 1})

    # Read at t=2000 with ttl=100 -> expired
    monkeypatch.setattr(m, "now_ts", lambda: 2000)
    res, cached = m.cache_get(key, ttl=100)
    assert res.hit is False
    assert cached is None
    assert res.age_seconds == 1000


# -------------------------
# Command error path (no network)
# -------------------------

def test_cmd_fetch_weather_requires_location(monkeypatch, capsys):
    ns = types.SimpleNamespace(
        source="weather",
        location="",
        base="USD",
        symbols="EUR",
        timeout=5,
        cache_ttl=0,
        no_cache=True,
        json=False,
    )
    rc = m.cmd_fetch(ns)
    err = capsys.readouterr().err
    assert rc == 2
    assert "requires --location" in err

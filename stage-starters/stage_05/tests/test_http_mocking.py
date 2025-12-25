import pytest
import app.main as m


def test_fetch_currency_success_monkeypatch(monkeypatch):
    def fake_http(url: str, *, timeout: int):
        # Minimal valid Frankfurter-like shape
        return {"base": "USD", "date": "2025-01-01", "rates": {"EUR": 0.92, "JPY": 150.0}}

    monkeypatch.setattr(m, "http_get_json", fake_http)

    result = m.fetch_currency("USD", "EUR,JPY", timeout=5)
    assert result["source"] == "currency"
    assert result["base"] == "USD"
    assert "EUR" in result["rates"]
    assert result["rates"]["EUR"] == 0.92


def test_fetch_currency_requires_base_and_symbols():
    with pytest.raises(m.DataError):
        m.fetch_currency("", "EUR", timeout=5)
    with pytest.raises(m.DataError):
        m.fetch_currency("USD", "", timeout=5)


def test_fetch_currency_missing_rates_is_apierror(monkeypatch):
    def fake_http(url: str, *, timeout: int):
        return {"base": "USD", "date": "2025-01-01", "rates": {}}

    monkeypatch.setattr(m, "http_get_json", fake_http)

    with pytest.raises(m.APIError):
        m.fetch_currency("USD", "EUR", timeout=5)


def test_geocode_city_open_meteo_no_results(monkeypatch):
    def fake_http(url: str, *, timeout: int):
        return {"results": []}

    monkeypatch.setattr(m, "http_get_json", fake_http)

    assert m.geocode_city_open_meteo("NowhereTown", timeout=5) is None


def test_geocode_location_direct_latlon_skips_network(monkeypatch):
    called = {"count": 0}

    def fake_geocode(*args, **kwargs):
        called["count"] += 1
        return (0.0, 0.0, "bad")

    monkeypatch.setattr(m, "geocode_city_open_meteo", fake_geocode)

    lat, lon, display = m.geocode_location("47.6,-122.3", timeout=5)
    assert (lat, lon) == (47.6, -122.3)
    assert display == "47.6,-122.3"
    assert called["count"] == 0  # no network geocode attempted


def test_fetch_weather_success_monkeypatch(monkeypatch):
    # Avoid any real geocode/http calls
    monkeypatch.setattr(m, "geocode_location", lambda location, *, timeout: (47.6, -122.3, "Seattle, WA"))

    def fake_http(url: str, *, timeout: int):
        return {
            "current": {
                "time": "2025-01-01T00:00",
                "temperature_2m": 10.5,
                "relative_humidity_2m": 80,
                "wind_speed_10m": 12.3,
            }
        }

    monkeypatch.setattr(m, "http_get_json", fake_http)

    result = m.fetch_weather("Seattle,WA", timeout=5)
    assert result["source"] == "weather"
    assert result["location_resolved"] == "Seattle, WA"
    assert result["current"]["temperature_2m"] == 10.5

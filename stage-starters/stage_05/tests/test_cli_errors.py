import json
import app.main as m


def test_main_no_command_returns_error(capsys):
    code = m.main([])
    captured = capsys.readouterr()
    assert code != 0
    assert "ERROR" in captured.err or "usage" in captured.err.lower() or "help" in captured.err.lower()


def test_fetch_weather_missing_location_returns_error(capsys):
    code = m.main(["fetch", "--source", "weather"])
    captured = capsys.readouterr()
    assert code == 2
    assert "requires --location" in captured.err


def test_fetch_currency_missing_symbols_returns_error(capsys):
    code = m.main(["fetch", "--source", "currency", "--base", "USD", "--symbols", ""])
    captured = capsys.readouterr()
    assert code == 2
    assert "Currency requires" in captured.err


def test_fetch_uses_cache_hit_and_does_not_call_network(tmp_path, monkeypatch, capsys):
    # Isolate cache
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    # Seed cache with a weather payload
    cached_payload = {
        "source": "weather",
        "location_input": "Seattle,WA",
        "location_resolved": "Seattle, WA",
        "latitude": 47.6,
        "longitude": -122.3,
        "current": {"time": "x", "temperature_2m": 10, "relative_humidity_2m": 50, "wind_speed_10m": 5},
    }
    m.cache_set("weather|loc=Seattle,WA", cached_payload)

    # If fetch_weather is called, fail the test
    monkeypatch.setattr(m, "fetch_weather", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network called")))

    code = m.main(["fetch", "--source", "weather", "--location", "Seattle,WA", "--cache-ttl", "900"])
    assert code == 0

    out = capsys.readouterr().out
    assert "Weather Report" in out


def test_cache_status_command_outputs_json(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    m.cache_set("k1", {"a": 1})

    code = m.main(["cache", "status"])
    assert code == 0

    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert payload["entries"] == 1
    assert "cache_dir" in payload

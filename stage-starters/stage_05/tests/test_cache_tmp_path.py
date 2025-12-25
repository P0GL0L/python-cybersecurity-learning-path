import app.main as m


def test_cache_set_and_get_hit(tmp_path, monkeypatch):
    # Isolate cache dir to temp folder
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    m.cache_set("k1", {"hello": "world"})

    meta, data = m.cache_get("k1", ttl=900)
    assert meta.hit is True
    assert meta.age_seconds == 0
    assert data == {"hello": "world"}


def test_cache_get_miss_when_expired(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)

    # Cache was written at ts=1000, but "now" is 2000, TTL=100 => expired
    monkeypatch.setattr(m, "now_ts", lambda: 1000)
    m.cache_set("k2", {"a": 1})

    monkeypatch.setattr(m, "now_ts", lambda: 2000)
    meta, data = m.cache_get("k2", ttl=100)
    assert meta.hit is False
    assert data is None
    assert meta.age_seconds == 1000


def test_cache_ttl_zero_forces_refresh(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)
    m.cache_set("k3", {"a": 1})

    meta, data = m.cache_get("k3", ttl=0)
    assert meta.hit is False
    assert data is None


def test_cache_clear_removes_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    m.cache_set("k4", {"x": 1})
    m.cache_set("k5", {"y": 2})

    cleared = m.cache_clear()
    assert cleared == 2

    # Now nothing should exist
    assert list(tmp_path.glob("*.json")) == []


def test_cache_status_counts_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    m.cache_set("k6", {"x": 1})
    monkeypatch.setattr(m, "now_ts", lambda: 2000)
    m.cache_set("k7", {"y": 2})

    status = m.cache_status()
    assert status["entries"] == 2
    assert status["newest_cached_at"] == 2000
    assert status["oldest_cached_at"] == 1000

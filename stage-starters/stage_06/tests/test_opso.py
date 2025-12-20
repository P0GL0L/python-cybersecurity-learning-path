import json
from pathlib import Path

import pytest

import app.main as m


def test_build_parser_requires_command():
    p = m.build_parser()
    with pytest.raises(SystemExit) as excinfo:
        p.parse_args([])
    assert excinfo.value.code == 2


def test_ingest_records_requires_list(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text('{"id":1}', encoding="utf-8")
    with pytest.raises(ValueError, match="must be a list"):
        m.ingest_records(p)


def test_ingest_records_file_not_found(tmp_path: Path):
    p = tmp_path / "missing.json"
    with pytest.raises(ValueError, match="not found"):
        m.ingest_records(p)


def test_ingest_records_invalid_json(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text("{not-json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        m.ingest_records(p)


def test_enrich_records_counts_and_totals():
    records = [
        {"id": 1, "name": "alpha", "value": 10},
        {"id": 2, "name": "bravo", "value": 15},
        {"id": 3, "name": "alpha", "value": 7},
    ]
    enriched = m.enrich_records(records)
    assert enriched["record_count"] == 3
    assert enriched["groups"]["alpha"]["count"] == 2
    assert enriched["groups"]["alpha"]["total_value"] == 17
    assert enriched["groups"]["bravo"]["count"] == 1
    assert enriched["groups"]["bravo"]["total_value"] == 15


def test_print_report_contains_expected_text(capsys):
    enriched = {
        "record_count": 2,
        "groups": {"alpha": {"count": 2, "total_value": 17}},
    }
    m.print_report(enriched)
    out = capsys.readouterr().out
    assert "OpsOps Report" in out
    assert "Total records: 2" in out
    assert "Group: alpha" in out
    assert "Total Value: 17" in out


def test_cmd_run_json_output(tmp_path: Path, capsys):
    inp = tmp_path / "in.json"
    inp.write_text(json.dumps([{"name": "x", "value": 3}]), encoding="utf-8")

    ns = type("Args", (), {"input": str(inp), "output": None, "json": True})
    rc = m.cmd_run(ns)
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["record_count"] == 1
    assert payload["groups"]["x"]["total_value"] == 3


def test_cmd_run_writes_output_file(tmp_path: Path):
    inp = tmp_path / "in.json"
    outp = tmp_path / "out.json"
    inp.write_text(json.dumps([{"name": "x", "value": 3}]), encoding="utf-8")

    ns = type("Args", (), {"input": str(inp), "output": str(outp), "json": True})
    rc = m.cmd_run(ns)
    assert rc == 0
    written = json.loads(outp.read_text(encoding="utf-8"))
    assert written["record_count"] == 1


def test_main_run_smoke(tmp_path: Path, capsys):
    inp = tmp_path / "in.json"
    inp.write_text(json.dumps([{"name": "alpha", "value": 1}]), encoding="utf-8")
    rc = m.main(["run", "--input", str(inp), "--json"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"record_count": 1' in out


def test_demo_uses_sample_json(monkeypatch, capsys, tmp_path: Path):
    monkeypatch.setattr(m, "DATA_DIR", tmp_path)
    (tmp_path / "sample.json").write_text(json.dumps([{"name": "alpha", "value": 2}]), encoding="utf-8")
    rc = m.main(["demo"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "OpsOps Report" in out

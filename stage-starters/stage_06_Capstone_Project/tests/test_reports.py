import json
from datetime import datetime

from src.models import AnalysisReport, Finding, Severity


def test_save_json_report(tmp_path):
    f = Finding(rule_name="test", severity=Severity.LOW, source_ip="1.2.3.4", description="x")
    report = AnalysisReport(total_entries=1, findings=[f], summary={"low": 1}, analysis_time=datetime(2025, 1, 1))
    out = tmp_path / "report.json"

    from src.reports import save_json_report

    save_json_report(report, str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["total_entries_analyzed"] == 1
    assert data["findings"][0]["rule_name"] == "test"

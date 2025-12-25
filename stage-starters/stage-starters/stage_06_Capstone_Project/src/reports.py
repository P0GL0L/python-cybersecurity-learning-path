"""Report generation for SecureSIEM.

Outputs:
- Human-readable console report
- JSON report (machine readable)
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import List

from .models import AnalysisReport, Finding, LogEntry


def print_findings(findings: List[Finding]) -> None:
    """Print findings in a readable console format."""
    if not findings:
        print("\n[OK] No security threats detected!")
        return

    print("\n" + "=" * 60)
    print("SECURITY ANALYSIS REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Findings: {len(findings)}")
    print("-" * 60)

    severity_icons = {
        "critical": "[CRITICAL]",
        "high": "[HIGH]",
        "medium": "[MEDIUM]",
        "low": "[LOW]",
    }

    for i, finding in enumerate(findings, 1):
        icon = severity_icons.get(finding.severity.value, "[?]")
        print(f"\n{icon} Finding #{i}: {finding.rule_name.upper()}")
        print(f"   Source IP: {finding.source_ip}")
        print(f"   Description: {finding.description}")

        if finding.geo_info:
            geo = finding.geo_info
            loc = f"{geo.get('city', '?')}, {geo.get('country', '?')}"
            print(f"   Location: {loc}")

        if finding.evidence:
            print(f"   Evidence ({len(finding.evidence)} entries):")
            for entry in finding.evidence[:3]:
                line = entry.raw_line
                if len(line) > 90:
                    line = line[:90] + "..."
                print(f"      - {line}")

    print("\n" + "=" * 60)


def print_summary(entries: List[LogEntry]) -> None:
    """Print quick stats about the parsed file."""
    print("\n" + "=" * 40)
    print("LOG FILE SUMMARY")
    print("=" * 40)
    print(f"Total Entries: {len(entries)}")

    type_counts = {}
    for e in entries:
        t = e.log_type.value
        type_counts[t] = type_counts.get(t, 0) + 1

    print("\nBy Log Type:")
    for t, c in sorted(type_counts.items(), key=lambda kv: kv[0]):
        print(f"  {t}: {c}")

    unique_ips = {e.source_ip for e in entries}
    print(f"\nUnique IPs: {len(unique_ips)}")
    print("=" * 40)


def finding_to_dict(f: Finding) -> dict:
    """Convert a Finding to a JSON-serializable dict."""
    return {
        "rule_name": f.rule_name,
        "severity": f.severity.value,
        "source_ip": f.source_ip,
        "description": f.description,
        "evidence_count": len(f.evidence),
        "geo_info": f.geo_info,
    }


def save_json_report(report: AnalysisReport, filepath: str) -> None:
    """Write analysis report to JSON."""
    payload = {
        "generated_at": report.analysis_time.isoformat(),
        "total_entries_analyzed": report.total_entries,
        "summary": report.summary,
        "findings": [finding_to_dict(f) for f in report.findings],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

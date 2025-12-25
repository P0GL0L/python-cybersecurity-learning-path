"""Main entry point for SecureSIEM.

This module coordinates parsing, detection, enrichment, and reporting.

Run (from stage_06 folder):
- python -m src.main --help
- python -m src.main analyze --input data/sample_apache.log --verbose
"""

from __future__ import annotations

import sys
from datetime import datetime

from .cli import parse_args, validate_input_file
from .detection import run_all_detections
from .log_parser import parse_file_to_list
from .models import AnalysisReport
from .reports import print_findings, print_summary, save_json_report


def cmd_analyze(args) -> None:
    input_path = validate_input_file(args.input)

    if args.verbose:
        print(f"Analyzing: {input_path}")

    entries = parse_file_to_list(str(input_path))

    if args.verbose:
        print(f"Parsed {len(entries)} log entries")

    findings = run_all_detections(entries)

    if args.verbose:
        print(f"Found {len(findings)} security findings")

    if args.enrich:
        from .enrichment import enrich_findings

        findings = enrich_findings(findings)

    summary = {
        "critical": sum(1 for f in findings if f.severity.value == "critical"),
        "high": sum(1 for f in findings if f.severity.value == "high"),
        "medium": sum(1 for f in findings if f.severity.value == "medium"),
        "low": sum(1 for f in findings if f.severity.value == "low"),
    }

    report = AnalysisReport(
        total_entries=len(entries),
        findings=findings,
        summary=summary,
        analysis_time=datetime.now(),
    )

    print_findings(findings)

    if args.output:
        save_json_report(report, args.output)
        print(f"\nReport saved to: {args.output}")


def cmd_summary(args) -> None:
    input_path = validate_input_file(args.input)
    entries = parse_file_to_list(str(input_path))
    print_summary(entries)


def cmd_cache_clear(args) -> None:
    from .cache import cache_clear

    if not getattr(args, "yes", False):
        ans = input("This will delete all cached enrichment data. Continue? (y/N): ").strip().lower()
        if ans not in {"y", "yes"}:
            print("Cancelled.")
            return
    removed = cache_clear()
    print(f"Cache cleared. Removed {removed} file(s).")


def main() -> None:
    args = parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "summary":
        cmd_summary(args)
    elif args.command == "cache-clear":
        cmd_cache_clear(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

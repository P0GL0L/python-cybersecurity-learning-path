"""Command-line interface (CLI) for SecureSIEM.

Implements subcommands:
- analyze: analyze a log file, run detections, optionally enrich, output report
- summary: quick stats about a log file
- cache-clear: clear local enrichment cache (optional quality-of-life)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="securesiem",
        description="SecureSIEM - Security Log Analyzer",
        epilog="Example: securesiem analyze --input data/sample_apache.log --enrich --output report.json",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    analyze = subparsers.add_parser("analyze", help="Analyze a log file for threats")
    analyze.add_argument("--input", "-i", required=True, help="Path to log file to analyze")
    analyze.add_argument("--output", "-o", help="Path to save JSON report (optional)")
    analyze.add_argument("--enrich", action="store_true", help="Enrich findings with geolocation data")
    analyze.add_argument("--verbose", "-v", action="store_true", help="Show extra progress output")

    summary = subparsers.add_parser("summary", help="Show a quick summary of a log file")
    summary.add_argument("--input", "-i", required=True, help="Path to log file")

    cache_clear = subparsers.add_parser("cache-clear", help="Clear local enrichment cache")
    cache_clear.add_argument("--yes", action="store_true", help="Skip confirmation prompt")

    return parser


def validate_input_file(filepath: str) -> Path:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        raise SystemExit(1)
    if not path.is_file():
        print(f"Error: Not a file: {filepath}", file=sys.stderr)
        raise SystemExit(1)
    return path


def parse_args(args=None) -> argparse.Namespace:
    parser = create_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        raise SystemExit(0)

    return parsed

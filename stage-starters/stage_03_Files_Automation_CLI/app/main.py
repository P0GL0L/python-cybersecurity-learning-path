
"""
Stage 03 - Log Analyzer
A professional CLI tool that reads a log file, summarizes events, and optionally exports a JSON report.

Log format expected (per line):
YYYY-MM-DD HH:MM:SS LEVEL message...

Example:
2024-01-15 08:00:00 INFO Application started
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


# -----------------------------
# Exit codes (professional CLI)
# -----------------------------
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INPUT_ERROR = 2
EXIT_OUTPUT_ERROR = 3


# -----------------------------
# Data model
# -----------------------------
@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    level: str
    message: str


# -----------------------------
# CLI
# -----------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a log file and summarize entries by level (INFO/WARNING/ERROR)."
    )

    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input log file to analyze (e.g., data/sample.log)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Optional JSON output file (e.g., output/report.json)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    return parser.parse_args()


# -----------------------------
# Parsing + analysis
# -----------------------------
def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single log line.

    Expected format:
      DATE TIME LEVEL MESSAGE...
    where we split into at most 4 parts:
      [0]=date [1]=time [2]=level [3]=message

    Returns LogEntry if valid, otherwise None for blank/malformed lines.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split(" ", 3)
    if len(parts) < 4:
        return None

    date_part, time_part, level, message = parts[0], parts[1], parts[2], parts[3]
    timestamp = f"{date_part} {time_part}"

    return LogEntry(timestamp=timestamp, level=level, message=message)


def analyze_log_file(path: Path, verbose: bool = False) -> dict:
    """
    Analyze the log file and return a report dictionary that can be printed and/or exported to JSON.
    """
    level_counts: Counter[str] = Counter()
    total_lines = 0
    parsed_lines = 0
    invalid_lines = 0
    first_timestamp: Optional[str] = None
    last_timestamp: Optional[str] = None

    # Read safely with explicit encoding; replace decode errors rather than crashing.
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for raw_line in f:
                total_lines += 1
                entry = parse_log_line(raw_line)
                if entry is None:
                    invalid_lines += 1
                    continue

                parsed_lines += 1
                level_counts[entry.level] += 1

                if first_timestamp is None:
                    first_timestamp = entry.timestamp
                last_timestamp = entry.timestamp
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}") from None
    except PermissionError:
        raise PermissionError(f"No permission to read: {path}") from None

    if verbose:
        print(f"[verbose] Read {total_lines} lines from: {path}")

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_file": str(path),
        "summary": {
            "total_lines": total_lines,
            "parsed_lines": parsed_lines,
            "invalid_lines": invalid_lines,
            "first_timestamp": first_timestamp,
            "last_timestamp": last_timestamp,
        },
        "counts_by_level": dict(level_counts),
    }

    return report


# -----------------------------
# Output helpers
# -----------------------------
def print_summary(report: dict) -> None:
    summary = report.get("summary", {})
    counts = report.get("counts_by_level", {})

    print("=== Log Analyzer Summary ===")
    print(f"Input file: {report.get('input_file')}")
    print(f"Generated:  {report.get('generated_at')}")
    print()
    print(f"Total lines:   {summary.get('total_lines', 0)}")
    print(f"Parsed lines:  {summary.get('parsed_lines', 0)}")
    print(f"Invalid lines: {summary.get('invalid_lines', 0)}")
    print(f"First ts:      {summary.get('first_timestamp')}")
    print(f"Last ts:       {summary.get('last_timestamp')}")
    print()
    print("Counts by level:")
    if counts:
        for level, count in sorted(counts.items()):
            print(f"  {level}: {count}")
    else:
        print("  (no valid entries parsed)")


def write_json_report(output_path: Path, report: dict, verbose: bool = False) -> None:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    except PermissionError:
        raise PermissionError(f"No permission to write: {output_path}") from None
    except OSError as e:
        raise OSError(f"Failed to write output file {output_path}: {e}") from None

    if verbose:
        print(f"[verbose] Wrote JSON report to: {output_path}")


# -----------------------------
# Main
# -----------------------------
def main() -> int:
    args = parse_args()

    input_path: Path = args.input
    output_path: Optional[Path] = args.output
    verbose: bool = args.verbose

    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return EXIT_INPUT_ERROR

    if input_path.is_dir():
        print(f"Error: Input path is a directory, not a file: {input_path}", file=sys.stderr)
        return EXIT_INPUT_ERROR

    try:
        report = analyze_log_file(input_path, verbose=verbose)
        print_summary(report)

        if output_path is not None:
            write_json_report(output_path, report, verbose=verbose)

        return EXIT_OK

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())

"""Stage 6 - Capstone Portfolio Project (OpsOps)

OpsOps is a configurable automation + reporting CLI that:
- Ingests structured JSON data
- Applies enrichment and aggregation logic
- Produces human-readable and JSON reports
- Supports demo and real execution paths

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


# -----------------------------
# Paths
# -----------------------------

APP_DIR = Path(__file__).resolve().parent
STAGE_DIR = APP_DIR.parent
DATA_DIR = STAGE_DIR / "data"


# -----------------------------
# Helpers
# -----------------------------

def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Input file not found: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in file: {path}")


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# -----------------------------
# Core OpsOps Logic
# -----------------------------

def ingest_records(path: Path) -> List[Dict[str, Any]]:
    data = read_json(path)
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of records")
    return data


def enrich_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Enrichment logic:
    - Group records by 'name'
    - Compute count and total value per group
    """
    summary: Dict[str, Dict[str, int]] = defaultdict(lambda: {"count": 0, "total_value": 0})

    for r in records:
        name = r.get("name", "unknown")
        value = int(r.get("value", 0))
        summary[name]["count"] += 1
        summary[name]["total_value"] += value

    return {
        "record_count": len(records),
        "groups": summary,
    }


def print_report(enriched: Dict[str, Any]) -> None:
    print("OpsOps Report")
    print("-------------")
    print(f"Total records: {enriched['record_count']}")
    print()

    for name, stats in enriched["groups"].items():
        print(f"Group: {name}")
        print(f"  Count: {stats['count']}")
        print(f"  Total Value: {stats['total_value']}")
        print()


# -----------------------------
# Commands
# -----------------------------

def cmd_run(args: argparse.Namespace) -> int:
    input_path = Path(args.input)

    try:
        records = ingest_records(input_path)
        enriched = enrich_records(records)
    except ValueError as exc:
        eprint(f"ERROR: {exc}")
        return 2

    if args.json:
        print(json.dumps(enriched, indent=2, ensure_ascii=False))
    else:
        print_report(enriched)

    if args.output:
        try:
            write_json(Path(args.output), enriched)
        except Exception as exc:
            eprint(f"ERROR: Failed writing output file: {exc}")
            return 2

    return 0


def cmd_demo(_: argparse.Namespace) -> int:
    sample = DATA_DIR / "sample.json"
    print("Running OpsOps demo using sample data\n")
    return cmd_run(argparse.Namespace(
        input=sample,
        output=None,
        json=False,
    ))


# -----------------------------
# CLI
# -----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OpsOps - Capstone Automation & Reporting Tool")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run OpsOps against an input JSON file")
    run.add_argument("--input", required=True, help="Path to input JSON data")
    run.add_argument("--output", help="Optional path to write JSON report")
    run.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted report")
    run.set_defaults(func=cmd_run)

    demo = sub.add_parser("demo", help="Run OpsOps demo using sample data")
    demo.set_defaults(func=cmd_demo)

    return p


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

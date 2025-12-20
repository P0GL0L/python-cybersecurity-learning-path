"""Stage 2 - Data Structures and Problem Solving starter.

Replace placeholders with your implementation.
"""

from __future__ import annotations

import argparse
import sys

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Stage 2 - Data Structures and Problem Solving")
    p.add_argument("--demo", action="store_true", help="Run a demo path")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.demo:
        print("Demo running for Stage 2 - Data Structures and Problem Solving")
        return 0
    print("Use --help to see options.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

"""Stage 1 - Foundations and Setup starter.

Replace placeholders with your implementation.
"""

from __future__ import annotations

import argparse
import sys

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Stage 1 - Foundations and Setup")
    p.add_argument("--demo", action="store_true", help="Run a dempo path")
    p.add_argument("--version", action="store_true", help="Print the program version and exit")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.version:
        print("Stage 1 Tool Version: 1.0.0")
        return 0

    elif args.demo:
        name = input("Enter your name: ").strip()

        if not name:
            print("Error: Name cannot be empty.")
            return 1

        print(f"Hello, {name}! Welcome to Stage 1.")
        return 0

    print("Use --help to see options.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

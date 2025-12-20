import argparse
import logging
from pathlib import Path


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="stage3",
        description="Stage 3 - Python Cybersecurity Learning Path starter",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data") / "sample.txt",
        help="Path to an input file (default: data/sample.txt)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)

    logging.info("Stage 3 starter running.")
    logging.info("Input path: %s", args.input)

    # Create sample input file if it does not exist (beginner-friendly behavior)
    args.input.parent.mkdir(parents=True, exist_ok=True)
    if not args.input.exists():
        args.input.write_text("sample input\n", encoding="utf-8")
        logging.info("Created sample input file at: %s", args.input)

    content = args.input.read_text(encoding="utf-8").strip()
    logging.info("Read %d characters.", len(content))

    logging.info("Stage 3 starter complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

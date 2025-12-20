import argparse
import json
import logging
import re
import sys
import shutil
from typing import Iterable
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# Exit codes (Stage 3 checkpoint: meaningful status codes)
EXIT_OK = 0
EXIT_USAGE = 2          # argparse uses 2 for argument errors
EXIT_INPUT_ERROR = 3
EXIT_OUTPUT_ERROR = 4
EXIT_FATAL_PARSE = 5


LOG_LINE_RE = re.compile(
    r"""
    ^
    (?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})   # timestamp
    \s+
    (?P<level>[A-Z]+)                               # log level
    \s+
    (?P<msg>.*)                                     # message (rest of line)
    $
    """,
    re.VERBOSE,
)


@dataclass
class ParsedLine:
    timestamp: str
    level: str
    message: str


def setup_logging(verbose: bool, log_file: Optional[Path]) -> None:
    """
    Logging best practices:
      - Console handler always
      - Optional rotating file handler if --log-file is provided
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # handlers filter levels; keep root wide

    # Clear any default handlers (important if re-run in some environments)
    root.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Console handler
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(fmt)
    root.addHandler(console)

    # Optional rotating file handler
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=256_000,      # 256 KB
            backupCount=3,         # keep up to 3 old logs
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="stage3",
        description="Stage 3 - Files, Automation, and Robust CLI Programs",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional path to a rotating debug log file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------- analyze (Log Analyzer) --------
    analyze_p = subparsers.add_parser(
        "analyze",
        help="Analyze a log file and export a JSON summary report",
    )
    analyze_p.add_argument("--input", type=Path, required=True, help="Path to the input log file")
    analyze_p.add_argument("--output", type=Path, required=True, help="Path to write the JSON report")
    analyze_p.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top message patterns to include (default: 10)",
    )

    # -------- backup (Backup/Sync helper) --------
    backup_p = subparsers.add_parser(
        "backup",
        help="Copy files by pattern from source to destination (supports dry-run)",
    )
    backup_p.add_argument("--source", type=Path, required=True, help="Source directory to search")
    backup_p.add_argument("--dest", type=Path, required=True, help="Destination directory for copied files")
    backup_p.add_argument(
        "--pattern",
        type=str,
        required=True,
        help='Glob pattern to match files (example: "*.log" or "*.txt")',
    )
    backup_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without copying any files",
    )
    backup_p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination files if they already exist",
    )

    return parser.parse_args()



def normalize_message(msg: str) -> str:
    """
    Defensive "message template" normalization.
    This is intentionally simple for beginners:
      - Replace IPs with <IP>
      - Replace integers with <N>
      - Trim whitespace
    """
    msg = msg.strip()
    msg = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "<IP>", msg)
    msg = re.sub(r"\b\d+\b", "<N>", msg)
    return msg


def parse_log_line(line: str) -> Optional[ParsedLine]:
    """
    Parse a single log line.
    Expected format:
      YYYY-MM-DD HH:MM:SS LEVEL message...
    Returns ParsedLine if matched; otherwise None (nonfatal).
    """
    m = LOG_LINE_RE.match(line.rstrip("\n"))
    if not m:
        return None

    ts = m.group("ts")
    level = m.group("level").upper()
    msg = m.group("msg").strip()

    return ParsedLine(timestamp=ts, level=level, message=msg)


def validate_input_file(path: Path) -> Optional[str]:
    if not path.exists():
        return f"Input file does not exist: {path}"
    if not path.is_file():
        return f"Input path is not a file: {path}"
    try:
        # quick read test
        with path.open("r", encoding="utf-8") as _:
            pass
    except OSError as e:
        return f"Input file is not readable: {path} ({e})"
    return None


def validate_output_path(path: Path) -> Optional[str]:
    """
    Ensure we can create the output directory and write the report.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return f"Could not create output directory: {path.parent} ({e})"

    # Write-test to a temp file next to the output (defensive)
    try:
        test_path = path.with_suffix(path.suffix + ".tmp")
        test_path.write_text("", encoding="utf-8")
        test_path.unlink(missing_ok=True)
    except OSError as e:
        return f"Output path is not writable: {path} ({e})"

    return None


def analyze_log(input_path: Path, top_n: int) -> dict:
    """
    Reads the log file and produces a summary dictionary suitable for JSON export.
    """
    total_lines = 0
    parsed_lines = 0
    bad_lines = 0

    level_counts: Counter[str] = Counter()
    template_counts: Counter[str] = Counter()

    first_ts: Optional[str] = None
    last_ts: Optional[str] = None

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            total_lines += 1
            pl = parse_log_line(raw)
            if pl is None:
                bad_lines += 1
                continue

            parsed_lines += 1
            level_counts[pl.level] += 1

            tmpl = normalize_message(pl.message)
            template_counts[tmpl] += 1

            # track first/last timestamps (string compare works for this fixed format)
            if first_ts is None or pl.timestamp < first_ts:
                first_ts = pl.timestamp
            if last_ts is None or pl.timestamp > last_ts:
                last_ts = pl.timestamp

    top_templates = [
        {"template": t, "count": c}
        for t, c in template_counts.most_common(max(0, top_n))
    ]

    report = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input_file": str(input_path),
        "summary": {
            "total_lines": total_lines,
            "parsed_lines": parsed_lines,
            "malformed_lines": bad_lines,
            "first_timestamp": first_ts,
            "last_timestamp": last_ts,
        },
        "counts_by_level": dict(level_counts),
        "top_message_templates": top_templates,
    }

    return report


def write_json_report(output_path: Path, report: dict) -> None:
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose, args.log_file)

    # ---------- analyze ----------
    if args.command == "analyze":
        logging.info("Stage 3 Log Analyzer starting.")
        logging.info("Input:  %s", args.input)
        logging.info("Output: %s", args.output)

        input_error = validate_input_file(args.input)
        if input_error:
            logging.error(input_error)
            return EXIT_INPUT_ERROR

        output_error = validate_output_path(args.output)
        if output_error:
            logging.error(output_error)
            return EXIT_OUTPUT_ERROR

        try:
            report = analyze_log(args.input, args.top)
            write_json_report(args.output, report)
        except Exception as e:
            logging.exception("Fatal error while analyzing logs: %s", e)
            return EXIT_FATAL_PARSE

        logging.info("Report written to: %s", args.output)
        logging.info(
            "Lines: total=%d parsed=%d malformed=%d",
            report["summary"]["total_lines"],
            report["summary"]["parsed_lines"],
            report["summary"]["malformed_lines"],
        )
        logging.info("Stage 3 Log Analyzer complete.")
        return EXIT_OK

    # ---------- backup ----------
    if args.command == "backup":
        logging.info("Stage 3 Backup/Sync helper starting.")
        logging.info("Source:   %s", args.source)
        logging.info("Dest:     %s", args.dest)
        logging.info("Pattern:  %s", args.pattern)
        logging.info("Dry-run:  %s", args.dry_run)
        logging.info("Overwrite:%s", args.overwrite)

        return run_backup(
            source=args.source,
            dest=args.dest,
            pattern=args.pattern,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
        )

    logging.error("Unknown command: %s", args.command)
    return EXIT_USAGE



if __name__ == "__main__":
    raise SystemExit(main())

def write_json_report(output_path: Path, report: dict) -> None:
    def iter_matching_files(source_dir: Path, pattern: str) -> Iterable[Path]:
        """
        Yield all files under source_dir that match the glob pattern.
        Uses rglob for recursive search.
        """
    yield from (p for p in source_dir.rglob(pattern) if p.is_file())


def copy_with_structure(
    source_file: Path,
    source_root: Path,
    dest_root: Path,
    overwrite: bool,
) -> Path:
    """
    Copy source_file into dest_root, preserving the relative folder structure.
    """
    rel = source_file.relative_to(source_root)
    dest_path = dest_root / rel
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists() and not overwrite:
        raise FileExistsError(f"Destination exists (use --overwrite): {dest_path}")

    shutil.copy2(source_file, dest_path)
    return dest_path


def run_backup(source: Path, dest: Path, pattern: str, dry_run: bool, overwrite: bool) -> int:
    # Validate source
    if not source.exists():
        logging.error("Source directory does not exist: %s", source)
        return EXIT_INPUT_ERROR
    if not source.is_dir():
        logging.error("Source path is not a directory: %s", source)
        return EXIT_INPUT_ERROR

    # Validate dest (create if needed)
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logging.error("Could not create destination directory: %s (%s)", dest, e)
        return EXIT_OUTPUT_ERROR

    matches = list(iter_matching_files(source, pattern))
    logging.info("Matched %d file(s) using pattern %r under %s", len(matches), pattern, source)

    copied = 0
    skipped = 0
    errors = 0

    for src in matches:
        try:
            rel = src.relative_to(source)
            planned_dest = dest / rel

            if planned_dest.exists() and not overwrite:
                logging.warning("SKIP (exists): %s", planned_dest)
                skipped += 1
                continue

            if dry_run:
                logging.info("DRY-RUN copy: %s -> %s", src, planned_dest)
                copied += 1
                continue

            out_path = copy_with_structure(src, source, dest, overwrite=overwrite)
            logging.info("COPIED: %s -> %s", src, out_path)
            copied += 1

        except Exception as e:
            logging.error("ERROR copying %s: %s", src, e)
            errors += 1

    logging.info("Backup summary: planned/copied=%d skipped=%d errors=%d", copied, skipped, errors)
    return EXIT_OK if errors == 0 else EXIT_FATAL_PARSE


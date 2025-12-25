"""Log parser module for SecureSIEM.

Converts raw log lines into structured :class:`~src.models.LogEntry` objects.

Supported formats:
- Apache access logs (common/combined variants used in this course)
- SSH authentication logs (sshd)
- Generic auth logs (course format)

Parsing uses regular expressions and conservative error handling:
- Unparseable lines are skipped (return None)
- Timestamps that fail to parse become None (still yields entry)
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Generator

from .models import LogEntry, LogType


# =============================================================================
# REGEX PATTERNS
# =============================================================================

APACHE_PATTERN = re.compile(
    r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'             # IP
    r'\s+-\s+'                                       # -
    r'(?P<user>\S+)'                                  # user or -
    r'\s+\[(?P<timestamp>[^\]]+)\]'                # [timestamp]
    r'\s+"(?P<method>\w+)\s+(?P<path>\S+)'          # "METHOD /path
    r'\s+(?P<protocol>[^"]+)"'                         # HTTP/1.1"
    r'\s+(?P<status>\d{3})'                           # status
    r'\s+(?P<size>\d+|-)'                             # size
)

SSH_PATTERN = re.compile(
    r'^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)'   # Dec 25 10:15:32
    r'\s+(?P<host>\S+)'                                # hostname
    r'\s+sshd\[\d+\]:'                               # sshd[pid]:
    r'\s+(?P<status>Failed|Accepted)'                   # Failed/Accepted
    r'\s+password\s+for\s+'
    r'(?:invalid\s+user\s+)?'
    r'(?P<user>\S+)'
    r'\s+from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'
)

AUTH_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
    r'\s+AUTH\s+(?P<status>SUCCESS|FAILURE)'
    r'\s+user=(?P<user>\S+)'
    r'\s+ip=(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'
    r'(?:\s+reason=(?P<reason>\S+))?'
)


# =============================================================================
# TIMESTAMP PARSING
# =============================================================================

def parse_apache_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse Apache timestamp (example: '25/Dec/2024:10:15:32 +0000')."""
    try:
        ts_clean = ts_str.split()[0] if " " in ts_str else ts_str
        return datetime.strptime(ts_clean, "%d/%b/%Y:%H:%M:%S")
    except ValueError:
        return None


def parse_ssh_timestamp(ts_str: str, year: Optional[int] = None) -> Optional[datetime]:
    """Parse SSH log timestamp (no year present in syslog style dates)."""
    if year is None:
        year = datetime.now().year
    try:
        dt = datetime.strptime(ts_str, "%b %d %H:%M:%S")
        return dt.replace(year=year)
    except ValueError:
        return None


def parse_auth_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse generic auth timestamp (example: '2024-12-25 10:15:32')."""
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


# =============================================================================
# LINE PARSERS
# =============================================================================

def parse_apache_line(line: str) -> Optional[LogEntry]:
    match = APACHE_PATTERN.match(line.strip())
    if not match:
        return None

    g = match.groupdict()
    action = f"{g['method']} {g['path']}"

    return LogEntry(
        timestamp=parse_apache_timestamp(g["timestamp"]),
        source_ip=g["ip"],
        log_type=LogType.APACHE,
        raw_line=line.strip(),
        user=None if g["user"] == "-" else g["user"],
        action=action,
        status=g["status"],
        details=f"size={g['size']}",
    )


def parse_ssh_line(line: str) -> Optional[LogEntry]:
    match = SSH_PATTERN.search(line.strip())
    if not match:
        return None

    g = match.groupdict()
    return LogEntry(
        timestamp=parse_ssh_timestamp(g["timestamp"]),
        source_ip=g["ip"],
        log_type=LogType.SSH,
        raw_line=line.strip(),
        user=g["user"],
        action="ssh_login",
        status="success" if g["status"] == "Accepted" else "failure",
        details=f"host={g['host']}",
    )


def parse_auth_line(line: str) -> Optional[LogEntry]:
    match = AUTH_PATTERN.match(line.strip())
    if not match:
        return None

    g = match.groupdict()
    return LogEntry(
        timestamp=parse_auth_timestamp(g["timestamp"]),
        source_ip=g["ip"],
        log_type=LogType.AUTH,
        raw_line=line.strip(),
        user=g["user"],
        action="auth",
        status="success" if g["status"] == "SUCCESS" else "failure",
        details=g.get("reason"),
    )


# =============================================================================
# MAIN PARSER FUNCTIONS
# =============================================================================

def detect_log_type(sample_line: str) -> LogType:
    """Detect log type from a single line."""
    s = sample_line.strip()
    if APACHE_PATTERN.match(s):
        return LogType.APACHE
    if SSH_PATTERN.search(s):
        return LogType.SSH
    if AUTH_PATTERN.match(s):
        return LogType.AUTH
    return LogType.UNKNOWN


def parse_line(line: str, log_type: Optional[LogType] = None) -> Optional[LogEntry]:
    """Parse a single line. Auto-detects type if *log_type* is not provided."""
    if not line or not line.strip():
        return None

    if log_type is None:
        log_type = detect_log_type(line)

    parser_map = {
        LogType.APACHE: parse_apache_line,
        LogType.SSH: parse_ssh_line,
        LogType.AUTH: parse_auth_line,
    }
    parser = parser_map.get(log_type)
    return parser(line) if parser else None


def parse_file(filepath: str) -> Generator[LogEntry, None, None]:
    """Parse a log file yielding entries one at a time (generator)."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {filepath}")

    # Detect file type from first non-empty line.
    log_type: Optional[LogType] = None
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                log_type = detect_log_type(line)
                break

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            entry = parse_line(line, log_type)
            if entry:
                yield entry


def parse_file_to_list(filepath: str) -> List[LogEntry]:
    """Parse a log file and return all entries as a list."""
    return list(parse_file(filepath))

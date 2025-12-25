"""securesiem data models.

This module defines the core data structures used throughout SecureSIEM.

We use dataclasses for clarity and to reduce boilerplate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class LogType(Enum):
    """Supported log formats."""

    APACHE = "apache"
    SSH = "ssh"
    AUTH = "auth"
    UNKNOWN = "unknown"


class Severity(Enum):
    """Threat severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class LogEntry:
    """Represents a single parsed log entry."""

    timestamp: Optional[datetime]
    source_ip: str
    log_type: LogType
    raw_line: str
    user: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None
    details: Optional[str] = None


@dataclass
class Finding:
    """Represents a detected security finding."""

    rule_name: str
    severity: Severity
    source_ip: str
    description: str
    evidence: List[LogEntry] = field(default_factory=list)
    geo_info: Optional[Dict[str, Any]] = None


@dataclass
class AnalysisReport:
    """Represents a complete analysis report."""

    total_entries: int
    findings: List[Finding]
    summary: Dict[str, int]
    analysis_time: datetime = field(default_factory=datetime.now)

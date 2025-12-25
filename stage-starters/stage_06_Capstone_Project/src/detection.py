"""Detection engine for SecureSIEM.

This module implements rule-based detections over parsed log entries.
Rules intentionally stay simple and explainable for beginners, while still
mapping to real SOC workflows.

Rules implemented (course spec):
- brute_force: repeated authentication failures from same IP
- sql_injection: SQLi indicators in HTTP requests
- directory_traversal: ../ style traversal in request paths
- admin_probe: repeated hits on common admin endpoints
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .models import Finding, LogEntry, LogType, Severity


def _is_auth_failure(entry: LogEntry) -> bool:
    # SSH/AUTH store 'failure', Apache stores status codes.
    if entry.status is None:
        return False
    if entry.status == "failure":
        return True
    if entry.log_type == LogType.APACHE and entry.status in {"401", "403"}:
        return True
    if entry.log_type == LogType.AUTH and entry.status == "failure":
        return True
    return False


def detect_brute_force(entries: List[LogEntry], threshold: int = 5) -> List[Finding]:
    """Detect multiple failed logins from the same IP."""
    failures_by_ip: Dict[str, List[LogEntry]] = defaultdict(list)

    for e in entries:
        if _is_auth_failure(e):
            failures_by_ip[e.source_ip].append(e)

    findings: List[Finding] = []
    for ip, failed_entries in failures_by_ip.items():
        if len(failed_entries) >= threshold:
            findings.append(
                Finding(
                    rule_name="brute_force",
                    severity=Severity.HIGH,
                    source_ip=ip,
                    description=f"Possible brute force: {len(failed_entries)} failed attempts from {ip}",
                    evidence=failed_entries[:10],
                )
            )
    return findings


SQL_PATTERNS = [
    "' OR '",
    "' or '",
    "1=1",
    "1 = 1",
    "DROP TABLE",
    "drop table",
    "UNION SELECT",
    "union select",
    "--",
    ";--",
    "/*",
    "*/",
    "@@version",
    "SLEEP(",
    "sleep(",
    "BENCHMARK(",
]


def detect_sql_injection(entries: List[LogEntry]) -> List[Finding]:
    """Detect SQL injection patterns in Apache request lines."""
    suspicious_by_ip: Dict[str, List[LogEntry]] = defaultdict(list)

    for e in entries:
        if e.log_type != LogType.APACHE:
            continue
        haystack = (e.action or "") + " " + e.raw_line
        for pat in SQL_PATTERNS:
            if pat in haystack:
                suspicious_by_ip[e.source_ip].append(e)
                break

    findings: List[Finding] = []
    for ip, sql_entries in suspicious_by_ip.items():
        findings.append(
            Finding(
                rule_name="sql_injection",
                severity=Severity.CRITICAL,
                source_ip=ip,
                description=f"SQL injection attempt detected from {ip} ({len(sql_entries)} suspicious requests)",
                evidence=sql_entries[:10],
            )
        )
    return findings


def detect_directory_traversal(entries: List[LogEntry]) -> List[Finding]:
    """Detect directory traversal indicators in request paths."""
    traversal_patterns = ["../", "..\\", "%2e%2e/", "%2e%2e%2f"]
    suspicious_by_ip: Dict[str, List[LogEntry]] = defaultdict(list)

    for e in entries:
        if not e.action:
            continue
        action_lower = e.action.lower()
        for pat in traversal_patterns:
            if pat in action_lower:
                suspicious_by_ip[e.source_ip].append(e)
                break

    findings: List[Finding] = []
    for ip, trav_entries in suspicious_by_ip.items():
        findings.append(
            Finding(
                rule_name="directory_traversal",
                severity=Severity.HIGH,
                source_ip=ip,
                description=f"Directory traversal attempt from {ip}",
                evidence=trav_entries[:10],
            )
        )
    return findings


def detect_admin_probe(entries: List[LogEntry], threshold: int = 3) -> List[Finding]:
    """Detect repeated access to common admin endpoints."""
    admin_paths = [
        "/admin",
        "/wp-admin",
        "/administrator",
        "/phpmyadmin",
        "/manager",
        "/console",
        "/.env",
        "/config",
    ]
    admin_by_ip: Dict[str, List[LogEntry]] = defaultdict(list)

    for e in entries:
        if not e.action:
            continue
        action_lower = e.action.lower()
        for p in admin_paths:
            if p in action_lower:
                admin_by_ip[e.source_ip].append(e)
                break

    findings: List[Finding] = []
    for ip, admin_entries in admin_by_ip.items():
        if len(admin_entries) >= threshold:
            findings.append(
                Finding(
                    rule_name="admin_probe",
                    severity=Severity.MEDIUM,
                    source_ip=ip,
                    description=f"Admin page probing from {ip} ({len(admin_entries)} requests)",
                    evidence=admin_entries[:10],
                )
            )
    return findings


def run_all_detections(entries: List[LogEntry]) -> List[Finding]:
    """Run all detection rules and return findings sorted by severity."""
    findings: List[Finding] = []
    findings.extend(detect_brute_force(entries))
    findings.extend(detect_sql_injection(entries))
    findings.extend(detect_directory_traversal(entries))
    findings.extend(detect_admin_probe(entries))

    severity_order = {
        Severity.CRITICAL: 0,
        Severity.HIGH: 1,
        Severity.MEDIUM: 2,
        Severity.LOW: 3,
    }
    findings.sort(key=lambda f: severity_order.get(f.severity, 99))
    return findings

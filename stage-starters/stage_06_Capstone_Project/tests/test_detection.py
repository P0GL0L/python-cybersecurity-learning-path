from src.detection import (
    detect_brute_force,
    detect_sql_injection,
    detect_directory_traversal,
    detect_admin_probe,
    run_all_detections,
)
from src.log_parser import parse_line


def test_bruteforce_threshold():
    lines = [
        "Dec 25 10:15:32 server sshd[1]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:33 server sshd[2]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:34 server sshd[3]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:35 server sshd[4]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:36 server sshd[5]: Failed password for root from 192.168.1.100 port 22 ssh2",
    ]
    entries = [parse_line(l) for l in lines]
    entries = [e for e in entries if e]
    findings = detect_brute_force(entries, threshold=5)
    assert len(findings) == 1
    assert findings[0].rule_name == "brute_force"


def test_sql_injection_detected():
    line = "203.0.113.50 - - [25/Dec/2024:10:17:00 +0000] \"GET /search?q=1' OR '1'='1 HTTP/1.1\" 200 0"
    entries = [parse_line(line)]
    findings = detect_sql_injection([e for e in entries if e])
    assert findings
    assert findings[0].rule_name == "sql_injection"


def test_directory_traversal_detected():
    line = "172.16.0.1 - - [25/Dec/2024:10:18:00 +0000] \"GET /../../../etc/passwd HTTP/1.1\" 400 0"
    entries = [parse_line(line)]
    findings = detect_directory_traversal([e for e in entries if e])
    assert findings
    assert findings[0].rule_name == "directory_traversal"


def test_admin_probe_threshold():
    lines = [
        '192.168.1.100 - - [25/Dec/2024:10:15:33 +0000] "GET /admin HTTP/1.1" 403 287',
        '192.168.1.100 - - [25/Dec/2024:10:15:34 +0000] "GET /admin HTTP/1.1" 403 287',
        '192.168.1.100 - - [25/Dec/2024:10:15:35 +0000] "GET /admin HTTP/1.1" 403 287',
    ]
    entries = [parse_line(l) for l in lines]
    entries = [e for e in entries if e]
    findings = detect_admin_probe(entries, threshold=3)
    assert len(findings) == 1
    assert findings[0].rule_name == "admin_probe"


def test_run_all_detections_sorting():
    lines = [
        "203.0.113.50 - - [25/Dec/2024:10:17:00 +0000] \"GET /search?q=1' OR '1'='1 HTTP/1.1\" 200 0",
        "Dec 25 10:15:32 server sshd[1]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:33 server sshd[2]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:34 server sshd[3]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:35 server sshd[4]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "Dec 25 10:15:36 server sshd[5]: Failed password for root from 192.168.1.100 port 22 ssh2",
    ]
    entries = [parse_line(l) for l in lines]
    entries = [e for e in entries if e]
    findings = run_all_detections(entries)
    assert findings
    # SQL injection is CRITICAL and should come first
    assert findings[0].severity.value == "critical"

import pytest
from src.log_parser import detect_log_type, parse_line, parse_file_to_list
from src.models import LogType


def test_detect_apache():
    line = '192.168.1.1 - - [25/Dec/2024:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 1234'
    assert detect_log_type(line) == LogType.APACHE


def test_parse_apache_line():
    line = '203.0.113.50 - - [25/Dec/2024:10:17:00 +0000] "GET /admin HTTP/1.1" 403 287'
    entry = parse_line(line)
    assert entry is not None
    assert entry.log_type == LogType.APACHE
    assert entry.source_ip == "203.0.113.50"
    assert entry.status == "403"
    assert entry.action.startswith("GET ")


def test_parse_ssh_line():
    line = "Dec 25 10:15:32 server sshd[12345]: Failed password for root from 192.168.1.100 port 22 ssh2"
    entry = parse_line(line)
    assert entry is not None
    assert entry.log_type == LogType.SSH
    assert entry.source_ip == "192.168.1.100"
    assert entry.status == "failure"
    assert entry.user == "root"


def test_parse_auth_line():
    line = "2024-12-25 10:15:32 AUTH FAILURE user=admin ip=192.168.1.100 reason=invalid_password"
    entry = parse_line(line)
    assert entry is not None
    assert entry.log_type == LogType.AUTH
    assert entry.source_ip == "192.168.1.100"
    assert entry.status == "failure"
    assert entry.user == "admin"


def test_parse_file_to_list(tmp_path):
    p = tmp_path / "sample.log"
    p.write_text("2024-12-25 10:15:32 AUTH FAILURE user=admin ip=192.168.1.100 reason=invalid_password\n")
    entries = parse_file_to_list(str(p))
    assert len(entries) == 1

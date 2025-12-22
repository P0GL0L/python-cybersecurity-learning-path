# Python for Cybersecurity Learning Path

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/P0GL0L/python-cybersecurity-learning-path?style=social)](https://github.com/P0GL0L/python-cybersecurity-learning-path/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/P0GL0L/python-cybersecurity-learning-path?style=social)](https://github.com/P0GL0L/python-cybersecurity-learning-path/network/members)
[![Issues](https://img.shields.io/github/issues/P0GL0L/python-cybersecurity-learning-path)](https://github.com/P0GL0L/python-cybersecurity-learning-path/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Last Commit](https://img.shields.io/github/last-commit/P0GL0L/python-cybersecurity-learning-path)](https://github.com/P0GL0L/python-cybersecurity-learning-path/commits/main)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue)](https://P0GL0L.github.io/python-cybersecurity-learning-path)
[![NICE Framework](https://img.shields.io/badge/NICE-Framework%20Aligned-purple)](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center)

> A comprehensive, security-first Python learning path from fundamentals to professional automation.  
> Aligned with the NICE Cybersecurity Workforce Framework.  
> **~225–265 hours of hands-on, portfolio-driven learning.**

---

## 🚦 Start Here

- **New learners:** Start with `docs/START_HERE.md`
- **Track progress:** Use `docs/LEARNER_PROGRESS_CHECKLIST.md`
- **Interview / portfolio review:** See `audience-docs/`

**Workflow rule:** Complete each stage, then **commit and push** before moving on.

---

## 📌 What This Repository Is

- Beginner-to-capstone Python learning path
- Security concepts introduced from Day 1
- Hands-on tools, not theory-only exercises
- NICE Cybersecurity Workforce Framework aligned
- Designed for learners, career-changers, and students

---

## 📁 Repository Structure

.
├── docs/
│ ├── START_HERE.md
│ └── LEARNER_PROGRESS_CHECKLIST.md
├── stage-starters/
│ ├── stage_01/
│ ├── stage_02/
│ ├── stage_03/
│ ├── stage_04/
│ ├── stage_05/
│ └── stage_06/
├── capstone/
├── audience-docs/
├── TESTIMONIALS.md
└── README.md


---

## 🧭 Learning Path Overview

### Stage 01 – Python Foundations
Variables, conditionals, loops, secure input handling, CLI workflow discipline

### Stage 02 – Core Programming & Data Handling
Functions, collections, menu-driven CLI tools

### Stage 03 – File Handling & Automation
Safe file I/O, error handling, predictable exit states

### Stage 04 – APIs & Network Integration
Secure API usage, secrets handling, network scanning fundamentals

### Stage 05 – Testing, Packaging & CI
Unit testing, mocking, packaging, CI workflows

### Stage 06 – Portfolio-Ready CLI Tool
Integrated security tooling with documentation and tests

### Capstone – Final Integration Project
End-to-end security automation platform, interview-ready

---

## 🧠 NICE Framework Alignment

- **SP-DEV** – Secure software development  
- **PR-CDA** – Cyber defense analysis  
- **OM-ADM** – Automation and integrity monitoring  

---

## 📋 Prerequisites

### Required
- Basic computer literacy
- Comfort using the command line
- 10–15 hours per week recommended

### Recommended
- Intro programming exposure
- Basic networking concepts
- Linux familiarity

### Technical Requirements
- OS: Windows, macOS, or Linux
- Python: 3.8+
- RAM: 8 GB minimum (16 GB recommended)
- Storage: ~20 GB free

---

## ⏱️ Time Estimates

| Stage | Time | Difficulty |
|-----|-----|-----------|
| Stage 01 | 25–30 hrs | Beginner |
| Stage 02 | 30–35 hrs | Beginner–Intermediate |
| Stage 03 | 35–40 hrs | Intermediate |
| Stage 04 | 30–35 hrs | Intermediate |
| Stage 05 | 30–35 hrs | Intermediate–Advanced |
| Stage 06 | 35–40 hrs | Advanced |
| Capstone | 40–50 hrs | Advanced |
| **Total** | **225–265 hrs** | Comprehensive |

---

## 🚀 Getting Started
```bash
git clone https://github.com/P0GL0L/python-cybersecurity-learning-path.git
cd python-cybersecurity-learning-path
```

### Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
Windows PowerShell: .\venv\Scripts\Activate.ps1
Windows CMD: venv\Scripts\activate.bat
macOS/Linux: source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Run a stage script:
```bash
python path/to/script.py
```

## 💻 What You'll Learn: Code Examples


See the progression from basic Python to production-ready security tools.

<details>
<summary><b>Stage 01: From Basic to Security-Aware Code</b> 👈 Click to expand</summary>

### Before: Simple user input
```python
# ❌ Insecure approach
username = input("Enter username: ")
password = input("Enter password: ")
print(f"Welcome {username}!")
```

### After: Security-conscious input handling
```python
import getpass
import re

def get_secure_credentials():
    """Get user credentials with security best practices."""
    username = input("Enter username: ").strip()
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username format")
    
    password = getpass.getpass("Enter password: ")
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    
    return username, password
```

**Key learning:** Security awareness from day one - no plain text passwords!

</details>

<details>
<summary><b>Stage 03: Implementing Cryptography</b> 👈 Click to expand</summary>

### Password Hashing with Salt (PBKDF2)
```python
import hashlib
import os
import base64

def hash_password(password: str) -> tuple[str, str]:
    """Hash password with salt. Returns (salt, hash) for storage."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return (
        base64.b64encode(salt).decode('utf-8'),
        base64.b64encode(key).decode('utf-8')
    )

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    salt_bytes = base64.b64decode(salt.encode('utf-8'))
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
    return base64.b64encode(key).decode('utf-8') == stored_hash
```

**Key learning:** Never store passwords in plain text - always hash with salt!

</details>

<details>
<summary><b>Stage 04: Network Port Scanner (Async)</b> 👈 Click to expand</summary>

```python
import asyncio
import socket

async def scan_port(ip: str, port: int) -> tuple[int, bool]:
    """Scan a single port asynchronously."""
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=1.0
        )
        writer.close()
        await writer.wait_closed()
        return (port, True)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return (port, False)

async def scan_ports(ip: str, ports: list[int]) -> list[int]:
    """Scan multiple ports concurrently."""
    tasks = [scan_port(ip, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return [port for port, is_open in results if is_open]

# Scan 1000 ports in ~10 seconds with async!
```

**Key learning:** Asynchronous programming makes network tools 50x faster!

</details>

<details>
<summary><b>Stage 05: SQL Injection Scanner</b> 👈 Click to expand</summary>

```python
import requests

class SQLiScanner:
    """Basic SQL injection vulnerability scanner."""
    
    PAYLOADS = ["' OR '1'='1", "' OR '1'='1' --", "admin'--"]
    ERROR_PATTERNS = ["SQL syntax", "mysql_fetch", "ORA-"]
    
    def test_parameter(self, url: str, param: str):
        """Test parameter for SQL injection."""
        for payload in self.PAYLOADS:
            test_url = f"{url}?{param}={payload}"
            response = requests.get(test_url, timeout=5)
            
            for pattern in self.ERROR_PATTERNS:
                if pattern in response.text:
                    return {'vulnerable': True, 'evidence': pattern}
        return {'vulnerable': False}
```

**Key learning:** Automated vulnerability detection - OWASP Top 10 in action!

**⚠️ Legal Note:** Only test systems you own or have written permission to test.

</details>

<details>
<summary><b>Stage 06: Threat Intelligence Aggregator</b> 👈 Click to expand</summary>

```python
import requests
from datetime import datetime

class ThreatIntelAggregator:
    """Aggregate threat intelligence from multiple sources."""
    
    def fetch_urlhaus_threats(self) -> list[dict]:
        """Fetch recent malicious URLs from URLhaus."""
        response = requests.post(
            'https://urlhaus-api.abuse.ch/v1/urls/recent/',
            timeout=10
        )
        data = response.json()
        
        threats = []
        for url_data in data.get('urls', [])[:10]:
            threats.append({
                'indicator': url_data['url'],
                'type': 'url',
                'threat_type': url_data.get('threat', 'unknown'),
                'source': 'URLhaus',
                'risk_score': self.calculate_risk(url_data)
            })
        return threats
    
    def calculate_risk(self, threat_data: dict) -> int:
        """Calculate risk score (0-100)."""
        score = 50
        if threat_data.get('threat') in ['malware', 'ransomware']:
            score += 30
        if threat_data.get('url_status') == 'online':
            score += 20
        return min(score, 100)
```

**Key learning:** Real-time threat intelligence from multiple APIs!

</details>

<details>
<summary><b>Stage 07: Security Automation Platform (Capstone)</b> 👈 Click to expand</summary>

```python
import asyncio
from datetime import datetime

class SecurityAutomationPlatform:
    """Complete security automation platform."""
    
    async def run_automation_cycle(self, targets: list[str]):
        """Run complete automation cycle."""
        print("🚀 Starting Security Automation Platform\n")
        
        # Run all tasks concurrently
        await asyncio.gather(
            self.run_vulnerability_scan(targets),
            self.collect_threat_intelligence(),
            self.analyze_logs()
        )
        
        # Correlate and analyze
        await self.correlate_and_analyze()
        
        # Generate report
        self.generate_report()
        self.export_results()
```

**Architecture:**
```
Web Dashboard → FastAPI → [Vuln Scanner | Threat Intel | Log Analysis]
                              ↓              ↓              ↓
                          Alert & Reporting System
```

**Key learning:** Integrate everything you've built into one production platform!

</details>

---

### 🎯 Progressive Complexity

| Stage | What You Build | Key Skill |
|-------|---------------|-----------|
| **01-02** | Password checker, file tools | Python fundamentals |
| **03** | Encryption tools, hash utilities | Cryptography |
| **04** | Port scanner, packet sniffer | Network programming |
| **05** | Web vulnerability scanner | Web security |
| **06** | Threat intel aggregator | API integration |
| **07** | Complete security platform | System architecture |

**Full code examples with detailed explanations available in each stage's directory!** 🚀

---

**Want to try it now?** See [QUICKSTART.md](QUICKSTART.md) for your first security script in 5 minutes!

---

## 🎉 Success Stories

See how learners transitioned into cybersecurity roles:
...coming soon....

---

## 🤝 Contributing

Please review CONTRIBUTING.md and SECURITY.md.

---

## 📜 License

MIT License. See LICENSE for details.

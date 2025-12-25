# Stage 06 — Capstone Project: SecureSIEM (Security Log Analyzer)

Welcome to the capstone. In this stage you will apply **everything** you learned in Stages 01–05 to build a complete, portfolio-worthy cybersecurity tool: **SecureSIEM**.

SecureSIEM is a command-line tool that:
- Parses multiple log formats (Apache access logs, SSH auth logs, and a generic AUTH log format)
- Detects suspicious activity (brute force attempts, SQL injection, directory traversal, admin probing)
- Optionally enriches suspicious IP addresses with geolocation context (with caching)
- Generates professional output to the console and optional JSON reports
- Includes a test suite and GitHub Actions CI

---

## Learning Outcomes

By the end of Stage 06, you will be able to:

- Design a multi-module Python project with clear responsibilities (SRP)
- Build a professional CLI tool using `argparse` subcommands
- Parse messy real-world text into structured data using regex and dataclasses
- Implement detection rules and create explainable findings
- Integrate an external API safely (timeouts, error handling, caching)
- Write unit tests with pytest, including mocking network calls
- Package a Python project with `pyproject.toml`
- Run CI in GitHub Actions

---

## Project Structure

This stage uses a clean, testable module layout:

```
stage_06/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point, coordinates modules
│   ├── cli.py            # Command-line interface
│   ├── log_parser.py     # Log file parsing
│   ├── detection.py      # Threat detection rules
│   ├── enrichment.py     # IP geolocation API
│   ├── cache.py          # Response caching
│   ├── reports.py        # Report generation
│   └── models.py         # Data classes (LogEntry, Finding, AnalysisReport)
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_detection.py
│   ├── test_enrichment.py
│   ├── test_cache.py
│   └── test_reports.py
├── data/
│   ├── sample_apache.log
│   ├── sample_ssh.log
│   └── sample_auth.log
├── .github/workflows/ci.yml
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Quickstart

### 1) Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install in editable mode (with dev dependencies)

From inside `stage_06/`:

```bash
pip install -e ".[dev]"
```

### 3) Run tests

```bash
pytest -v
```

### 4) Run SecureSIEM

Show help:
```bash
securesiem --help
```

Analyze a file:
```bash
securesiem analyze --input data/sample_apache.log --verbose
```

Analyze + enrich + export JSON:
```bash
securesiem analyze --input data/sample_apache.log --enrich --output report.json
```

Summary:
```bash
securesiem summary --input data/sample_ssh.log
```

Clear cache:
```bash
securesiem cache-clear
```

---

## How SecureSIEM Works (Data Flow)

1. CLI validates inputs and reads the target log file
2. Parser converts log lines into `LogEntry` objects
3. Detection rules convert entries into `Finding` objects
4. Enrichment optionally adds geolocation context to findings (cached)
5. Reporting prints results and optionally writes a JSON report

---

## Acceptance Criteria (Minimum Bar)

You should meet these before calling Stage 06 complete:

- The CLI runs: `securesiem --help`
- The parser correctly parses the included sample logs
- Detections produce findings on the sample logs
- Enrichment works without crashing and uses caching
- JSON report export works
- Tests pass locally: `pytest -v`
- GitHub Actions CI is green

---

## Common Troubleshooting

### `ModuleNotFoundError: No module named 'src'`
You are likely running from the wrong directory.
- `cd stage_06`
- run `pip install -e ".[dev]"` again

### Enrichment returns `None` or missing fields
- The API may be rate-limiting or temporarily unavailable.
- Try again later, or run without `--enrich`.

### Windows PowerShell won’t activate the venv
Run PowerShell as Administrator, then:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Next Extensions (Optional)

If you want to go beyond the baseline capstone:
- Add more detections (XSS, command injection, credential stuffing)
- Add a “watch” mode to monitor a log file in near real time
- Integrate a second threat intel source (VirusTotal/AbuseIPDB) with an API key
- Create an HTML report output
- Add coverage thresholds and linting in CI

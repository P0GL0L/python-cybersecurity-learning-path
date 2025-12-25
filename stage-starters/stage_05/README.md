# Stage 05 â€” Testing, Packaging, CI, and Documentation
## Writing Professional-Quality Tests with pytest

Welcome to **Stage 05**.

Stages 01â€“04 focused on writing code that *does things*. Stage 05 focuses on writing code that *checks your code*: automated tests that verify behavior, catch regressions, and prove your tool fails safely under bad inputs and hostile conditions.


---

## What You Will Build by the End of Stage 05

You will deliver:

- **10+ automated tests** using `pytest`
- Tests that run **WITHOUT internet** (mocking network calls)
- A packaged Python project installable with **pip**
- A GitHub Actions **CI pipeline** that runs tests on every push / PR

Important: Stage 05 is primarily about **quality and workflow**, not adding new features.

---

## Repository Layout (Target)

```text
Stage_05_Testing_Packaging_CI_Documentation/
â”œâ”€â”€ app/
â”‚ â””â”€â”€ main.py
â”œâ”€â”€ tests/
â”‚ â”œâ”€â”€ test_pure_functions.py
â”‚ â”œâ”€â”€ test_http_mocking.py
â”‚ â”œâ”€â”€ test_cache_tmp_path.py
â”‚ â””â”€â”€ test_cli_errors.py
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ README.md
â””â”€â”€ .github/
â””â”€â”€ workflows/
â””â”€â”€ ci.yml
```
---

## Prerequisites

- Python 3.10+ recommended
- `pip` available

---

## Part 1 â€” Setup pytest (Milestone 1)

From inside this stage folder:

### Windows PowerShell
```powershell
python -m pip install -U pip
python -m pip install pytest
python -m pytest --version
```

macOS/Linux
```bash
python -m pip install -U pip
python -m pip install pytest
python -m pytest --version
```
Run tests (verbose):
```powershell
python -m pytest -v
```

### Part 2 â€” Your First Test (Milestone 1 continued)

Create tests/test_pure_functions.py:
```python
import app.main as m

def test_clamp_int_bounds():
    assert m.clamp_int(0, 1, 10) == 1   # below min
    assert m.clamp_int(50, 1, 10) == 10 # above max
    assert m.clamp_int(5, 1, 10) == 5   # in range
```
Run
```powershell
python -m pytest -v
```

### Part 3 â€” Testing Pure Functions (Milestone 2)

**Pure functions are easiest to test because they have:**
- no network
- no filesystem
- no time dependence

**Recommended pure-function tests:**
clamp_int()
parse_latlon()
normalize_us_location()

Example:
```python
import app.main as m

def test_parse_latlon_valid():
    assert m.parse_latlon("47.6,-122.3") == (47.6, -122.3)

def test_parse_latlon_invalid():
    assert m.parse_latlon("hello") is None

def test_parse_latlon_boundary():
    assert m.parse_latlon("90,180") == (90.0, 180.0)
```
### Part 4 â€” Mocking (Milestones 3â€“5)
**Why mocking?**
- You must not hit real APIs during tests:
- tests should run offline
- tests should be deterministic
- tests should be fast
- tests should not get rate-limited

**Monkeypatch basics (Milestone 3)**
```python
import app.main as m

def test_fetch_currency_monkeypatch(monkeypatch):
    def fake_http(url, timeout):
        return {"base": "USD", "date": "2025-01-01", "rates": {"EUR": 0.92}}

    monkeypatch.setattr(m, "http_get_json", fake_http)

    result = m.fetch_currency("USD", "EUR", timeout=5)
    assert result["rates"]["EUR"] == 0.92
```
**Test error conditions (Milestone 5)**
```python
import pytest
import app.main as m

def test_fetch_currency_requires_base():
    with pytest.raises(m.DataError):
        m.fetch_currency("", "EUR", timeout=5)
```

### Part 5 â€” tmp_path and Filesystem Tests (Milestone 6)

Use tmp_path so tests donâ€™t conflict with each other and donâ€™t leave junk files.
```python
import app.main as m

def test_cache_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(m, "now_ts", lambda: 1000)

    m.cache_set("key", {"hello": "world"})
    meta, data = m.cache_get("key", ttl=900)

    assert meta.hit is True
    assert data["hello"] == "world"
```

### Part 6 â€” Fixtures (Milestone 7)

Fixtures let you reuse setup.
```python
import pytest
import app.main as m

@pytest.fixture
def sample_weather_payload():
    return {"source": "weather", "location_resolved": "Seattle", "current": {"temperature_2m": 10}}

def test_print_report_contains_temp(sample_weather_payload, capsys):
    m.print_report(sample_weather_payload)
    out = capsys.readouterr().out
    assert "Temp" in out
```

### Part 7 â€” Packaging with pyproject.toml (Milestone 8)

Create pyproject.toml:
```python
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "stage05-toolkit"
version = "0.1.0"
description = "Stage 05: testing, packaging, CI, and documentation for a production-style CLI."
readme = "README.md"
requires-python = ">=3.10"
[project.optional-dependencies]
dev = ["pytest>=7.0"]

[project.scripts]
stage5-tool = "app.main:main"
```
Install editable + dev deps:
```powershell
python -m pip install -e ".[dev]"
stage5-tool --help
python -m pytest -q
```
### Part 8 â€” CI with GitHub Actions (Milestone 9)

Create .github/workflows/ci.yml:
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install -U pip
      - run: pip install -e ".[dev]"
      - run: pytest -q
```
**Verify:**

GitHub repo â†’ Actions tab â†’ green checks = passing builds.

---
### Part 9 â€” Documentation (Milestone 10)

Your README must include:
- Installation
- Usage examples
- How to run tests
- Troubleshooting guidance 
---

### Success Checklist (Definition of Done)

**Testing:**

 - [ ] 10+ unit tests
 - [ ] Pure functions tested
 - [ ] HTTP mocked (no internet required)
 - [ ] Error paths tested
 - [ ] Cache/filesystem tested with tmp_path

**Packaging:**

 - [ ] pyproject.toml exists
 - [ ] pip install -e ".[dev]" works
 - [ ] stage5-tool --help works

**CI:**

 - [ ] .github/workflows/ci.yml exists
 - [ ] Actions passes on push/PR

**Documentation:**

 - [ ] Installation
 - [ ] Usage examples
 - [ ] Test instructions
 - [ ] Troubleshooting
---
### Required Git Commands (After Completion)

From repository root:
```powershell
git status
git add stage-starters/Stage_05_Testing_Packaging_CI_Documentation
git commit -m "Complete Stage 05 - Testing, Packaging, and CI"
git push
```
### Do not proceed to Stage 06 until Stage 05 is committed and CI is green!


---

## Running the Tool

Stage 05 supports **two equivalent execution methods**:

- **Installed console script** (`stage5-tool`) â€” preferred in real projects
- **Direct Python invocation** (`python app/main.py`) â€” useful for development and debugging

Both methods run the same code and accept the same arguments.

### Option A â€” Installed Script (Recommended)

After installing Stage 05 in editable mode:

```powershell
python -m pip install -e ".[dev]"
```

You can run the tool using the console script:
```powershell
stage5-tool --help
```

Examples
Fetch weather:
```powershell
stage5-tool fetch --source weather --location "Seattle,WA"
```
Fetch currency:
```powershell
stage5-tool fetch --source currency --base USD --symbols EUR,JPY
```
Generate an integration report:
```powershell
stage5-tool integrate --source weather --location "Seattle,WA" --input data\sample.json --output report.json
```
Cache Utilities:
```powershell
stage5-tool cache status
stage5-tool cache clear
```

### Why this matters:
This mirrors how professional Python tools are distributed and executed after installation.

---

### Option B â€” Direct Python Execution (Development Mode)

If you prefer not to install the package, you can run the tool directly with Python.
From inside the stage folder:

```powershell
python app\main.py --help
```
**Examples**

Fetch weather:
```python
python app\main.py fetch --source weather --location "Seattle,WA"
```
Fetch currency:
```pythoin
python app\main.py fetch --source currency --base USD --symbols EUR,JPY
```
Generate an integration report:
```python
python app\main.py integrate --source currency --base USD --symbols EUR,JPY --input data\sample.json --output report.json
```
Cache utilities:
```python
python app\main.py cache status
python app\main.py cache clear
```
***Note:***
This method is ideal for debugging, stepping through code, and test-driven development.

**Which Method Should I Use?**

## Which Method Should I Use?

Use **`stage5-tool`** when:
- You want a realistic, production-style workflow
- You are validating packaging and CI behavior
- You are simulating how users run installed tools

Use **`python app/main.py`** when:
- You are actively developing or debugging
- You want to run the code without installing
- You are stepping through tests or adding features

***Both methods are fully supported and tested.***

---
**Editors Note **
How to Run the Tests
From inside Stage_05_Testing_Packaging_CI_Documentation/:
```powershell
python -m pip install -e ".[dev]"
python -m pytest -v
```

**Install and verify pyproject.toml**
```powershell
python -m pip install -e ".[dev]"
stage5-tool --help
python -m pytest
```
**For cy.yml:**
***Notes:***
- Uses working-directory so CI runs only for Stage 05 without needing repo-wide packaging.
- Runs offline-safe tests (your tests mock network).

**Integration command examples:**
***sample.json***
Weather merge:
```powershell
python .\app\main.py integrate --source weather --location "Seattle,WA" --input data\sample.json --output report.json
```
```powershell
python .\app\main.py integrate --source currency --base USD --symbols "EUR,JPY" --input data\sample.json --output report.json
```

---

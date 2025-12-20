# Stage 6 — Capstone Portfolio Project (OpsOps)

## Goal
**OpsOps** is a configurable automation + reporting tool (CLI) that:
- Ingests local JSON data (records/log-like entries)
- Enriches and aggregates data into a report-ready structure
- Outputs human-readable reports and optional JSON output

This stage is a portfolio-style release: a runnable tool, packaged install, tests, and clear documentation.

---

## Repository Layout
- `app/`
  - `main.py` — OpsOps CLI implementation
  - `__init__.py`
- `data/`
  - `sample.json` — example input dataset
- `tests/`
  - `test_opso.py` — unit test suite
- `pyproject.toml` — packaging + dev dependencies

---

## Acceptance Criteria Mapping
- **Capstone CLI implemented:** `opso run` / `opso demo` available
- **Test suite included:** `python -m pytest -q` (10+ tests)
- **Packaging included:** `pyproject.toml` supports editable install and console script
- **Docs included:** install, usage, examples, troubleshooting, and demo transcript are included below

---

## Requirements
- Python **3.10+** (recommended)
- Standard library only for runtime execution
- `pytest` for tests (installed via `[dev]` extras)

---

## Install (Developer / Local)
From the `stage_06` folder:

```powershell
python -m pip install -e ".[dev]"

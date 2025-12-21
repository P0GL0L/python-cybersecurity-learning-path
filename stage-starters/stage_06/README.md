# Stage 06 - Capstone Portfolio Project (OpsOps)

## Goal

**OpsOps** is a configurable automation and reporting command-line tool (CLI) that:

- Ingests local JSON data (records or log-like entries)
- Enriches and aggregates data into a report-ready structure
- Outputs human-readable reports and optional JSON output

This stage represents a **portfolio-style release**: a runnable tool, installable package, test suite, and complete documentation.

---

## Repository Layout

```
stage_06/
├── app/
│   ├── main.py        - OpsOps CLI implementation
│   └── __init__.py
├── data/
│   └── sample.json    - example input dataset
├── tests/
│   └── test_opso.py   - unit test suite
└── pyproject.toml     - packaging and development dependencies
```

---

## Acceptance Criteria (Must Meet)

To complete Stage 06, all of the following must be true:

- **Capstone CLI implemented**
  - Commands such as `opso run` and `opso demo` are available
- **Test suite included**
  - `python -m pytest -q`
  - At least 10 meaningful tests
- **Packaging included**
  - `pyproject.toml` supports editable install and console script entry point
- **Documentation included**
  - Install
  - Usage
  - Examples
  - Troubleshooting
  - Demo transcript

---

## Requirements

- Python **3.10+** recommended
- Standard library only for runtime execution
- `pytest` for tests (installed via `[dev]` extras)

---

## Install (Developer / Local)

From the `stage_06` folder:

Windows PowerShell:
```powershell
python -m pip install -e ".[dev]"
```

macOS / Linux:
```bash
python -m pip install -e ".[dev]"
```

---

## Running the Tool

After installation, example commands may include:

```powershell
opso demo
opso run --input data/sample.json
```

(macOS / Linux)
```bash
opso demo
opso run --input data/sample.json
```

Use `--help` to see all available options:

```powershell
opso --help
```

---

## Running Tests

From the `stage_06` directory:

```powershell
python -m pytest -q
```

(macOS / Linux)
```bash
python -m pytest -q
```

---

## Definition of Done (Required)

Stage 06 is **only complete** when **all** of the following are true:

1. OpsOps runs successfully from the command line
2. All acceptance criteria are met
3. All tests pass locally
4. Package installs correctly
5. Documentation is complete and readable
6. Changes are **committed and pushed to GitHub**

### Required Git Commands (After Completion)

From the repository root:

```powershell
git status
git add stage-starters/stage_06
git commit -m "Complete Stage 06 - OpsOps capstone project"
git push
```

---

## What’s Next

After completing and committing Stage 06:

- Review the final `capstone/` project (if applicable)
- Ensure your repository tells a clear story for instructors and employers
- Use this stage as a portfolio reference

## What’s Next

Choose documentation based on your goal:

- Learning review: `docs/LEARNER_PROGRESS_CHECKLIST.md`
- Interview prep: `audience-docs/interview_talking_points.md`
- Employer review: `audience-docs/employer_README.md`
- Academic evaluation: `audience-docs/instructor_notes.md`

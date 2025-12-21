# Stage 05 - Testing, Packaging, CI, and Documentation

## Overview

This stage focuses on hardening the prior-stage Python CLI into something that behaves like a real internal tool by adding:

- **Unit testing** with `pytest` (or `unittest`)
- **Mocking** for external I/O (network, files, environment, time) to keep tests deterministic
- **Packaging** with `pyproject.toml` (setuptools)
- A **GitHub Actions CI pipeline** that runs tests on push and pull requests
- Clean **documentation**: install, usage, examples, and troubleshooting

This stage does not add new features. It improves reliability, repeatability, and maintainability.

---

## Learning Objectives

By the end of Stage 05, you should be able to:

- Write unit tests with meaningful assertions for core logic
- Mock external dependencies so tests run offline and consistently
- Package a Python project so it can be installed and built predictably
- Configure CI to automatically run tests and produce artifacts
- Document the tool so another person can run it without assistance

---

## Repository Layout

```
stage_05/
├── app/
│   └── main.py
├── tests/
│   └── test_*.py
├── pyproject.toml
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Acceptance Criteria (Must Meet)

To complete Stage 05, all of the following must be true:

- **At least 10 unit tests** with meaningful assertions
- Tests do **not** rely on live network calls (external I/O is mocked)
- Project is an **installable package** via `pyproject.toml`
- CI runs on **push** and **pull_request**
- README includes **install**, **usage**, **examples**, and **troubleshooting**

---

## Prerequisites

- Python 3.10+ recommended
- No external dependencies required unless you choose to add them

---

## Where You Should Be

All commands below assume you are in:

```
python-cybersecurity-learning-path/stage-starters/stage_05
```

### Confirm your location

Windows PowerShell:
```powershell
Get-Location
Get-ChildItem
```

macOS / Linux:
```bash
pwd
ls
```

---

## Running Tests

From the `stage_05` directory:

```powershell
python -m pytest -q
```

(macOS / Linux)

```bash
python -m pytest -q
```

---

## Definition of Done (Required)

Stage 05 is **only complete** when **all** of the following are true:

1. All acceptance criteria are met
2. Tests pass locally
3. CI passes on GitHub
4. Package installs correctly
5. Documentation is complete and readable
6. Changes are **committed and pushed to GitHub**

### Required Git Commands (After Completion)

From the repository root:

```powershell
git status
git add stage-starters/stage_05
git commit -m "Complete Stage 05 - Testing, Packaging, and CI"
git push
```

Do **not** proceed to Stage 06 without a clean commit and push.

---

## What’s Next

After completing and committing Stage 05:

- Proceed to `stage-starters/stage_06`
- Apply the same quality and workflow standards
- Prepare for a portfolio-ready release

## What’s Next

Proceed to `stage-starters/stage_0X+1`

Do not continue until this stage is committed and pushed.

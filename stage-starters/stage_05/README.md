# Stage 5 — Testing, Packaging, CI, and Documentation

## Overview
This stage focuses on hardening the prior-stage Python CLI into something that behaves like a real internal tool by adding:
- **Unit testing** with `pytest` (or `unittest`)
- **Mocking** for external I/O (network/files/env/time) to keep tests deterministic
- **Packaging** with `pyproject.toml` (setuptools)
- A **GitHub Actions CI pipeline** that runs tests on push/PR and produces build artifacts
- Clean **documentation**: install, usage, examples, troubleshooting

This stage does not add new features. It improves reliability, repeatability, and maintainability.

---

## Learning Objectives
By the end of Stage 5, you should be able to:
- Write unit tests with meaningful assertions for core logic
- Mock external dependencies so tests run offline and consistently
- Package a Python project so it can be installed and built predictably
- Configure CI to automatically run tests and produce artifacts
- Document the tool so another person can run it without assistance

---

## Repository Layout
- stage_05/
  - app/
    - main.py
  - tests/
    - test_*.py
  - pyproject.toml
  - README.md
  - .github/
    - workflows/
      - ci.yml

---

## Acceptance Criteria (Must Meet)
- **>= 10 unit tests** with meaningful assertions
- Tests do **not** rely on live network calls (external I/O is mocked)
- Convert this stage into an **installable package** (via `pyproject.toml`)
- CI runs on **push** and **pull_request**
- README includes **install**, **usage**, **examples**, and **troubleshooting**

---

## Prerequisites
- Python 3.10+ recommended
- No external dependencies required unless you choose to add them

---

## Where You Should Be
All commands below assume you are in:

`C:\Users\<USERNAME>\python-cybersecurity-learning-path\stage-starters\stage_05`

Confirm:

```powershell
pwd
ls

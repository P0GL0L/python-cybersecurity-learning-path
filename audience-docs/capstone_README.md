# Capstone Project – Python CLI Automation Tool

## Overview

This capstone represents the **final integration point** of the Python Cybersecurity Learning Path.

It combines:
- disciplined CLI design
- secure data handling
- testing and packaging practices
- documentation suitable for handoff or review

The goal is not feature breadth, but **clarity, reliability, and explainability**.

---

## What This Tool Does

At a high level, the tool:

- Ingests structured local data (JSON or similar)
- Validates and processes records safely
- Produces human-readable and optional machine-readable output
- Follows predictable CLI behavior
- Includes tests and packaging metadata

Exact behavior depends on the implemented scenario, but the structure mirrors real internal tools.

---

## How to Run

### Option A: From Repository Root

Windows PowerShell:
```powershell
python capstone\app\main.py --help
```

macOS / Linux:
```bash
python capstone/app/main.py --help
```

---

### Option B: From Capstone Folder

Windows PowerShell:
```powershell
python app\main.py --help
```

macOS / Linux:
```bash
python app/main.py --help
```

---

## Testing

From the capstone directory:

```powershell
python -m pytest -q
```

(macOS / Linux)
```bash
python -m pytest -q
```

---

## Evaluation Criteria

This capstone should be evaluated on:

- Correctness and stability
- Input validation and failure handling
- Test coverage and determinism
- Documentation clarity
- Git history and workflow discipline
- Ability to explain design decisions

Feature quantity is less important than **intentional design**.

---

## Relationship to Earlier Stages

Earlier stages focus on **isolated skill development**.

This capstone focuses on:
- integration
- polish
- explanation
- readiness for review

It is expected to reuse patterns learned earlier, not reinvent them.

---

## Intended Audience

- Instructors evaluating technical progression
- Reviewers assessing portfolio readiness
- Employers interested in problem-solving approach

---

## Status

Capstone complete and committed using the same workflow standards enforced throughout the repository.

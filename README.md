# Python Cybersecurity Learning Path

A step-by-step Python learning path for cybersecurity, guiding beginners through secure software development, automation, logging, integrity checks, and a final capstone project.

This repository is designed for **learners**, **career-changers**, and **students** who want to learn Python with a real-world cybersecurity focus.

---

## 🚦 Start Here (Read This First)

Choose the path that matches your goal:

- **New learner:**  
  Start with `docs/START_HERE.md` for setup, workflow rules, and how to progress

- **Track progress:**  
  Use `docs/LEARNER_PROGRESS_CHECKLIST.md` to verify stage completion

- **Interview / portfolio / academic review:**  
  See `audience-docs/` for audience-specific documentation

> **Workflow rule:** Complete each stage, then **commit + push** before moving forward.

---

## What This Repository Is

- A **beginner-to-capstone Python learning path**
- Security concepts integrated from day one
- Hands-on projects instead of theory-only lessons
- Aligned to the **NICE Cybersecurity Workforce Framework**
- Built openly so others can learn, fork, and adapt

---

## 📁 Repository Structure

- `docs/`
  - `START_HERE.md` – onboarding, setup, workflow rules
  - `LEARNER_PROGRESS_CHECKLIST.md` – stage completion checklist
- `stage-starters/`
  - Stages **01–06**, each focused on a specific skill boundary
- `capstone/`
  - Final integration project demonstrating applied skills
- `audience-docs/`
  - Learner, employer, instructor, and interview documentation

---

## 🧭 Learning Path Overview

### Stage 01 – Python Foundations
- Variables, input/output, conditionals, loops
- Secure input handling
- CLI structure and workflow discipline

### Stage 02 – Core Programming & Data Handling
- Functions and scope
- Dictionaries, lists, and sets
- Menu-driven CLI behavior

### Stage 03 – File Handling and Automation
- Safe file I/O
- CLI flags and predictable behavior
- Error handling and exit states

### Stage 04 – APIs and Data Integration
- External API usage with timeouts
- Environment variables for secrets
- Caching and data reuse

### Stage 05 – Testing, Packaging, and CI
- Unit testing with mocking
- Packaging with `pyproject.toml`
- Continuous integration workflows

### Stage 06 – Portfolio-Ready CLI Tool
- Integrated functionality
- Tests and documentation
- Explainable design decisions

### Capstone – Final Integration Project
- End-to-end CLI automation tool
- Secure data handling
- Portfolio-ready presentation

---

## 🧠 NICE Cybersecurity Workforce Framework Alignment

This repository aligns with:

- **Securely Provision (SP-DEV)** – Secure software development
- **Protect and Defend (PR-CDA)** – Log analysis and detection
- **Operate and Maintain (OM-ADM)** – Automation and integrity monitoring

---

## 🚀 Getting Started

1. Clone the repository
2. Read `docs/START_HERE.md`
3. Begin with `stage-starters/stage_01`
4. Commit and push after each stage
5. Complete the capstone in `capstone/`

---

## Audience-Specific Documentation

See `audience-docs/` for:
- learner guidance
- interview talking points
- employer-facing overview
- instructor evaluation notes

## How to Run

### Option A — Use a Virtual Environment (recommended)
**Windows (PowerShell)**
```powershell
git clone https://github.com/P0GL0L/python-cybersecurity-learning-path.git
cd python-cybersecurity-learning-path

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
```

Then run a stage script from its directory, for example:
python path/to/script.py

### Option B — Run Without a Virtual Environment (not recommended)

If you choose not to use a venv, ensure you have Python 3 installed and use python (or python3) directly:

python path/to/script.py

### Note: Some stages may introduce dependencies later. Option A avoids system-level package conflicts.


If you already have specific stage entrypoints (like `stage-starters/stage-1/...`), tell me the exact path(s) and I’ll tailor the commands so they are 1:1 with your repo layout.

---

## 4) Exact Git commands to add everything

From repo root:

```bash
git add LICENSE .gitignore CONTRIBUTING.md SECURITY.md README.md
git commit -m "Add repo hygiene files (license, ignore, contributing, security) and pin How to Run"
git push

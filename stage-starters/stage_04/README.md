# Stage 04 - APIs, Networking Concepts, and Data Integration

## Overview

This stage focuses on building a small, production-style Python command-line tool that:

- Pulls data from a **public API** (for example: weather, currency, etc.)
- Implements **networking best practices** (timeouts, retries, clean failure modes)
- **Caches** results locally to reduce repeat requests and improve resilience
- Generates a simple **report** output
- Demonstrates **data integration** by merging API data with a local JSON or CSV dataset

This stage is intentionally written like a real internal tool: predictable CLI behavior, safe defaults, and clean logs and errors.

---

## Learning Objectives

By the end of Stage 04, you should be able to:

- Build a robust API client using `urllib` or `requests` patterns
- Implement timeouts and defensive error handling for all network calls
- Cache API responses using a file-based cache with a TTL (time-to-live)
- Read and integrate local datasets (JSON or CSV)
- Produce consistent report output suitable for logs, tickets, or dashboards

---

## Repository Layout

```
stage_04/
├── app/
│   ├── __init__.py
│   └── main.py
├── data/
│   └── sample.json
└── README.md
```

---

## Acceptance Criteria (Must Meet)

To complete Stage 04, all of the following must be true:

- All network calls include **timeouts** and **error handling**
- **No API keys** are committed to Git
- Secrets are provided via **environment variables**
- Caching is implemented and respects a TTL
- The CLI supports `--help` and exits cleanly on error

---

## Prerequisites

- Python 3.10+ recommended
- Standard library preferred (external libraries optional, but no secrets committed)

---

## Configuration (No Secrets in Git)

If the API you choose requires a key, store it in an environment variable.

### Windows PowerShell

```powershell
setx API_KEY "your_key_here"
```

Restart your terminal after setting the variable.

### macOS / Linux

```bash
export API_KEY="your_key_here"
```

---

## How to Run

You can run this stage in two supported ways.

### Option A: Run from the Repository Root (Recommended)

Windows PowerShell:
```powershell
python stage-starters\stage_04\app\main.py --help
```

macOS / Linux:
```bash
python stage-starters/stage_04/app/main.py --help
```

---

### Option B: Run from Inside the Stage Folder

If your terminal is already in `stage-starters/stage_04`:

Windows PowerShell:
```powershell
python app\main.py --help
```

macOS / Linux:
```bash
python app/main.py --help
```

---

## Expected Output (Example)

A typical successful run may:

- Fetch data from the selected API
- Load and integrate local dataset data
- Cache the API response to disk
- Output a summary report to the console

Example (conceptual):

```
API request successful
Cache hit: false
Records processed: 25
Report generated successfully
```

Exact output will vary based on the API and dataset you choose.

---

## Definition of Done (Required)

Stage 04 is **only complete** when **all** of the following are true:

1. Program runs without unhandled exceptions
2. Network failures are handled gracefully
3. API data is cached and reused correctly
4. No secrets exist in the repository
5. Output report is clear and consistent
6. Changes are **committed and pushed to GitHub**

### Required Git Commands (After Completion)

From the repository root:

```powershell
git status
git add stage-starters/stage_04
git commit -m "Complete Stage 04 - APIs and data integration"
git push
```

Do **not** proceed to Stage 05 without a clean commit and push.

---

## Troubleshooting

### API request fails immediately
- Verify your API key is set in the environment
- Confirm the API endpoint URL is correct
- Ensure a timeout is configured

### Cache not working
- Confirm cache file path is writable
- Check TTL logic is applied correctly

### Program exits with unclear error
- Add defensive exception handling around network calls
- Ensure error messages are printed clearly before exit

---

## What’s Next

After completing and committing Stage 04:

- Proceed to `stage-starters/stage_05`
- Focus on testing, packaging, and CI
- Treat this stage as the transition from scripting to production-quality tooling

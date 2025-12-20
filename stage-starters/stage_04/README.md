# Stage 4 — APIs, Networking Concepts, and Data Integration

## Overview
This stage focuses on building a small, production-style Python CLI that:
- Pulls data from a **public API** (example: weather, currency, etc.)
- Implements **networking best practices** (timeouts, retries/handling, clean failure modes)
- **Caches** results locally to reduce repeat requests and improve resilience
- Generates a simple **report** output
- Demonstrates **data integration** by merging API data with a local JSON/CSV dataset

This stage is intentionally written like a real internal tool: predictable CLI, safe defaults, and clean logs/errors.

---

## Learning Objectives
By the end of Stage 4, you should be able to:
- Build a robust API client using `urllib` or `requests` patterns (even if not using `requests`)
- Implement timeouts and defensive error handling for all network calls
- Cache API responses with TTL (time-to-live)
- Read and integrate local datasets (JSON/CSV)
- Produce a consistent report format suitable for logs, tickets, or dashboards

---

## Repository Layout
- stage_04/
- app/
- init.py
- main.py
- data/
- sample.json
- README.md

---

## Acceptance Criteria (Must Meet)
- All network calls include **timeouts** and **error handling**
- **No API keys** are committed to Git (use environment variables instead)
- Caching is implemented (file-based) and respects a TTL
- The CLI supports `--help` and provides clear usage/exit behavior

---

## Prerequisites
- Python 3.10+ recommended
- No external dependencies required unless you choose to add them (do not commit secrets)

---

## Configuration (No Secrets in Git)
If the API you choose requires a key, store it in an environment variable.

### Windows PowerShell
```powershell
setx API_KEY "your_key_here"

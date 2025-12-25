# Stage 04 — APIs, Networking Concepts, and Data Integration
## Connecting Your Programs to the World Wide Web

Welcome to **Stage 04**. In Stage 03 you mastered file I/O, JSON, and CLI tools. In this stage, your programs go online: you will fetch live data from the internet, handle network failures safely, cache API responses, and merge API data with local datasets.

By the end, you will build a **Data Fetcher Toolkit**—a production-style command-line tool that fetches:
- **Weather** (Open-Meteo)
- **Currency exchange rates** (Frankfurter / ECB reference rates)

And supports:
- timeouts + defensive error handling
- file-based caching with TTL (time-to-live)
- optional environment variables for configuration
- data integration (API snapshot + local JSON merged into a report)

---

## What You Will Learn

You will gain hands-on skill in:

- **HTTP fundamentals** (request/response, status codes)
- **APIs** (endpoints, query params, JSON responses)
- **HTTP requests with `urllib`** (standard library)
- **Network error handling** (HTTPError, URLError, timeouts)
- **Caching with TTL** (speed, reliability, rate-limit friendliness)
- **Environment variables** (secure config patterns; never commit secrets)
- **Data integration** (combining local + API data into a report)

---

## What You Will Build

A **Data Fetcher Toolkit** CLI that:

- Fetches current weather for a location (city or lat/lon)
- Retrieves current currency exchange rates
- Handles network errors gracefully (no crashes)
- Caches responses to disk with TTL
- Combines API data with a local JSON file into a single report
- Provides cache utilities (status / clear)

---

## Recommended Folder Layout

Inside `Stage_04_APIs_Networking_Data_Integration/`:

```text
Stage_04_APIs_Networking_Data_Integration/
├── README.md
├── main.py
├── data/
│   └── sample.json
└── .cache/
    └── (generated automatically)
```

**Notes:**
data/sample.json is your local dataset for the integration milestone.
.cache/ is created automatically for cached API responses.

### Milestones (Complete in Order)

1. Understand HTTP basics and make your first web request
2. Parse JSON data from an API response
3. Handle network errors with try/except
4. Implement timeouts for network requests
5. Build a file-based cache with TTL
6. Use environment variables for configuration (and keep secrets out of Git)
7. Build the Weather Fetcher tool
8. Build the Currency Converter tool
9. Create a data integration report (local + API)
10. Commit + push to GitHub

---

### Create Your Local Dataset

Create data/sample.json:
```json
{
  "asset_owner": "SOC Team",
  "environment": "lab",
  "tracked_locations": ["Seattle,WA", "Portland,OR"],
  "tracked_currencies": {
    "base": "USD",
    "symbols": ["EUR", "JPY"]
  }
}
```

### Configuration (Environment Variables)

This stage uses safe defaults and does not require an API key by default.
If you later use an API that requires a key, store it in an environment variable—never in code, and never committed.

Optional environment variables supported by main.py:

- STAGE4_TIMEOUT (default: 10)
- STAGE4_CACHE_TTL (default: 900)

**Windows PowerShell (examples)**

Temporary (current terminal session):
```powershell
$env:STAGE4_TIMEOUT="10"
$env:STAGE4_CACHE_TTL="900"
```

Permanent (user scope):
```powershell
setx STAGE4_TIMEOUT "10"
setx STAGE4_CACHE_TTL "900"
```

Restart your terminal after using setx.

macOS / Linux (examples):
```bash
export STAGE4_TIMEOUT="10"
export STAGE4_CACHE_TTL="900"
```

### How to Run

You can run Stage 04 in two supported ways.

Option A: Run from inside the Stage folder (Recommended)

Windows PowerShell:
```powershell
python .\main.py --help
```

macOS / Linux:
```bash
python ./main.py --help
```

Option B: Run from the repository root

Windows PowerShell:
```powershell
python stage-starters\Stage_04_APIs_Networking_Data_Integration\main.py --help
```

macOS / Linux:
```bash
python stage-starters/Stage_04_APIs_Ne
tworking_Data_Integration/main.py --help
```

---
### Commands

1) Fetch Weather

Fetch weather by city/state:
```powershell
python .\main.py fetch --source weather --location "Seattle,WA"
```

Fetch weather by lat/lon:
```powershell
python .\main.py fetch --source weather --location "47.6062,-122.3321"
```

Force refresh (ignore cache):
```powershell
python .\main.py fetch --source weather --location "Seattle,WA" --no-cache
```

Output raw JSON:
```powershell
python .\main.py fetch --source weather --location "Seattle,WA" --json
```

2) Fetch Currency

Get USD -> EUR and JPY:
```powershell
python .\main.py fetch --source currency --base USD --symbols "EUR,JPY"\
```

3) Data Integration Report (Local + API Snapshot)

Merge data/sample.json with a weather snapshot and write report.json:
```powershell
python .\main.py integrate --source weather --location "Seattle,WA" --input data\sample.json --output report.json
```

Merge with currency snapshot:
```powershell
python .\main.py integrate --source currency --base USD --symbols "EUR,JPY" --input data\sample.json 
```

4) Cache Utilities

Show cache status:
```powershell
python .\main.py cache status
```

Clear cache:
```powershell
python .\main.py cache clear
```
---

**Expected Output (Conceptual)**

Successful runs will:
- Fetch data from the API (or use cache)
- Print a clear summary report
- Optionally output raw JSON
- On integration, write a merged JSON report file

**Definition of Done (Required)**

Stage 04 is complete only when:
1. Program runs without unhandled exceptions
2. Network failures are handled gracefully (timeouts + error messages)
3. API data is cached and reused correctly (TTL enforced)
4. No secrets exist in the repository
5. Output is clear and consistent
6. Changes are committed and pushed to GitHub

---

Required Git Commands

From repository root:
```powershell
git status
git add stage-starters/Stage_04_APIs_Networking_Data_Integration
git commit -m "Complete Stage 04 - APIs and data integration"
git push
```

### What’s Next (Stage 05 Preview)

**Stage 05 will move into:**
- automated testing (pytest)
- mocking network calls
- packaging
- CI with GitHub Actions


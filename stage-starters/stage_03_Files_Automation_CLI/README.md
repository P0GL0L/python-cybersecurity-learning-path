# Stage 03 — Files, Automation, and Robust CLI Programs
## Reading, Writing, and Processing Files Like a Pro

Welcome to **Stage 03**. In Stage 02 you learned how to structure logic with functions and work with data in memory (lists/dicts). In this stage you take the next major step: **working with data stored in files** and building **professional command-line tools** with arguments, error handling, and meaningful exit codes. :contentReference[oaicite:1]{index=1}

By the end of this stage, you will build a **Log Analyzer** — a practical cybersecurity-style CLI utility that reads logs, summarizes events, and optionally exports results to JSON.

---

## What You Will Learn

You will gain hands-on skill in:

- **File reading** (open/read safely, line-by-line processing)
- **File writing** (create output files and reports)
- **Path handling** with `pathlib` (portable, cross-platform paths)
- **JSON** read/write with Python’s `json` module
- **Command-line interfaces** with `argparse` (`--help`, flags, typed args)
- **Exit codes** for professional automation behavior

---

## What You Will Build

A **Log Analyzer** command-line tool that:

- Reads and parses log files
- Counts and summarizes events (INFO/WARNING/ERROR)
- Optionally exports a report to **JSON**
- Supports CLI flags: `--input`, `--output`, `--verbose`, `--help`
- Handles common errors gracefully (missing file, unreadable file, bad data)
- Returns meaningful **exit codes** (success vs failure)

---

## Recommended Folder Layout

Inside `stage_03_Files_Automation_CLI/`:

```text
stage_03_Files_Automation_CLI/
├── README.md
├── main.py
├── data/
│   ├── sample.txt
│   ├── sample.log
│   └── config.json
└── output/
    └── (generated files go here)
```
**Notes:**
- data/ holds your input files.
- output/ is created/used by the program when writing results.

**Milestones (Complete in Order)**
**Milestone 1:** Read your first file and display its contents
**Milestone 2:** Write data to a new file
**Milestone 3:** Use pathlib to handle file paths properly
**Milestone 4:** Read and write JSON data
**Milestone 5:** Create a CLI with argparse (--help, --input, --output)
**Milestone 6:** Build Log Analyzer Part A (read and count log entries)
**Milestone 7:** Build Log Analyzer Part B (full tool with JSON export)
**Milestone 8:** Add exit codes and push to GitHub

### Create Your Sample Data Files
1) data/sample.txt

Create data/sample.txt with:
```text
Hello, this is my first text file!
Python can read every line.
This is line 3.
And this is the last line.
```

2) data/sample.log

Create data/sample.log with:
```text
2024-01-15 08:00:00 INFO Application started
2024-01-15 08:01:00 INFO User admin logged in
2024-01-15 08:02:00 WARNING Disk space low
2024-01-15 08:03:00 ERROR Database timeout
2024-01-15 08:04:00 INFO Backup completed
2024-01-15 08:05:00 WARNING High memory usage
2024-01-15 08:06:00 ERROR Network unreachable
2024-01-15 08:07:00 INFO User admin logged out
```

3) data/config.json (optional practice file)

Create data/config.json with:
```json
{
  "app_name": "Security Scanner",
  "version": "1.0.0",
  "max_threads": 4,
  "verbose": true
}
```
**How to Run (Log Analyzer)**

***From inside stage_03_Files_Automation_CLI/:***

Show help
```bash
python main.py --help
```

Analyze the sample log (no JSON output)
```bash
python main.py --input data/sample.log
```

Analyze with verbose output
```bash
python main.py --input data/sample.log --verbose
```

Analyze and export JSON report
```bash
python main.py --input data/sample.log --output output/report.json
```

***Expected Output (Example)***

When you run:
```bash
python main.py --input data/sample.log
```

**You should see a short summary similar to:**
- total lines read
- parsed lines
- invalid/malformed lines (if any)
- counts by level (INFO/WARNING/ERROR)
- first/last timestamp

**Success Checklist**

You are “done” with Stage 03 when you can confidently say:
- [ ] I can read a text file using with open(...) safely
- [ ] I can loop line-by-line and process entries
- [ ]  I can write output files (and create output folders)
- [ ]  I can use pathlib.Path for paths and joining
- [ ]  I can read/write JSON with json.load / json.dump
- [ ]  I can build a CLI with argparse and a useful --help
- [ ]  My log analyzer summarizes log levels correctly
- [ ]  My tool returns meaningful exit codes

### Git Completion (This is a MUST!)
```bash
git status
git add stage_03_Files_Automation_CLI
git commit -m "Complete Stage 03 - Files, CLI, Log Analyzer"
git push
```

---

### Next Stage Preview

**Stage 04 will move into networking and APIs (HTTP requests, timeouts, combining local + remote data).**

See you in the next stage. Keep up the good work!
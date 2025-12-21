# Stage 03 - Files, Automation, and Robust CLI Programs

## Goal

Build robust, production-style CLI programs focused on file handling and automation, such as:

- **Log Analyzer**: parse a log file, produce a summary report, export JSON
- **Backup/Sync Helper**: copy files by pattern with a dry-run mode

This stage emphasizes predictable CLI behavior, safe file I/O, and clear exit behavior.

---

## Acceptance Criteria

To complete Stage 03, your program must:

- Support CLI flags such as:
  - `--help`
  - `--input`
  - `--output`
  - `--verbose`
- Exit with meaningful status codes (success vs failure)
- Handle missing files and bad inputs gracefully (no crashes)
- Produce output that is clear and usable (report text and/or JSON)

---

## How to Run

You can run this stage in two supported ways.

### Option A: Run from the Repository Root (Recommended)

Windows PowerShell:
```powershell
python stage-starters\stage_03\app\main.py --help
```

macOS / Linux:
```bash
python stage-starters/stage_03/app/main.py --help
```

---

### Option B: Run from Inside the Stage Folder

If your terminal is already in `stage-starters/stage_03`:

Windows PowerShell:
```powershell
python app\main.py --help
```

macOS / Linux:
```bash
python app/main.py --help
```

---

## Example Usage (Typical)

These examples show the expected CLI pattern. Adjust file names to match your stage files and sample data.

Show help:
```powershell
python app\main.py --help
```

Analyze an input log and write a report:
```powershell
python app\main.py --input data\sample.log --output output\report.json --verbose
```

Dry-run a backup/sync operation:
```powershell
python app\main.py --input data\ --output backup\ --verbose
```

(macOS / Linux paths use `/` instead of `\`.)

---

## Definition of Done (Required)

Stage 03 is **only complete** when **all** of the following are true:

1. `--help` works and clearly describes usage
2. Required flags behave correctly (`--input`, `--output`, `--verbose`)
3. Missing input files and invalid paths are handled cleanly
4. Exit behavior is meaningful (success vs error)
5. Changes are **committed and pushed to GitHub**

### Required Git Commands (After Completion)

From the repository root:

```powershell
git status
git add stage-starters/stage_03
git commit -m "Complete Stage 03 - Files and robust CLI behavior"
git push
```

Do **not** proceed to Stage 04 without a clean commit and push.

---

## What’s Next

After completing and committing Stage 03:

- Proceed to `stage-starters/stage_04`
- Add networking best practices (timeouts, caching, clean failures)
- Continue treating your tooling like production code

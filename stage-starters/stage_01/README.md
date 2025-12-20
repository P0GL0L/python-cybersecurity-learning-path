# Stage 01 – Foundations and Setup

## Goal

Build a small **Hello Toolkit** command-line application that demonstrates:

- Basic Python syntax and structure
- Writing and calling multiple functions
- Menu-driven program flow
- Input validation (no crashes on bad input)
- Clean formatting, naming, and docstrings
- Basic logging concepts

This stage establishes the coding and workflow standards used throughout the rest of the learning path.

---

## Acceptance Criteria

To complete Stage 01, your program must:

- Implement **at least 5 small functions**
- Call all functions from a **single menu-driven script**
- Handle **invalid user input gracefully** (no unhandled exceptions)
- Run successfully from the command line
- Follow basic coding standards (readable names, spacing, comments/docstrings)

---

## Repository Location

This stage lives in:

```text
stage-starters/stage_01/
```

All coding work for this stage happens inside this folder.

---

## How to Run

You can run this stage in two supported ways.

### Option A: Run from the Repository Root (Recommended)

From the **repository root**:

```powershell
python stage-starters\stage_01\app\main.py --help
```

macOS / Linux:

```bash
python stage-starters/stage_01/app/main.py --help
```

---

### Option B: Run from Inside the Stage Folder

If your terminal is already in `stage-starters/stage_01`:

```powershell
python app\main.py --help
```

macOS / Linux:

```bash
python app/main.py --help
```

---

## Beginner Notes (Windows CMD Shortcut)

If you are new to the command line on Windows, you can open Command Prompt directly in the correct folder:

1. Open **File Explorer**
2. Navigate to:
   ```text
   C:\Users\<USERNAME>\python-cybersecurity-learning-path\stage-starters\stage_01
   ```
3. Click the address bar at the top
4. Type `cmd` and press **Enter**

A Command Prompt window will open already set to this folder. You can now run:

```powershell
python app\main.py
```

without using `cd`.

---

## Definition of Done (Required)

Stage 01 is **only complete** when **all** of the following are true:

1. The program runs without errors
2. Menu options work as expected
3. Invalid input does not crash the program
4. Code is readable and reasonably documented
5. Changes are **committed and pushed to GitHub**

### Required Git Commands (After Completion)

From the repository root:

```powershell
git status
git add stage-starters/stage_01
git commit -m "Complete Stage 01 - Foundations and Setup"
git push
```

Do **not** proceed to Stage 02 without a clean commit and push.

---

## What’s Next

After completing and committing Stage 01:

- Proceed to `stage-starters/stage_02`
- Follow the same workflow discipline
- Build on the foundations you established here

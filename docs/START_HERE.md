# START HERE – Python Cybersecurity Learning Path

Welcome.  
This document is the **operational entry point** for this repository.

If you are new here, **do not skip this file**.

This guide tells you:
- What you need installed
- How to open and navigate the repository
- Where to start coding
- How stages work
- When a stage is complete
- When you are allowed to move forward

---

## 1. What You Need Installed

### Required (All Platforms)
- **Python 3.10 or newer**
  - Verify:
    ```bash
    python --version
    ```
    or
    ```bash
    python3 --version
    ```
- **Git**
  - Verify:
    ```bash
    git --version
    ```
- **Visual Studio Code (VS Code)**

### Supported Operating Systems
- Windows 10 / 11
- macOS
- Linux

No prior cybersecurity experience is required.  
Basic comfort using a terminal is helpful.

---

## 2. Clone the Repository

From a terminal, PowerShell, or CMD:

```bash
git clone https://github.com/P0GL0L/python-cybersecurity-learning-path.git
cd python-cybersecurity-learning-path
```

### 3. Open the Repository in VS Code (Required)

1. Open VS Code
2. Click File → Open Folder
3. Select the python-cybersecurity-learning-path folder
4. Click Select Folder / Open

You should now see folders on the left panel in VS Code.
If you do not see folders, you did not open the correct directory.

### 4. Understand the Repository Structure (Important)

You will work in three main folders:
- docs/
- stage-starters/
- capstone/

### What each folder is for

docs/ → READ HERE
- Explanations
- Concepts
- Guidance
- Markdown files only (no runnable code)

stage-starters/ → START CODING HERE
- One folder per stage
- This is where you edit and run Python files
- Stage 1 begins here

capstone/ → DO THIS LAST
- Final project
- Do not open until all stages are complete

### 5. How This Learning Path Works

This repository is intentionally structured as progressive stages.

Rules:
1. Complete stages in order
2. Do not skip ahead
3. Work only inside the current stage folder
4. Each stage builds on the previous one

You must commit and push after every completed stage
Skipping stages will cause later work to break or make no sense.

### 6. START STAGE 1 (Do This First)
You start in Stage 1, not in docs/ and not in capstone/.

In VS Code:
1. Expand stage-starters/
2. Expand stage-1 (or similarly named Stage 1 folder)
3. Open the first Python file
4. Read the comments at the top
5. Follow the instructions written in the file

Running the file

From a terminal in the stage folder:

Option A (most systems)
```
python main.py
```

Option B (if needed)
```bash
Copy code
python3 main.py
```
You may also use VS Code’s Run button if configured correctly.

### 7. Using docs/ (When and Why)

You do not start in docs/.

You use docs/ only when a stage file tells you to.

Example:

“Read the explanation in docs/…”

At that point:
1. Open docs/
2. Read the referenced file
3. Return to the stage code

Otherwise, stay in stage-starters/.

### 8. Definition of “Stage Complete” (Strict Rule)

A stage is only complete when all of the following are true:
1. The program runs without errors
2. Required functionality behaves as expected
3. You understand what the code is doing
4. Your changes are committed and pushed to GitHub

Required Git Workflow (After Each Stage)
From the repository root:
```bash
git status
git add .
git commit -m "Complete Stage X"
git push
```
Do not proceed to the next stage without a clean commit and push.
This mirrors real-world software and cybersecurity workflows.

### 9. Moving to the Next Stage

You may move forward only after:
- The current stage runs correctly
- You have committed and pushed your work

Then:
1. Open the next stage folder
2. Repeat the same process

### 10. Common Troubleshooting

“Nothing to commit, working tree clean”
- You did not modify or save files
- Verify you edited the correct stage folder

Python command not found
- Try python3 instead of python
- Verify Python is installed and in PATH

Permission or path errors
- Confirm you are inside the correct stage directory
- Use cd to navigate correctly

### 11. When to Start the Capstone

You may begin the capstone only after:
- All stages are completed
- Each stage has its own commit
- You understand RBAC, logging, hashing, and file handling

Capstone location:
capstone/

Instructions are provided inside that folder.

### 12. What to Do Right Now

1. Return to the repository root
2. Navigate to:
```bash
stage-starters/stage-1
```
3. Open the Python file
4. Begin Stage 1

### Final Note

This repository is designed to build real cybersecurity-focused development habits:
- Incremental progress
- Auditability via commits
- Defensive thinking from the start
If something feels strict, that is intentional.








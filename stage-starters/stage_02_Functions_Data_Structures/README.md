# Stage 02 - Functions, Data Structures, and Menus
## Building Reusable Code and Working with Data (Python Cybersecurity Learning Path)

### Stage 02 Overview
Stage 01 taught you how to write basic Python that runs.
Stage 02 is about writing Python that is reusable, reliable, and structured like real tools.

In this stage you will:
- Write **functions that return values** (not just print)
- Understand core **data types**
- Convert between data types safely (casting)
- Use **try/except** for robust input validation (no crashes)
- Learn the basics of **lists** and **dictionaries**
- Build two practical tools:
  - **Temperature Converter**
  - **Password Strength Checker (security challenge)**

---

## What You Will Build

### Tool 1: Temperature Converter
A menu-driven converter that:
- Converts **Fahrenheit → Celsius**
- Converts **Celsius → Fahrenheit**
- Uses safe numeric input handling with `try/except`
- Displays clean output formatting (e.g., `:.2f`)

### Tool 2: Password Strength Checker (Security Challenge)
A password checker that:
- Scores password strength from **0 to 6**
- Evaluates:
  - length (8+ and 12+)
  - uppercase letters
  - lowercase letters
  - numbers
  - special characters
- Returns **multiple values** from a function (score + feedback)
- Uses a **dictionary** to map score → rating (cleaner than long if/elif)

---

## Folder Structure
```
stage_02_Functions_Data_Structures/
└── app/
└── main.py
```


---

## How to Run

You can run this stage in two supported ways.

### Option A (Recommended): Run from the Repository Root

PowerShell (Windows):
```powershell
python stage_02_Functions_Data_Structures\app\main.py
```

macOS / Linux:
```bash
python app/main.py
```

### Success Checklist (Stage 02 Complete When…)

**Functions and Return Values**

- You can explain the difference between print() and return

- You can call a function and store its returned value in a variable

**Data Types and Conversion**

- You can identify and explain:

 - str, int, float, bool

- You can safely convert user input to numeric types

**Robust Input Validation**

- Your program does not crash when the user enters invalid input

- Invalid input is handled using try/except and re-prompts the user

**Lists and Dictionaries**

- You can explain what lists and dictionaries are used for

- Your program uses a dictionary for password score → rating mapping

**Temperature Converter**

- Fahrenheit → Celsius works correctly

- Celsius → Fahrenheit works correctly

Results display with appropriate decimal formatting

**Password Strength Checker**

- Correctly checks length requirements

- Correctly detects uppercase, lowercase, digits, and special characters

- Provides clear improvement suggestions when needed

**Code Quality**

- Proper indentation (4 spaces)

- Functions are used instead of repeated code

**Git and GitHub**

- All changes committed to Git

- Changes pushed to GitHub

- Git Commands for Completion

### From your repository root folder:
```powershell
git status
git add stage_02_Functions_Data_Structures
git commit -m "Complete Stage 02 - Functions, Data Structures, and Menus"
git push
```

### ***Do not proceed to Stage 03 without a clean commit and push.***

**What’s Next (Stage 03 Preview)**

In Stage 03, you will learn to work with files and build more advanced automation tools:
- File I/O: read/write files
- Log analysis (security-relevant)
- CLI arguments (flags like --help)
- JSON data handling
- Automation tools that process data automatically


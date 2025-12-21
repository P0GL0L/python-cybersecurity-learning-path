> Short on time? See `README_QUICK_START.md` for the fastest way to begin.

# Quick Start — Python Cybersecurity Learning Path

This is the **fastest way to begin** using this repository.

If you only read one file before starting, read this one.

---

## 🚀 Try It Right Now (5 Minutes)

**Want to see what you'll build?** Run your first security tool before even cloning the repo:

### Your First Security Script: Password Strength Checker

Create a file called `password_checker.py`:
```python
import re
import getpass

def check_password_strength(password):
    """Check password strength and return score (0-100)."""
    score = 0
    feedback = []
    
    # Length check
    length = len(password)
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 15
        feedback.append("Consider using 12+ characters")
    else:
        feedback.append("Password too short! Use at least 12 characters")
    
    # Character variety checks
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append("Add lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append("Add uppercase letters")
    
    if re.search(r'\d', password):
        score += 15
    else:
        feedback.append("Add numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 20
    else:
        feedback.append("Add special characters")
    
    # Determine strength
    if score >= 80:
        strength = "STRONG 💪"
    elif score >= 60:
        strength = "MODERATE ⚠️"
    else:
        strength = "WEAK ❌"
    
    return score, strength, feedback

# Main program
print("=" * 50)
print("PASSWORD STRENGTH CHECKER")
print("=" * 50)
print("\nYour password is not stored or transmitted.\n")

password = getpass.getpass("Enter password to check: ")

score, strength, feedback = check_password_strength(password)

print(f"\n{'=' * 50}")
print(f"Strength: {strength}")
print(f"Score: {score}/100")
print(f"{'=' * 50}")

if feedback:
    print("\n💡 Improvement suggestions:")
    for tip in feedback:
        print(f"   • {tip}")
else:
    print("\n✅ Excellent password!")

print(f"\n{'=' * 50}")
```

**Run it:**
```bash
python password_checker.py
```

**What you just built:**
- ✅ Secure password input (no echo to screen)
- ✅ Pattern matching with regex
- ✅ Security best practices
- ✅ User-friendly output

**This is what you'll learn in Stage 01!**

---

## 📚 Ready for the Full Learning Path?

Continue below for the complete structured approach...

---

## 1) Prerequisites

- Python **3.10+** installed
- Git installed
- Basic command-line access (PowerShell, CMD, Terminal)

Verify Python:
```bash
python --version
```

---

## 2) Clone the Repository
```bash
git clone https://github.com/P0GL0L/python-cybersecurity-learning-path.git
cd python-cybersecurity-learning-path
```

---

## 3) Read the Onboarding Rules (Required)

Before writing any code, read:
```
docs/START_HERE.md
```

This explains:
- how stages work
- how to run code
- when you must commit and push

Skipping this causes confusion later.

---

## 4) Begin the Learning Path

Start with **Stage 01**:
```
stage-starters/stage_01
```

Read the stage README and follow it exactly.

Run code using either method:
- from repo root, or
- from inside the stage folder

---

## 5) Stage Completion Rule (Important)

A stage is **not complete** until:

- code runs correctly
- README instructions are followed
- changes are committed
- changes are pushed to GitHub

After completing a stage:
```bash
git status
git add .
git commit -m "Complete Stage XX"
git push
```

Then move to the next stage.

---

## 6) Track Your Progress

Use the checklist:
```
docs/LEARNER_PROGRESS_CHECKLIST.md
```

If an item is not checked, the stage is not done.

---

## 7) Final Integration (Capstone)

After completing all stages:
```
capstone/
```

This is where earlier skills are integrated into a final, review-ready tool.

---

## 8) Choose Documentation Based on Your Goal

When finished, see:
```
audience-docs/
```

- Learners: `learner_overview.md`
- Interviews: `interview_talking_points.md`
- Employers: `employer_README.md`
- Instructors: `instructor_notes.md`

---

## You're Ready

If you:
- follow stages in order
- commit and push consistently
- use the checklist

This repository will tell a **clear, professional learning story** — even if you are not present to explain it.
# Instructor Notes  
Python Cybersecurity Learning Path

This document is intended for **instructors, evaluators, and reviewers** who are assessing this repository as part of a course, capstone, or structured learning activity.

It explains **how the repository is meant to be evaluated**, what signals to look for, and what successful completion looks like.

---

## Repository Intent

This repository is a **stage-based learning path**, not a single project.

Each stage introduces a specific technical boundary and requires:
- working code
- documentation
- disciplined Git workflow
- incremental improvement

Progression and consistency matter more than feature count.

---

## How This Repository Should Be Evaluated

### 1. Start With Structure, Not Code

Before reviewing individual scripts, verify that the repository contains:

- Root `README.md` (project overview)
- `docs/START_HERE.md` (onboarding and workflow rules)
- `docs/LEARNER_PROGRESS_CHECKLIST.md` (completion criteria)
- `stage-starters/` with numbered stages (01–06)
- `audience-docs/` with presentation-focused documentation

Missing or incomplete documentation indicates incomplete submission.

---

### 2. Evaluate Stages in Order

Stages are designed to be completed **sequentially**.

Each stage should include:
- a stage-specific `README.md`
- clear acceptance criteria
- run instructions
- a “Definition of Done” section
- evidence of commit and push

Skipping stages or completing them out of order undermines the learning intent.

---

### 3. Use Git History as a Primary Signal

This repository enforces a **commit + push gate after every stage**.

Reviewers should:
- Inspect commit messages for clarity
- Confirm that commits align with stage boundaries
- Look for incremental progress rather than bulk uploads
- Verify that no generated artifacts (cache files, build outputs) are tracked

Git history is part of the assessment.

---

## What to Look for by Stage

### Stages 01–02 (Foundations)
- Basic Python syntax and structure
- Menu-driven CLI behavior
- Input validation
- Clean program flow
- Readable, maintainable code

### Stage 03 (Files and Automation)
- Safe file handling
- Predictable CLI flags
- Graceful failure modes
- Meaningful exit behavior

### Stage 04 (APIs and Data Integration)
- Defensive network calls (timeouts, error handling)
- No secrets committed to Git
- Environment variable usage
- Caching and data reuse

### Stage 05 (Testing and CI)
- Meaningful unit tests
- Mocking of external dependencies
- Passing CI pipeline
- Packaging discipline

### Stage 06 (Portfolio Tool)
- Integration of prior concepts
- Clear CLI behavior
- Professional documentation
- Ability to explain design decisions

---

## What This Repository Is *Not*

For clarity, this repository is **not** intended to be:
- a penetration testing toolkit
- a production security product
- a feature-complete application
- a copy-paste coding exercise

It is a **learning artifact** focused on professional software development habits.

---

## Evaluation Emphasis

When grading or reviewing, prioritize:
- correctness over cleverness
- clarity over optimization
- discipline over speed
- explanation over volume

A smaller, well-documented solution is preferred over a large, brittle one.

---

## Completion Criteria (Instructor Checklist)

Before marking this repository complete:

- [ ] All stages present and sequential
- [ ] Stage READMEs complete and accurate
- [ ] Learner progress checklist fully satisfied
- [ ] Git history shows clear stage progression
- [ ] No cache or build artifacts tracked
- [ ] Learner can verbally explain each stage

---

## Final Notes

This repository is designed to support **discussion-based evaluation**.  
Learners should be able to explain:
- why stages exist
- what problems each stage solves
- what tradeoffs were made
- what they would improve next

The ability to explain decisions is as important as the code itself.

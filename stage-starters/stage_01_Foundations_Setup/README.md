# Stage 01 — Foundations and Setup  
## Building Your First Python CLI Toolkit (Hello Toolkit)

**Python Cybersecurity Learning Path**  
**Audience:** Complete beginners (no prior programming experience required)

Welcome. In this stage you will learn the fundamental building blocks of Python and use them to build a real, working command-line program: the **Hello Toolkit**.

---

## What You Will Learn and Why It Matters

Stage 01 is your foundation. Think of it like learning the alphabet before writing sentences. These basics will be reused constantly in later cybersecurity stages.

### What You Will Build: “Hello Toolkit”
By the end of this stage, you will have created a command-line program that:

- Displays a menu of options to the user  
- Performs different actions based on what the user chooses  
- Handles mistakes gracefully (doesn’t crash on unexpected input)  
- Uses **at least 5 different functions** (reusable pieces of code)

### Skills You Will Gain (and why it matters)
- **Writing and running Python code** — Python is widely used for security tools and automation  
- **Creating functions** — security tools are built from small reusable components  
- **Building command-line interfaces (CLI)** — most professional security tooling runs in a terminal  
- **Handling user input safely** — input validation is a core security concept  
- **Using Git (version control)** — professional development requires change tracking

---

## The Milestones Approach

This stage is broken into small milestones so you can see progress clearly and build confidence.

**Your Stage 01 Milestones**
1. Run your first Python program (**Hello, World!**)  
2. Write your first function  
3. Create a function that interacts with users  
4. Build a simple menu system  
5. Complete the Hello Toolkit with error handling  
6. Save your work to GitHub (commit + push)

---

## Part 2 — Understanding the Basics: What is Python?

### What is a Programming Language?
A programming language is how you give instructions to a computer. Computers require very precise instructions (spelling, punctuation, formatting all matter).

**Analogy: A recipe**  
Code is like a recipe: step-by-step instructions that must be followed exactly.

### Why Python?
Python is a strong first language because it is:
- Readable (often looks like plain English)
- Beginner-friendly (you can build useful programs quickly)
- Powerful (used across industry)
- Security-focused (common for scripting, analysis, and automation)

### Key Vocabulary (you will see these terms often)
- **Code:** instructions you write for the computer  
- **Script:** a Python file (ends in `.py`)  
- **Function:** a reusable block of code that does one job  
- **Variable:** a named container for data (a “labeled box”)  
- **CLI:** command-line interface (text-based interaction)  
- **Terminal:** where you type commands (Command Prompt / PowerShell / Terminal)  
- **String:** text data in quotes like `"Hello"`  
- **Loop:** code that repeats  
- **Error:** a mistake that stops a program  
- **Docstring:** a short description inside a function explaining what it does  

---

## Part 3 — Milestone 1: Your First Program (“Hello, World!”)

### Step-by-step
1. Open your terminal:
   - **Windows:** Start → type `cmd` → Enter  
   - **Mac:** Command + Space → type `terminal` → Enter  
   - **Linux:** Ctrl + Alt + T  

2. Navigate to your Stage 01 folder (example):
   ```bash
   cd path/to/python-cybersecurity-learning-path/stage-starters/stage_01

3. Create a file named hello.py in your code editor.

4. Add this code:
```python
print("Hello, World!")
```
5. Run it:
```bash
python hello.py
```

You should see:
```python
Hello, World!
```

## What You Just Did (Quick Breakdown)
- `print` = a built-in function that displays output  
- `("...")` = parentheses pass information into the function  
- `"Hello, World!"` = a string (text in quotes)

## Common Mistakes (Avoid These)
- `print(Hello, World!)` — missing quotes  
- `Print("Hello, World!")` — Python is case-sensitive  
- `print "Hello, World!"` — missing parentheses  

## Practice
- Change the message to your own  
- Add a second `print()` on the next line  
- Try printing a number without quotes:  
   ```python
  print(42)
   ```
---

# Part 4 — Milestone 2: Understanding Functions

## What Is a Function?

A function is a reusable block of code that performs a specific task. Instead of repeating code, you write it once and call it when needed.

**Analogy: a vending machine**  
You provide input (selection), it performs a process, and gives output. You don’t need to know the internal details—just how to use it.

---

## Anatomy of a Function (Example)

```python
def greet_user(name):
    """Print a friendly greeting."""
    print(f"Hello, {name}! Welcome to the tool.")
```

### Key Parts

- `def` starts a function definition  
- `greet_user` is the function name  
- `(name)` is a parameter (input the function needs)  
- `:` ends the header line  
- Docstring `"""..."""` describes the function  
- Indentation (4 spaces) defines the function body  
- `f"..."` is an f-string that inserts variables using `{}`  

---

## Milestone 2 Exercise: Write and Run Your First Function

Create `my_first_function.py`:

```python
# My first function

def say_hello():
    """Print a simple hello message."""
    print("Hello! This message came from my function!")

# Call the function
say_hello()
```

Run:

```bash
python my_first_function.py
```

---

## Practice: Add More Functions

```python
def say_goodbye():
    """Print a goodbye message."""
    print("Goodbye! Thanks for visiting!")

def show_welcome_banner():
    """Display a decorative welcome banner."""
    print("=" * 30)
    print("   Welcome to My Program!")
    print("=" * 30)

show_welcome_banner()
say_hello()
say_goodbye()
```

---

# Part 5 — Milestone 3: Getting Information from Users with `input()`

Programs become more useful when they interact with users.

## How `input()` Works

```python
user_name = input("What is your name? ")
print(f"Nice to meet you, {user_name}!")
```

- `input(...)` displays a prompt and waits  
- Whatever the user types becomes a **string**  
- `user_name = ...` stores it in a variable  

---

## Milestone 3 Exercise: Interactive Function

Create `interactive_greeting.py`:

```python
def greet_user():
    """Ask for the user's name and greet them."""
    name = input("What is your name? ")
    print(f"Hello, {name}! Welcome to the Hello Toolkit!")

greet_user()
```

**Important:** `input()` always returns text (a string), even if the user types numbers.

---

# Part 6 — Making Decisions with `if / elif / else`

Programs often need to make choices based on conditions.

## Basic `if` Example

```python
age = 18

if age >= 18:
    print("You are an adult.")
```

## Handling Multiple Options

```python
choice = input("Enter 1, 2, or 3: ")

if choice == "1":
    print("You chose option one!")
elif choice == "2":
    print("You chose option two!")
elif choice == "3":
    print("You chose option three!")
else:
    print("Invalid choice. Please enter 1, 2, or 3.")
```

### Critical Beginner Rule: `=` vs `==`

- `=` assigns a value  
  ```python
  x = 5
  ```
- `==` compares values  
  ```python
  x == 5
  ```

### Common Comparison Operators

- `==` equal to  
- `!=` not equal to  
- `>` greater than  
- `<` less than  
- `>=` greater than or equal  
- `<=` less than or equal  

---

# Part 7 — Milestone 4: Loops and Menus

To build a menu-driven tool, you need a loop that keeps running until the user exits.

## The `while` Loop (Concept)

A `while` loop repeats as long as its condition is `True`.

---

## Milestone 4 Exercise: Basic Menu Loop

```python
def show_menu():
    """Display the menu options."""
    print("\n=== Hello Toolkit ===")
    print("1. Say Hello")
    print("2. Say Goodbye")
    print("3. Exit")

running = True

while running:
    show_menu()
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        print("Hello there!")
    elif choice == "2":
        print("Goodbye, see you later!")
    elif choice == "3":
        print("Thanks for using the toolkit!")
        running = False
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
```

### What’s Happening

- `running = True` controls the loop  
- `while running:` repeats until set to `False`  
- Invalid input is handled without crashing  
- `\n` adds spacing for readability  

---

# Stage 01 Completion Checklist (Milestone 5–6 Targets)

Check off each item before moving on:

- [ ] Program runs without crashing  
- [ ] Menu displays with at least 5 options  
- [ ] Each menu option performs a different action  
- [ ] Program keeps running until the user chooses exit  
- [ ] Invalid choices produce a helpful message  
- [ ] At least 5 functions with descriptive names  
- [ ] Each function includes a docstring  
- [ ] Variables are meaningfully named  
- [ ] Code committed to Git  
- [ ] Code pushed to GitHub  

---

# What’s Next: Stage 02 Preview

Stage 02 will build on these foundations by introducing:

- Data structures (lists and dictionaries)  
- More complex functions with return values  
- More data types (numbers, strings, booleans)  
- A more sophisticated menu-driven application  


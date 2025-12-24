"""
Stage 1 - Foundations and Setup
Hello Toolkit (menu-driven CLI)

Meets Stage 01 README requirements:
- Menu-driven CLI with at least 5 options (+ Exit)
- Uses 5+ functions with docstrings
- Keeps running until user exits
- Handles invalid input gracefully
"""

from __future__ import annotations

import argparse


TOOL_VERSION = "1.0.0"


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    p = argparse.ArgumentParser(description="Stage 1 - Foundations and Setup (Hello Toolkit)")
    p.add_argument("--demo", action="store_true", help="Run a short demo path")
    p.add_argument("--version", action="store_true", help="Print the program version and exit")
    return p


def show_menu() -> None:
    """Display the Hello Toolkit menu options."""
    print("\n=== Hello Toolkit ===")
    print("1. Say Hello")
    print("2. Personalized Greeting")
    print("3. Show Welcome Banner")
    print("4. Echo Back Text")
    print("5. Quick Info (Why Stage 01 matters)")
    print("6. Exit")


def get_choice() -> str:
    """Prompt the user for a menu choice and return cleaned input."""
    return input("Enter your choice (1-6): ").strip()


def say_hello() -> None:
    """Print a simple hello message."""
    print("Hello there!")


def personalized_greeting() -> None:
    """Ask for the user's name and print a personalized greeting (with validation)."""
    name = input("What is your name? ").strip()
    if not name:
        print("Invalid input: name cannot be empty.")
        return
    print(f"Hello, {name}! Welcome to the Hello Toolkit!")


def show_welcome_banner() -> None:
    """Display a decorative welcome banner."""
    print("=" * 34)
    print("   Welcome to the Hello Toolkit")
    print("=" * 34)


def echo_back_text() -> None:
    """Ask the user for text and echo it back (with basic validation)."""
    text = input("Type something and I will echo it back: ").strip()
    if not text:
        print("Invalid input: text cannot be empty.")
        return
    print(f'You said: "{text}"')


def quick_info() -> None:
    """Print a short explanation of why Stage 01 concepts matter."""
    print("Stage 01 builds the core skills used in later cybersecurity tooling:")
    print("- Functions: reusable building blocks for tools")
    print("- CLI interaction: most security tools run in terminals")
    print("- Input validation: safer, more reliable programs")
    print("- Loops/menus: keep tools running until the user exits")


def handle_choice(choice: str) -> bool:
    """
    Execute the selected menu option.

    Returns:
        True to keep running; False to exit.
    """
    if choice == "1":
        say_hello()
        return True
    elif choice == "2":
        personalized_greeting()
        return True
    elif choice == "3":
        show_welcome_banner()
        return True
    elif choice == "4":
        echo_back_text()
        return True
    elif choice == "5":
        quick_info()
        return True
    elif choice == "6":
        print("Thanks for using the toolkit!")
        return False
    else:
        print("Invalid choice. Please enter a number from 1 to 6.")
        return True


def run_toolkit_loop() -> int:
    """Run the main menu loop until the user chooses to exit."""
    running = True
    while running:
        show_menu()
        choice = get_choice()
        running = handle_choice(choice)
    return 0


def run_demo() -> int:
    """Run a short demo path (kept for compatibility with the starter)."""
    name = input("Enter your name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return 1
    print(f"Hello, {name}! Welcome to Stage 1.")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Program entry point."""
    args = build_parser().parse_args(argv)

    if args.version:
        print(f"Stage 1 Tool Version: {TOOL_VERSION}")
        return 0

    if args.demo:
        return run_demo()

    return run_toolkit_loop()


if __name__ == "__main__":
    raise SystemExit(main())

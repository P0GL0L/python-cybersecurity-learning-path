
"""
Stage 02 - Functions, Data Structures, and Menus
Building Reusable Code and Working with Data

This stage builds two tools:
1) Temperature Converter (F <-> C) with robust input validation
2) Password Strength Checker (0-6 scoring + rating dictionary + improvement feedback)
"""

# ---------------------------
# Temperature Converter
# ---------------------------

def fahrenheit_to_celsius(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * (5 / 9)


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32


def get_temperature(prompt):
    """Safely get a temperature value from the user."""
    while True:
        raw_input = input(prompt).strip()
        try:
            temp = float(raw_input)
            return temp
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 98.6).")


def run_temperature_converter():
    """Run the temperature converter with user interaction."""
    print()
    print("=== Temperature Converter ===")
    print("a) Fahrenheit to Celsius")
    print("b) Celsius to Fahrenheit")
    print()

    mode = input("Choose a conversion (a/b): ").strip().lower()

    if mode not in ("a", "b"):
        print("Invalid selection. Returning to main menu.")
        return

    temp = get_temperature("Enter the temperature value: ")

    if mode == "a":
        result = fahrenheit_to_celsius(temp)
        print(f"{temp}°F = {result:.2f}°C")
    else:
        result = celsius_to_fahrenheit(temp)
        print(f"{temp}°C = {result:.2f}°F")


# ---------------------------
# Password Strength Checker
# ---------------------------

def has_uppercase(password):
    """Check if password contains uppercase."""
    for char in password:
        if char.isupper():
            return True
    return False


def has_lowercase(password):
    """Check if password contains lowercase."""
    for char in password:
        if char.islower():
            return True
    return False


def has_digit(password):
    """Check if password contains a digit."""
    for char in password:
        if char.isdigit():
            return True
    return False


def has_special(password):
    """Check if password contains special characters."""
    special_chars = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
    for char in password:
        if char in special_chars:
            return True
    return False


def calculate_password_strength(password):
    """
    Calculate password strength score (0-6).
    Returns multiple values: (score, feedback_list)
    """
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if len(password) >= 12:
        score += 1

    # Check character types
    if has_uppercase(password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z)")

    if has_lowercase(password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z)")

    if has_digit(password):
        score += 1
    else:
        feedback.append("Add numbers (0-9)")

    if has_special(password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%...)")

    return score, feedback


def get_strength_rating(score):
    """Return a rating based on the score."""
    ratings = {
        0: "Very Weak",
        1: "Very Weak",
        2: "Weak",
        3: "Fair",
        4: "Good",
        5: "Strong",
        6: "Very Strong"
    }
    return ratings.get(score, "Unknown")


def run_password_checker():
    """Run the password strength checker."""
    print()
    print("=== Password Strength Checker ===")
    password = input("Enter a password to check: ")

    if not password:
        print("No password entered.")
        return

    score, feedback = calculate_password_strength(password)
    rating = get_strength_rating(score)

    print()
    print(f"Password Strength: {rating} ({score}/6)")

    if feedback:
        print()
        print("Suggestions to improve:")
        for suggestion in feedback:
            print(f"  - {suggestion}")


# ---------------------------
# Menu System
# ---------------------------

def show_main_menu():
    print()
    print("=== Stage 02 Menu ===")
    print("1) Temperature Converter")
    print("2) Password Strength Checker")
    print("3) Exit")


def get_menu_choice():
    """Robust menu choice validation using try/except."""
    while True:
        raw = input("Select an option (1-3): ").strip()
        try:
            choice = int(raw)
            if choice in (1, 2, 3):
                return choice
            print("Invalid selection. Enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Enter a number (1-3).")


def main():
    while True:
        show_main_menu()
        choice = get_menu_choice()

        if choice == 1:
            run_temperature_converter()
        elif choice == 2:
            run_password_checker()
        else:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()

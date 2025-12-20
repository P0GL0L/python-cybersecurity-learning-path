"""Stage 02 - Functions, Data Structures, and Menus.

Step 1: Build the menu loop with input validation.
"""

def show_menu() -> None:
    print()
    print("=== Stage 2 Menu ===")
    print("1) Say Hello")
    print("2) Temperature COnverter (F <-> C)")
    print("3) Exit")

def get_choice() -> str:
    return input("Select an option (1-3): ").strip()

def prompt_for_name() -> str:
    while True:
        name = input("Enter your name: ").strip()
        if name:
            return name
        print("Name cannot be empty. Try again.")

def build_greeting(name: str) -> str:
    return f"Hello, {name}!"

def prompt_for_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Try again (example: 98.6).")

def f_to_c(f: float) -> float:
    return (f - 32) * (5 / 9)

def c_to_f(c: float) -> float:
    return (c * (9 / 5)) + 32

def run_temp_converter() -> None:
    print()
    print("Temperature Converter")
    print("a) Fahrenheit to Celsius")
    print("b) Celsius to Fahrenheit")

    mode = input("Choose a conversion (a/b): ").strip().lower()
    if mode not in ("a", "b"):
        print("Invalid selection. Returning to main menu.")
        return

    value = prompt_for_float("Enter the temperature value: ")

    if mode == "a":
        result = f_to_c(value)
        print(f"{value} F = {result:.2f} C")
    else:
        result = c_to_f(value)
        print(f"{value} C = {result:.2f} F")

def main() -> None:
    while True:
        show_menu()
        choice = get_choice()

        if choice == "1":
            name = prompt_for_name()
            greeting = build_greeting(name)
            print(greeting)
        elif choice == "2":
            run_temp_converter()
        elif choice == "3":
            print("Exciting...")
            break            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

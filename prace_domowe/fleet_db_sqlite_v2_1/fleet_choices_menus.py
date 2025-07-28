

def choice_menu(prompt: str, variable):
    print(f"\n{prompt}\n{'-' * len(prompt)}")

    if isinstance(variable, dict):
        for key, val in variable.items():
            print(f"{key}: {val}")
        valid_inputs = variable.keys()

    elif isinstance(variable, list):
        for item in variable:
            print(f"- {item}")
        valid_inputs = variable

    else:
        raise TypeError("Variable musi być słownikiem lub listą")

    while True:
        choice = input("Wpisz swoją odpowiedź: ").strip().lower()
        if choice in valid_inputs:
            return choice
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


def yes_or_not_menu(prompt: str) -> bool:
    # Funkcja zwraca False/True
    print(f"\n{prompt}\n{'-' * len(prompt)}")
    while True:
        choice = input("Wybierz (tak/nie): ").strip().lower()
        if choice in {"tak", "t", "yes", "y"}:
            return True
        elif choice in {"nie", "n", "no"}:
            return False
        else:
            print("\nNieprawidłowy wybór. Wpisz tak lub nie.")


from timeit import timeit

text = "tak"
choices_tuple = ("tak", "t", "yes", "y")
choices_set = {"tak", "t", "yes", "y"}

print("tuple:", timeit("text in choices_tuple", globals=globals(), number=1_000_000))
print("set  :", timeit("text in choices_set", globals=globals(), number=1_000_000))
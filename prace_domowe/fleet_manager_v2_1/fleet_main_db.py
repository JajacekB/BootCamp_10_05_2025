from fleet_manager_user import (
    login_user, register_user, change_password, add_seller,
    add_client, remove_client, get_clients, remove_seller)
from fleet_manager_fleet import (
    get_vehicle, borrow_vehicle, return_vehicle,
    add_vehicle, remove_vehicle, pause_vehicle,
    borrow_vehicle_to_client, return_vehicle_from_client,
    return_vehicle_by_id
)



def logoff_user():
    """Wylogowanie i ponowne logowanie z przekierowaniem do odpowiedniego menu."""
    print("\n🔒 Wylogowano.")
    main()


def handle_choice(options: dict):
    """Obsługuje wybór użytkownika z mapy opcji."""
    choice = input("Wybierz opcję: ").strip()
    action = options.get(choice)
    if callable(action):
        action()
    else:
        print("❌ Zły wybór. Spróbuj ponownie.")

def start_menu():
    while True:
        print("""
=== SYSTEM WYPOŻYCZANIA POJAZDÓW ===

0. Zamknij program
1. Zaloguj się
2. Zarejestruj się

""")
        choice = input("Wybierz opcję (0-2): ").strip()

        if choice == "1":
            user = login_user()
            if user:
                return user
        elif choice == "2":
            register_user()
            # Po rejestracji możesz np. automatycznie zalogować lub wrócić do menu startowego
        elif choice == "0":
            print("Do widzenia!")
            exit(0)
        else:
            print("❌ Niepoprawny wybór, spróbuj ponownie.")
0
def menu_client(user):
    while True:
        print(f"""\n=== MENU KLIENTA ===
0. Wyloguj się
1. Przeglądaj pojazdy
2. Wypożycz pojazd
3. Zwróć pojazd
4. Zmień hasło""")
        handle_choice({
            "0": logoff_user,
            "1": get_vehicle,
            "2": lambda: borrow_vehicle(user),
            "3": lambda: return_vehicle(user),
            "4": lambda: change_password(user)
        })


def menu_seller(user):
    while True:
        print(f"""\n=== MENU SPRZEDAWCY ===
0. Wyloguj się
1. Dodaj klienta
2. Usuń klienta
3. Przeglądaj klientów
4. Dodaj pojazd
5. Usuń pojazd
6. Przeglądaj pojazdy
7. Wypożycz pojazd klientowi
8. Zwróć pojazd od klienta
9. Zwróć pojazd po ID
10. Zmień hasło""")
        handle_choice({
            "0": logoff_user,
            "1": add_client,
            "2": remove_client,
            "3": get_clients,
            "4": add_vehicle,
            "5": remove_vehicle,
            "6": get_vehicle,
            "7": borrow_vehicle_to_client,
            "8": return_vehicle_from_client,
            "9": return_vehicle_by_id,
            "10": lambda: change_password(user)
        })


def menu_admin(user):
    while True:
        print(f"""\n=== MENU ADMINA ===
0. Wyloguj się
1. Dodaj sprzedawcę
2. Usuń sprzedawcę
3. Dodaj klienta
4. Usuń klienta
5. Przeglądaj klientów
6. Dodaj pojazd
7. Usuń pojazd
8. Przeglądaj pojazdy
9. Wypożycz pojazd klientowi
10. Zwróć pojazd od klienta
11. Zwróć pojazd po ID
12. Zmień hasło""")
        handle_choice({
            "0": logoff_user,
            "1": lambda: add_seller(),
            "2": lambda: remove_seller(role="seller"),
            "3": lambda: add_client(),
            "4": lambda: remove_client(role="client"),
            "5": get_clients,
            "6": add_vehicle,
            "7": remove_vehicle,
            "8": get_vehicle,
            "9": borrow_vehicle_to_client,
            "10": return_vehicle_from_client,
            "11": return_vehicle_by_id,
            "12": lambda: change_password(user)
        })


def main():
    while True:
        user = start_menu()
        if not user:
            # np. jeśli login_user zwróci None lub anulujesz logowanie, wróć do start_menu
            continue

        menus = {
            "client": menu_client,
            "seller": menu_seller,
            "admin": menu_admin
        }
        menu_function = menus.get(user.role)
        if menu_function:
            menu_function(user)
        else:
            print(f"❌ Nieznana rola użytkownika: {user.role}")


if __name__ == "__main__":
    main()
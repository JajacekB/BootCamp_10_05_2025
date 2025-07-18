from fleet_promo_db import  show_dynamic_promo_banner
from fleet_database import SessionLocal
from fleet_manager_user import (
    login_user, register_user, add_seller,
    add_client, remove_user, get_clients, update_profile)
from fleet_manager_fleet import (
    get_vehicle, rent_vehicle, return_vehicle,
    add_vehicles_batch, remove_vehicle, rent_vehicle_for_client,
    repair_vehicle
)
from fleet_overdue_db import check_overdue_vehicles
session = SessionLocal()


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
        show_dynamic_promo_banner(session)
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

def menu_client(user):
    while True:
        show_dynamic_promo_banner(session)
        print(f"""\n=== MENU KLIENTA ===
0. Wyloguj się
1. Przeglądaj pojazdy
2. Wypożycz pojazd
3. Zwróć pojazd
4. Zaktualizuj profil
""")
        handle_choice({
            "0": logoff_user,
            "1": lambda: get_vehicle(only_available=True),
            "2": lambda: rent_vehicle(user),
            "3": lambda: return_vehicle(user),
            "4": lambda: update_profile(user)
        })


def menu_seller(user):
    while True:
        print(f"""\n=== MENU SPRZEDAWCY ===
0. Wyloguj się
1. Dodaj nowego klienta
2. Usuń klienta
3. Przeglądaj klientów
4. Dodaj nowy pojazd
5. Usuń pojazd z użytkowania
6. Przeglądaj pojazdy
7. Wypożycz pojazd klientowi
8. Zwróć pojazd
9. Oddaj pojazd do naprawy
10. Aktualizuj profil
""")
        handle_choice({
            "0": logoff_user,
            "1": add_client,
            "2": lambda: remove_user(role="client"),
            "3": get_clients,
            "4": add_vehicles_batch,
            "5": remove_vehicle,
            "6": lambda: get_vehicle(),
            "7": lambda: rent_vehicle_for_client(user),
            "8": lambda: return_vehicle(user),
            "9": repair_vehicle,
            "10": lambda: update_profile(user)
        })


def menu_admin(user):
    while True:
        print(f"""\n=== MENU ADMINA ===
0. Wyloguj się 
1. Dodaj nowego sprzedawcę
2. Usuń sprzedawcę
3. Dodaj nowego klienta
4. Usuń klienta
5. Przeglądaj klientów
6. Dodaj nowy pojazd
7. Usuń pojazd z użytkowania
8. Przeglądaj pojazdy 
9. Wypożycz pojazd klientowi
10. Zwróć pojazd
11. Oddaj pojazd do naprawy
11. Aktualizuj profil
""")
        handle_choice({
            "0": logoff_user,
            "1": add_seller,
            "2": lambda: remove_user(role="seller"),
            "3": add_client,
            "4": lambda: remove_user(role="client"),
            "5": get_clients,
            "6": add_vehicles_batch,
            "7": remove_vehicle,
            "8": lambda: get_vehicle(),
            "9": lambda: rent_vehicle_for_client(user),
            "10": lambda: return_vehicle(user),
            "11": repair_vehicle,
            "12": lambda: update_profile(user)
        })


def main():
    while True:
        user = start_menu()
        if not user:
            # np. jeśli login_user zwróci None lub anulujesz logowanie, wróć do start_menu
            continue

        # Uruchamiamy automaty do sprawdzania przeterminowanych pojazdów tylko raz po zalogowaniu
        if user.role in ("seller", "admin"):
            check_overdue_vehicles(user, session)

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
    try:
        main()
    finally:
        session.close()
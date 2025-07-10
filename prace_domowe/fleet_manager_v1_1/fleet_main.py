from fleet_manager import FleetManager

fleet = FleetManager.load_file()

print("\nProgram ---Fleet Manager Turbo--- służy do zarządzania małą wypożyczalnią pojazdów.")

while True:
    print("""\nMożesz zrobić takie czynności:
    0. Zakończyć program
    1. Dodać pojazd
    2. Wyświetlić wszystkie pojazdy
    3. Wyświetlić filtrowane
    """)

    activity = input("\n Wybierz opcję (0-3): ")

    match activity:
        case "1":
            fleet.add_vehicle()
            fleet.save_file()

        case "2":
            fleet.get_all_vehicles()

        case "3":
            status = input("\nWpisz status (all, available, rented): ").strip().lower()

            # Informacja o automatycznym sortowaniu
            if status == "available":
                print("Sortowanie będzie ustawione automatycznie na 'id' (po ID pojazdu).")
            elif status == "rented":
                print("Sortowanie będzie ustawione automatycznie na 'date' (po dacie zwrotu).")
            else:
                print("Sortowanie domyślnie po ID pojazdu.")

            vehicle_type = input("Wpisz typ pojazdu (all, car, scooter, bike): ").strip().lower()

            min_price_input = input("Minimalna cena za dobę (ENTER aby pominąć): ").strip()
            max_price_input = input("Maksymalna cena za dobę (ENTER aby pominąć): ").strip()

            min_price = float(min_price_input) if min_price_input else None
            max_price = float(max_price_input) if max_price_input else None

            vehicles = fleet.get_vehicles(
                status=status,
                vehicle_type=vehicle_type,
                min_price=min_price,
                max_price=max_price
            )

            if not vehicles:
                print("\nBrak pojazdów spełniających kryteria.")
            else:
                for v in vehicles:
                    print(v)

        case "0":
            fleet.save_file()
            print("\nKoniec programu.")
            break

        case _:
            print("\nZły wybór. Spróbuj jeszcze raz")


# if isinstance(user, Admin):
#     admin_menu()
# elif isinstance(user, Seller):
#     seller_menu()
# elif isinstance(user, Client):
#     client_menu()
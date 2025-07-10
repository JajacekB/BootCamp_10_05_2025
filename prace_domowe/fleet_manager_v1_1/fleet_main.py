from fleet_manager import FleetManager

fleet = FleetManager.load_file()

print("\nProgram ---Fleet Manager Turbo--- służy do zarządzania małą wypożyczalnią pojazdów.")

while True:
    print("""\nMożesz zrobić takie czynności:
    0. Zakonmczyć program
    1. Dodać pojazd
    2. Wyświetlić dostępne pojazdy
    3. Sam nie wiem co
        """)

    activity = input("\n Wybierz opcję (0-3): ")

    match activity:
        case "1":
            fleet.add_vehicle()
            fleet.save_file()

        case "2":
            fleet.get_all_vehicles()

        case "3":
            status = input("Wpisz status (all, available, rented): ").strip().lower()
            vehicle_type = input("Wpisz typ pojazdu (all, car, scooter, bike): ").strip().lower()
            sort_by = input("Sortuj wg (id, date): ").strip().lower()

            vehicles = fleet.get_vehicles(status=status, vehicle_type=vehicle_type, sort_by=sort_by)
            if not vehicles:
                print("Brak pojazdów spełniających kryteria.")
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
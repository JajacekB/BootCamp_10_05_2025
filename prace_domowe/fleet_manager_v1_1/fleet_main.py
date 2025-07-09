from fleet_vehicle import Car, Scooter, Bike
from fleet_manager import FleetManager



fleet = FleetManager()

print("\n Program ---Fleet Manager Turbo--- służy do zarządzania małą wypożyczalnią pojazdów.")

while True:
    print("""\nMożesz zrobić takie czynności:
    0. Zakonmczyć program
    1. Dodać pojazd
    2. Wyświetlić dostępne pojazdy
        """)

    activity = input("\n Wybierz opcję (0-2): ")

    match activity:
        case "1":
            fleet.add_vehicle()

        case "2":
            fleet.get_all_vehicles()

        case "0":
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
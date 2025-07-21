from fleet_models_db import Vehicle, RentalHistory, RepairHistory
from datetime import date, datetime, timedelta


def check_overdue_vehicles(user, session):
    if user.role not in ("seller", "admin"):
        return  # tylko dla seller i admin

    print("\n=== Sprawdzanie przeterminowanych zwrotów pojazdów i powrotów z naprawy ===")

    today = date.today()
    overdue_vehicles = session.query(Vehicle).filter(
        Vehicle.return_date.isnot(None),
        Vehicle.return_date < today,
        Vehicle.is_available == False
    ).order_by(Vehicle.return_date.asc()).all()

    if not overdue_vehicles:
        print("Brak przeterminowanych zwrotów.\n")
        return

    for vehicle in overdue_vehicles:
        print(f"\nPojazd: {vehicle.brand} {vehicle.vehicle_model} (ID: {vehicle.vehicle_id})")
        print(f"Planowany zwrot: {vehicle.return_date}")
        answer = input("Czy pojazd został zwrócony? (tak/nie): ").strip().lower()

        if answer in ("tak", "t", "yes", "y"):
            actual_return_str = input("Podaj datę zwrotu (DD-MM-YYYY): ").strip()
            try:
                actual_return_date = datetime.strptime(actual_return_str, "%d-%m-%Y").date()
            except ValueError:
                print("Niepoprawny format daty, pomijam ten pojazd.")
                continue

            # Oblicz opóźnienie
            delay_days = (actual_return_date - vehicle.return_date).days
            delay_days = max(0, delay_days)

            # Szukamy powiązanej historii wypożyczenia (ostatniej rezerwacji tego pojazdu i tego wypożyczającego)
            rental = session.query(RentalHistory).filter_by(
                vehicle_id=vehicle.id,
                user_id=vehicle.borrower_id
            ).order_by(RentalHistory.end_date.desc()).first()

            repair = session.query(RepairHistory).filter_by(
                vehicle_id=vehicle.id,
                mechanic_id=vehicle.borrower_id
            ).order_by(RepairHistory.end_date.desc()).first()

            if rental is None and repair is None:
                print("Nie znaleziono historii wypożyczenia i naprawy tego pojazdu.")
                continue

            elif rental and repair:
                print(f"\n⚠️ UWAGA!!! Pojazd ID: {vehicle.id} figuruje jako wypożyczony i w naprawie!")

                choice = input(
                    f"\n Czy chcesz:"
                    f"\n (I) Ignorować ten wpis"
                    f"\n (N) anulować Naprawę"
                    f"\n (W) anulować Wypożyczenie"
                    f"\n Twój wybór: "
                ).strip().lower()

                if choice == "i":
                    break

                elif choice == "n":
                    repair.end_date = date.today()
                    session.commit()
                    print("✅ Naprawa została zakończona.")
                    break

                elif choice == "w":
                    rental.end_date = date.today()
                    session.commit()
                    print("✅ Wypożyczenie zostało zakończone.")
                    break

                else:
                    print("Nieprawidłowy wybór. Wpisz I, N lub W.")
                session.commit()

            elif rental is None and repair:
                # Aktualizacja pojazdu - powrót z naprawy i czyszczenie danych
                repair.end_date = actual_return_date
                vehicle.is_available = True
                vehicle.borrower_id = None
                vehicle.return_date = None
                session.commit()
                print(f"Pojazd {vehicle.vehicle_model} został zwrócony i jest dostępny.")

            else:
                # Obliczamy dodatkową opłatę za opóźnienie (100% ceny za dzień)
                additional_fee = delay_days * vehicle.cash_per_day
                print(f"Dodatkowa opłata za {delay_days} dni opóźnienia: {additional_fee:.2f} zł")

                # Aktualizujemy end_date w RentalHistory (przedłużenie wypożyczenia)
                planed_return = vehicle.return_date or rental.end_date
                if actual_return_date > planed_return:
                    print(f"Przedłużam wypożyczenie z {rental.end_date} do {actual_return_date}")
                    rental.end_date = actual_return_date

                    # Aktualizujemy całkowity koszt (bez rabatów, bo to dodatkowe dni)
                    base_days = (rental.end_date - rental.start_date).days + 1  # liczymy dni od początku do nowej daty
                    new_total_cost = base_days * vehicle.cash_per_day
                    rental.total_cost = new_total_cost

                    # Aktualizujemy fakturę powiązaną z rezerwacją (Invoice)
                    invoice = rental.invoice
                    if invoice:
                        invoice.amount = new_total_cost
                        print(f"Zaktualizowano kwotę faktury do: {invoice.amount:.2f} zł")
                    else:
                        print("Brak faktury powiązanej z tą rezerwacją, nie można zaktualizować kwoty.")

                # Aktualizacja pojazdu - zwrot i czyszczenie danych
                vehicle.is_available = True
                vehicle.borrower_id = None
                vehicle.return_date = None

                session.commit()
                print(f"Pojazd {vehicle.vehicle_model} został zwrócony i jest dostępny.")

        else:
            print("Pojazd nadal wypożyczony, sprawdzimy go ponownie jutro.")

    print("\n=== Koniec sprawdzania przeterminowanych zwrotów ===\n")

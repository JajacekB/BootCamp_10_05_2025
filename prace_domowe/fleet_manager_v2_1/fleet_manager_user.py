from fleet_database import Session
from fleet_models_db import User, Vehicle
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import or_, not_
import bcrypt
import getpass

def get_users_by_role(role_name: str, session):
    """Zwraca listę użytkowników o podanej roli."""
    return session.query(User).filter_by(role=role_name).all()

def login_user():
    # session = Session()
    while True:
        print("\n=== LOGOWANIE DO SYSTEMU ===")
        login_or_email = input("\nLogin: ").strip()
        password = input("Hasło: ").strip()

        with Session() as session:
            user = session.query(User).filter(
                (User.login == login_or_email) | (User.email == login_or_email)
            ).first()

            if not user:
                print("\nNie znaleziono użytkownika.")
            elif not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                print("\nBłędne hasło.")
            else:
                print(f"\nZalogowano jako {user.first_name} {user.last_name} ({user.role})")
                return user  # Wylogowanie = powrót None albo exit

        print(f"\nCo chcesz zrobić?\n"
                f"1. Spróbować jeszcze raz.\n"
                f"2. Zarejestrować się.\n"
                f"3. Anulować logowanie."
        )
        choise = input("\nWybierz opcje (1 - 3): ").strip()
        if choise == "1":
            continue
        elif choise == "2":
            return register_user()
        else:
            print("\nAnulowano logowanie.")
            return None

def register_user(role="client", auto=False):
    """
    Rejestracja nowego użytkownika.
    :param role: 'client' lub 'seller'
    :param auto: jeśli True, login i hasło są generowane automatycznie (dla sprzedawcy).
    """
    print(f"\n=== REJESTRACJA NOWEGO {'SPRZEDAWCY' if role == 'seller' else 'KLIENTA'} ===")

    print("\nPodaj dane potrzebne do rejestracji")
    first_name = input("Imię: ").strip().capitalize()
    last_name = input("Nazwisko: ").strip().capitalize()
    phone = input("Nr telefonu: ").strip()
    email = input("Email: ").strip()
    address = input("Adres zamieszkania: ").strip()

    if auto and role == "seller":
        with Session() as session:
            count = session.query(User).filter_by(role="seller").count()
            seller_number = str(count + 1).zfill(2)
            login = f"seller{seller_number}"
            raw_password = login  # np. seller01
            password_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
            print(f"\nUtworzono login: {login} | hasło: {raw_password}")
    else:
        login = input("Login: ").strip()
        while True:
            password = input("Hasło: ").strip()
            password_confirm = input("Potwierdź hasło: ").strip()
            if password != password_confirm:
                print("\n❌ Hasła nie są takie same. Spróbuj ponownie.")
            else:
                break
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        login=login,
        phone=phone,
        email=email,
        password_hash=password_hash,
        address=address,
        role=role
    )

    with Session() as session:
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            print(f"\n✅ Użytkownik {login} został dodany pomyślnie.")
            return new_user
        except IntegrityError:
            session.rollback()
            print("\n❌ Login, telefon lub email już istnieje. Spróbuj z innymi danymi.")
            return None

def add_client():
    return register_user(role="client")

def add_seller():
    return register_user(role="seller", auto=True)

def remove_user(role="client"):
    while True:
        with Session() as session:
            users = session.query(User).filter_by(role=role).all()
            if not users:
                print(f"\nℹ️ Brak użytkowników o roli '{role}' w bazie.")
                return

            print(f"\n📋 Lista użytkowników o roli '{role}':")
            for user in users:
                print(f" - ID: {user.id}, Login: {user.login}, Imię: {user.first_name} {user.last_name}")

        user_input = input(f"\nPodaj login albo ID użytkownika o roli '{role}', którego chcesz usunąć: ").strip()

        with Session() as session:
            query = session.query(User).filter(
                or_(
                    User.login == user_input,
                    User.id == int(user_input) if user_input.isdigit() else -1
                )
            ).first()

            if not query:
                print("\n❌ Nie znaleziono użytkownika o podanym loginie lub ID.")
            elif query.role == "admin":
                print("\n❌ Nie można usunąć użytkownika o roli 'admin'.")
            elif query.role != role:
                print(f"\n❌ Użytkownik {query.login} ma rolę '{query.role}', a nie '{role}'.")
            else:
                active_rentals = session.query(Vehicle).filter_by(
                    borrower_id=query.id, is_available=False).count()
                if active_rentals > 0:
                    print(f"\n🚫 Nie można usunąć użytkownika {query.login}, ponieważ ma aktywne wypożyczenie.")
                else:
                    confirm = input(f"\n✅ Znaleziono użytkownika: \n{query}\n"
                                    f"Czy chcesz go usunąć? (TAK/NIE)? ").strip().lower()
                    if confirm in ("tak", "t", "yes", "y"):
                        session.delete(query)
                        session.commit()
                        print(f"\n✅ Użytkownik {query.login} został usunięty z bazy.")
                    else:
                        print("\n❌ Anulowano usunięcie użytkownika.")

        # Pytanie o kolejne usunięcie
        while True:
            again = input("\nCzy chcesz usunąć kolejnego użytkownika? (TAK/NIE): ").strip().lower()
            if again in ("tak", "t", "yes", "y"):
                break  # wraca do początku głównej pętli
            elif again in ("nie", "n", "no"):
                print("🔙 Powrót do menu.")
                return
            else:
                print("❌ Niepoprawna odpowiedź. Wpisz 'tak' lub 'nie'.")

def get_clients():
    print(">>> Przeglądanie klientów <<<")
    client_status = input(
        "\nW jaki sposób chcesz przeglądać klientów?"
        "\n(A) - wszyscy"
        "\n(T) - tylko z wypożyczeniem"
        "\n(N) - tylko bez wypożyczenia"
        "\n\nTwój wybór: "
    ).strip().lower()
    with Session() as session:
        if client_status in ("a", "wszyscy"):
            clients = (
                session.query(User)
                .filter(User.role == "client")
                .order_by(User.last_name, User.first_name)
                .all()
            )
            if not clients:
                print("\n🚫 Brak klientów spełniających podane kryteria.")
                return
            print("\n>>> WSZYSCY KIENCI WYPOŻYCZALNI <<<\n")
            for client in clients:
                print(client, "\n")
        elif client_status in ("t", "tak", "z", "z wypożyczeniem"):
            borrower_ids = (
                session.query(Vehicle.borrower_id)
                .filter(Vehicle.is_available == False, Vehicle.borrower_id != None)
                .distinct()
                .all()
            )
            borrower_ids = [row[0] for row in borrower_ids]
            clients = (
                session.query(User)
                .filter(User.id.in_(borrower_ids), User.role == "client")
                .order_by(User.last_name, User.first_name)
                .all()
            )
            if not clients:
                print("\n🚫 Brak klientów spełniających podane kryteria.")
                return
            print("\n\n>>> KLIENCI Z WYPOŻYCZENIEM <<<\n")
            for client in clients:
                print(client, "\n")
            while True:
                choice = input(
                    f"\nCo chcesz teraz zrobić:"
                    f"\n(P) - Powrót do menu główneg"
                    f"\n(W) - Wyświetl szczegóły użytkownika"
                    f"\n\nTwój wybór: "
                ).strip().lower()
                if choice not in ["p", "powrót", "w", "wyświetl"]:
                    print("\nZły wybór, spróbuj jeszcze raz.")
                    continue
                if choice in ["p", "powrót"]:
                    return
                if choice in ["w", "wyświetl"]:
                    while True:
                        user_input = input("\nPodaj ID klient: ").strip()
                        try:
                            id_input = int(user_input)
                            break  # poprawna liczba, wychodzimy z pętli
                        except ValueError:
                            print("❌ Podaj poprawny numer ID (liczbę całkowitą).")
                    client = session.query(User).filter(User.id == id_input).first()
                    if not clients:
                        print("❌ Nie znaleziono użytkownika o podanym ID.")
                        return
                    vehicles = session.query(Vehicle).filter(Vehicle.borrower_id == id_input).all()
                    print("\n", client, ":")
                    for vehicle in vehicles:
                        print("\n      ", vehicle)
        elif client_status in ("n", "nie", "bez", "bez wypożyczenia"):
            borrowed_ids = (
                session.query(Vehicle.borrower_id)
                .filter(Vehicle.is_available == False, Vehicle.borrower_id != None)
                .distinct()
                .all()
            )
            borrower_id_list = [id for (id,) in borrowed_ids]
            clients = (
                session.query(User)
                .filter(
                    User.role == "client",
                    not_(User.id.in_(borrower_id_list))
                )
                .order_by(User.last_name, User.first_name)
                .all()
            )
            if not clients:
                print("\n🚫 Brak klientów spełniających podane kryteria.")
                return
            print("\n\n>>> KLIENCI BEZ WYPOŻYCXZENIA <<<\n")
            for client in clients:
                print(client, "\n")

def change_password():
    print(">>> [MOCK] Zmiana hasła...")

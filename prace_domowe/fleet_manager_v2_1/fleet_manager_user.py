from pandas.io.clipboard import is_available

from fleet_database import Session
from fleet_models_db import User, Vehicle
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import or_
import bcrypt
import getpass


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

def register_user():
    # session = Session()
    print("\n=== REJESTRACJA DO SYSTEMU ===")

    print("\nPodaj dane potrzebne do zalogowania")
    first_name = input("Imię: ").strip().capitalize()
    last_name = input("Nazwisko: ").strip().capitalize()
    login = input("Login: ").strip()
    phone = input("Nr telefon:").strip()
    email = input("Email: ").strip()
    address = input("Adres zamieszkania: ").strip()

    while True:
        # password = getpass.getpass("Hasło: ").strip()
        password = input("Hasło: ").strip()
        # password_confirm = getpass.getpass("Potwierdź hasło: ").strip()
        password_confirm = input("Potwierdź hasło: ").strip()

        if password != password_confirm:
            print("\nHasła nie są takie same, Spróbój ponownie.")
        else:
            break

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        login=login,
        phone=phone,
        email=email,
        password_hash=hashed_pw,
        address=address,
        role="client"
    )

    with Session() as session:
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            print(f"\nUżytkownik {login} został zarejestrowany pomyślnie.")
            return new_user
        except IntegrityError:
            session.rollback()
            print("\nLogin lub email już istnieje. Spróbuj z innymi danymi.")
            return None

def add_client():
    print(">>> [MOCK] Dodawanie klienta...")

def remove_client():
    while True:
        client_input = input("\nPodaj login albo ID klienta, którego chcesz usunąć z bazy: ").strip()

        with Session() as session:
            query = session.query(User).filter(
                or_(
                    User.login == client_input,
                    User.id == int(client_input) if client_input.isdigit() else -1
                )
            ).first()

            if not query:
                print("\n❌ Nie znaleziono klienta o podanym loginie lub ID.")
            elif query.role == "admin":
                print("\n❌ Nie można usunąć użytkownika o roli admin.")
            else:
                active_rentals = session.query(Vehicle).filter_by(borrower_id=query.id, is_available=False).count()
                if active_rentals > 0:
                    print(f"\n🚫 Nie można usunąć klienta {query.login}, ponieważ ma aktywne wypożyczenie.")
                else:
                    while True:
                        choice = input(f"\n✅ Znaleziono klienta: \n{query}\nCzy chcesz go usunąć? (TAK/NIE)? ").strip().lower()
                        if choice in ("tak", "t", "yes", "y"):
                            session.delete(query)
                            session.commit()
                            print(f"\n✅ Klient:\n{query}\nzostał usunięty z bazy.")
                            return  # koniec funkcji po usunięciu
                        elif choice in ("nie", "n", "no"):
                            print("\n❌ Anulowano usunięcie klienta.")
                            return  # koniec funkcji po anulowaniu
                        else:
                            print("\n❌ Niepoprawna odpowiedź. Wpisz 'tak' lub 'nie'.")
                            continue

        # Pytanie, czy chce próbować jeszcze raz
        while True:
            retry = input("\nCzy chcesz spróbować ponownie? (TAK/NIE): ").strip().lower()
            if retry in ("tak", "t", "yes", "y"):
                break  # wracamy do początku pętli
            elif retry in ("nie", "n", "no"):
                print("Powrót do menu.")
                return  # wychodzimy z funkcji
            else:
                print("Niepoprawna odpowiedź. Wpisz 'tak' lub 'nie'.")


def change_password():
    print(">>> [MOCK] Zmiana hasła...")

def add_seller():
    print(">>> [MOCK] Dodawanie sprzedawcy...")

def remove_seller():
    print(">>> [MOCK] Usuwanie sprzedawcy...")

def get_clients():
    print(">>> [MOCK] Przeglądanie klientów...")

def log_off_user():
    print(">>> [MOCK] Wylogowano.")







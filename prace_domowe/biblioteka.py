# stworzyc system zarzadzania biblioteką klasa Book
# dodnie ksiazki, wypozyczenie ksiazki, zwracanie ksiązki
# obsłużyc błedy
# Dodac Library i usera

from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author, lib_num, available=True, borrower=None, return_date=None):
        """
        Inicjacja obiektu Book
        :param title: Tytuł książki
        :param author: Autor książki
        :param lib_num: Numer katalogowy
        :param available: Czy książka jest dostępna (domyslnie True)
        :param borrower: Kto wypożyczył książkę (domyslnie None)
        :param return_date: Do kiedy trzeba zwrócić książkę (może kiedyś automatycznie)
        :return:
        """

        self.title = title
        self.author = author
        self.lib_num = lib_num
        self.available = available
        self.borrower = borrower
        self.return_date = return_date

    def __str__(self):
        status = "Dostępna" if self.available else f"Wypożyczona przez: {self.borrower}, do {self.return_date}"
        return f"{self.title} - {self.author} (Nr: {self.lib_num}) [{status}]"


class User:
    def __init__(self, user_id, name, borrowed=None):
        """
        Inicjacja użytkownika bibiloteki
        :param user_id: Numer uzytkownika
        :param name: Imię i nazwisko
        :param borrowed: Lista wypożyczonych książek
        """

        self.user_id = user_id
        self.name = name
        self.borrowed = borrowed if borrowed is not None else []

    def __str__(self):
        if self.borrowed:
            books = ', '.join(book.title for book in self.borrowed)
        else:
            books = "Brak wypożyczonych książek"
        return f"\n(Nr: {self.user_id}). {self.name} [Wypożyczone: {books}]"


class Library:
    def __init__(self):
        """
        Inicjacja pustej Biblioteki
        """

        self.books = []
        self.users = []
        self.borrow_books =[]


    def add_book(self):
        title = input("\nPodaj tytuł książki: ").strip()
        author = input("Podaj autora ksiązki: ").strip()
        lib_num = input("Podaj numer katalogowy: ").strip().lower()

        for book in self.books:
            if book.lib_num == lib_num:
                print(f"\nKsiążka z numerem {lib_num} już istnieje.")
                return

        book = Book(title, author, lib_num)
        self.books.append(book)

        print("\nOperacja dodawania książki zakończona sukcesem")

    def add_user(self):
        user_id = input("\nNadaj numer biblioteczny użytkownika (Numer karty): ")

        for user in self.users:
            if user.user_id == user_id:
                print(f"\nUżytkownik z numerem {user_id} już istnieje.")
                return

        name = input("\nPodaj imię i nazwisko użytkownika: ")

        user = User(user_id, name)
        self.users.append(user)

        print("\nOperacja dodawania użytkownika zakończona sukcesem")

    def borrow_book(self, user_id, lib_num, return_date):
        user_id = input("\nPodaj numer karty uzytkownika: ").strip()
        lib_num = input("Podaj numer katalogowy książki: ").strip().lower()

        # wyszukiwanie użytkownika
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user is None:
            print(f"\nUżutkownik {user_id} nie istnieje.")
            return

        # Wyszukiwanie książki
        book = next((b for b in self.books if b.lib_num == lib_num), None)
        if book is None:
            print(f"\nKsiążka z numerem {lib_num} nie istnieje")
            return

        # Czy książka jest dostepna
        if not book.available:
            print(f"\nKsiążka '{book.title}' jest wypozyczona do {return_date}.")
            return

        # Czy użytkownik nie przekroczył limitu ksiązek
        if len(user.borrowed) >= 4:
            print(f"\n{user.name} nie może wypozyczyć więcej niż cztery ksiązki.")

        # automat do ustawiania daty zwrotu.
        today = datetime.now()
        return_date = today + timedelta(weeks=4)
        return_date_str = return_date.strftime("%y-%m-%d")

        # ustwaienie flag dla wypożyczonej ksiązki
        book.available = False
        book.borrower = user.name
        book.return_date = return_date_str

        # dodawanie książki użytkownikowi
        user.borrowed.append(book)

        print(f"\nKsiążka '{book.title}' została wypożyczona przez {user.name}. Termin zwrotu: {return_date_str}.")

    def return_book(self, user_id, lib_num, return_date):
        lib_num = input("\nPodaj numer katalogowy książki: ").strip().lower()

        # Wyszukiwanie książki
        book = next((b for b in self.books if b.lib_num == lib_num), None)
        if book is None:
            print(f"\nnNie znaleziono książki o numerze {lib_num}.")
            return

        # Sprawdzanie czy książka jest wypozyczona
        if book.available:
            print(f"\nKsiążka '{book.title}' nie jest wypozyczona")
            return

        # Wyszukiwanie użytkownika
        user = next((u for u in self.users if u.name == book.borrower), None)
        if user is None:
            print(f"f\nNie znaleziono uzytkownika {book.borrower}.")
            return

        # Ustawienie flag dla zwróconej książki
        book.available = True
        book.borrower = None
        book.return_date = None

        # Usuwanie ksiązki użytkownikowi
        if book in user.borrowed:
            user.borrowed.remove(book)
        else:
            print(f"\nUwaga: użytkownik {user.name} nie ma tej książki na liście wypożyczeń.")

        print(f"\nKsiążka '{book.title}' o numerze katalogowym {lib_num} została zwrócona przez {user.name}.")

    def get_all_books(self):
        if not self.books:
            print("\nW bibliotece nie ma jeszcze książek.")
        else:
            print("\nLista książek:\n")
            for book in self.books:
                print(book)

    def get_available_books(self):
        for book in self.books:
            if book.available:
                print(book)

    def get_borrowed_books(self):
        print()
        borrowed_books = [book for book in self.books if not book.available]

        if not borrowed_books:
            print("\nŻadna książka nie jest aktualnie wypożyczona.")
        else:
            print("\nLista wypożyczonych książek:\n")
            for book in borrowed_books:
                print(book)

    def find_book(self):
        title = input("\nPodaj poszukiwaną książkę: ").strip().casefold()
        book = next((b for b in self.books if b.title.casefold() == title), None)

        if book is None:
            print(f"\nnNie znaleziono książki: '{title}'.")
            return
        else:
            print(f"\nZnaleziono książkę:\n{book}")

    def find_user(self):
        name = input("\nPodaj imię i nazwisko osoby: ").strip().casefold()
        user = next((u for u in self.users if u.name.casefold() == name), None)

        if user is None:
            print(f"\nNie znaleziono użytkownika: '{name}'.")
            return
        else:
            print(f"\nZnaleziono użytkownika :\n{user}")



book_aa1001 = Book("Pan Tadeusz", "Adam Mickiewicz", "aa1001")

print(book_aa1001)

user_1001 = User("1001", "Jan Kowalski")

print(user_1001)

book_aa1002 = Book("Dziady", "Adam Mickiewicz", "book_aa1002", False, "0001", "2025-07-15")

print(book_aa1002)
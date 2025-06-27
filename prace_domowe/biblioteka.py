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

    def borrow_book(self, book):
        if len(self.borrowed) >= 4:
            print(f"\n{self.name} Nie może wypożyczyć więcej niż 4 książki.")
            return
        self.borrowed.append(book)

    def return_book(self, book):
        if book in self.borrowed:
            self.borrowed.remove(book)
        else:
            print(f"\n{self.name} nie wypożyczył tej książki")

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
        book = next((w for w in self.books if w.lib_num == lib_num), None)
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
        return_date_str = return_date.strftime(%y-%m-%d)

        # ustwaienie flag dla ksiązki
        book.available = False
        book.borrower = user.name
        book.return_date = return_date_str

        user.borrowed.append(book)

        print(f"\nKsiążka '{book.title}' została wypożyczona przez {user.name}. Termin zwrotu: {return_date_str}.")

#    def return_book(self, user_id, lib_num, return_date):

#    def get_all_books(self):

#    def get_available_books(self):

#    def get_user_book(self, user_id):

#    def find_book(self, title):

#    def find_user(self, user_id=None):



book_1001 = Book("Pan Tadeusz", "Adam Mickiewicz", "1001")

print(book_1001)

user_1001 = User("1001", "Jan Kowalski")

print(user_1001)



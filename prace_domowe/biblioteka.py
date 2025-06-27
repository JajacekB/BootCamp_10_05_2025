# stworzyc system zarzadzania biblioteką klasa Book
# dodnie ksiazki, wypozyczenie ksiazki, zwracanie ksiązki
# obsłużyc błedy
# Dodac Library i usera



class Book:
    def __init__(self, title, author, lib_num, available=True, borrower=None):
        """
        Inicjacja obiektu Book
        :param title: Tytuł książki
        :param author: Autor książki
        :param lib_num: Numer katalogowy
        :param available: Czy książka jest dostępna (domyslnie True)
        :param borrower: Kto wypożyczył książkę (domyslnie None)
        :return:
        """

        self.title = title
        self.author = author
        self.lib_num = lib_num
        self.available = available
        self.borrower = borrower

    def __str__(self):
        status = "Dostępna" if self.available else f"Wypożyczona przez: {self.borrower}"
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
    def __init__(self, books, users):
        """
        Inicjacja Biblioteki
        :param books: ksiązki ma stanie biblioteki (dostępne i wypozyczone)
        :param users: uzytkownicy biblioteki
        """

        self.books = books
        self.users = users


    def add_book(self, book):

    def add_user(self, user):

    def borrow_book(self, user_id, lib_num, return_date):

    def return_book(self, user_id, lib_num, return_date):

    def get_all_books(self):

    def get_available_books(self):

    def get_user_book(self, user_id):

    def find_book(self, title):

    def find_user(self, user_id):



book_1001 = Book("Pan Tadeusz", "Adam Mickiewicz", "1001")

print(book_1001)

user_1001 = User("1001", "Jan Kowalski")

print(user_1001)
Program w formie okienkowej uruchamiany jest plikiem main_gui.py.
Istnieje możliwość uruchomienia wersji consolowej plikiem main_consol_version.py
Podczas pierwszego uruchamiania może byc potrzebna inicjalizacja bazy danych. Należy uruchmoic jednorazowo plik init_db.py
który znajduje sie w katalogu .database.
Program napisany jest w standardzie MVC/MVP.
W katalogu tests umieszczone sa pliki main.py służace do testowania funkcjonalności poszczególnych okien wykorzystywanych
w interface uzytkownika GUI. W przyszłości znajda się tam testy atomatyczne do testowania poszczegónych funkcjonalności.


Program posiada takie poziomy użytkownika User:
    1. Admin konto stworzone tylko w poprzez plik init.py w zamierzeniu bez możliwości usunięcia.
        login: admin
        hało admin
        Konto Admin słuzy do dodawania pracowników (Sprzedawaca, Księgowy), testowania wszystkich opcji programu.

    2. Sprzedawca tworzony tylko przez admina z domyślnym loginem i hasłem. Może zmieniać tylko swoje dane osobowe i hasło.
        Sprzedawca testowy:
        login: Seller03
        hasło: Seller03
        Konto Sprzedawca używane do obsługi klientów i floty pojazdów.

    3. Księgoy worzony tylko przez admina z domyślnym loginem i hasłem. Może zmieniać tylko swoje dane osobowe i hasło.
        login: Accountent01
        hasło: Accountent01
        Konto obecnie z pustym menu, w przyszłości będzie służyło do obsługi cześci księgowej (data science)

    4. klient powstaje przez rejestrację zwykłago usera albo może być stworzony przez admina lub sprzedawcę.
        Kient testowy:
        login: tester
        hasło: Tester01
        Konto symulujące klienta i sprawdzające funkcjonalność menu Client

Poza istniejącymi Użytkownikami istnieją profile uzytkowników z rolą "workshop" czyli warszatat naprawczy.
Używane są do zapisywania kosztów napraw pojazdów do przyszłego modułu księgowego.


Każdy poziom usera ma inne menu.

Wersje rozwojwoe:

- rental_v1_2 - wersja konsolowa w pełni funkcjonalna dla 3 typów userów: Admin, Sprzedawca, Klient
- rental_v2_2 - wersja okienkowa w pełni funkcjonalna dla 3 typów userów: Admin, Sprzedawca, Klient

wersje rozwojowe w planach:

- rental_v2_3 - dołożony model księgowy (data science)
- rental_v3_1 - wersja web'owa


import os  # Moduł do interakcji z systemem operacyjnym, np. do zarządzania ścieżkami plików.
from PySide6.QtWidgets import (  # Importuje podstawowe widżety (elementy interfejsu użytkownika) z PySide6.
    QWidget,  # Podstawowa klasa dla wszystkich obiektów interfejsu użytkownika.
    QLabel,  # Widżet do wyświetlania tekstu lub obrazków.
    QPushButton,  # Widżet przycisku.
    QVBoxLayout,  # Układarka pionowa, organizuje widżety jeden pod drugim.
    QSpacerItem,  # Element do tworzenia elastycznej przestrzeni w układach.
    QSizePolicy  # Definiuje, jak widżet powinien się rozszerzać lub kurczyć w układzie.
)
from PySide6.QtGui import (  # Importuje klasy związane z grafiką i wyglądem z PySide6.
    QFont,  # Klasa do definiowania czcionek (rodzaj, rozmiar, pogrubienie).
    QPixmap,  # Klasa do pracy z obrazkami rastrowymi (np. PNG, JPG).
    QPalette,  # Klasa do zarządzania kolorami interfejsu użytkownika.
    QColor  # Klasa do definiowania kolorów.
)
from PySide6.QtCore import Qt  # Importuje podstawowe typy danych Qt i stałe (np. wyrównanie).


class StartWindow(QWidget):  # Definicja klasy głównego okna, dziedziczącej po QWidget.
    def __init__(self):  # Metoda inicjalizacyjna, wywoływana przy tworzeniu instancji klasy.
        super().__init__()  # Wywołuje konstruktor klasy nadrzędnej (QWidget).
        self.setWindowTitle("MOTO VIBE 3000 – Wypożyczalnia Pojazdów")  # Ustawia tytuł okna.

        # Tło: 18% szarości
        palette = QPalette()  # Tworzy nową paletę kolorów.
        palette.setColor(QPalette.Window,
                         QColor("#2e2e2e"))  # Ustawia kolor tła okna na ciemnoszary (kod hexadecymalny).
        self.setPalette(palette)  # Stosuje paletę kolorów do okna.
        self.setAutoFillBackground(True)  # Włącza automatyczne wypełnianie tła kolorem z palety.

        self.setup_ui()  # Wywołuje metodę odpowiedzialną za budowanie interfejsu użytkownika.

    def setup_ui(self):  # Metoda do konfiguracji wszystkich elementów interfejsu użytkownika.
        layout = QVBoxLayout()  # Tworzy nową układarkę pionową.
        layout.setContentsMargins(100, 50, 100,
                                  50)  # Ustawia marginesy wokół zawartości układu (lewy, górny, prawy, dolny).

        # Ścieżka do logo
        # Poniższe linie obliczają ścieżkę do pliku 'logo.png' w folderze 'assets'.
        # Jest to najtrudniejszy element do poprawnego zrozumienia ze względu na ścieżki względne.
        base_dir = os.path.dirname(os.path.abspath(
            __file__))  # Pobiera absolutną ścieżkę do katalogu, w którym znajduje się bieżący skrypt (np. C:/.../gui/windows).
        parent_dir_1 = os.path.dirname(base_dir)  # Idzie poziom wyżej (np. C:/.../gui).
        project_root_dir = os.path.dirname(
            parent_dir_1)  # Idzie kolejny poziom wyżej, do katalogu głównego projektu (C:/YourProject/).
        logo_path = os.path.join(project_root_dir, "assets",
                                 "logo.png")  # Łączy ścieżkę do katalogu głównego z "assets" i "logo.png", tworząc pełną ścieżkę do obrazka.

        print(f"Attempting to load logo from: {logo_path}")  # Wyświetla próbę załadowania ścieżki do debugowania.

        logo_label = QLabel(self)  # Tworzy widżet etykiety dla logo.

        if not os.path.exists(logo_path):  # Sprawdza, czy plik obrazka istnieje pod wyliczoną ścieżką.
            print(f"❌ File not found at: {logo_path}")  # Jeśli plik nie istnieje, wyświetla błąd.
            logo_label.setText("Logo missing")  # Ustawia tekst zastępczy, jeśli logo nie znaleziono.
            logo_label.setStyleSheet("color: red; font-size: 20px;")  # Stylizuje tekst zastępczy na czerwono.
        else:
            print(f"✅ File found at: {logo_path}")  # Jeśli plik istnieje, wyświetla potwierdzenie.

        pixmap = QPixmap(logo_path)  # Tworzy obiekt QPixmap z obrazka podaną ścieżką.
        if pixmap.isNull():  # Sprawdza, czy załadowanie obrazka się powiodło.
            print(
                "❌ Nie udało się załadować obrazka! (QPixmap.isNull() returned True)")  # Wyświetla błąd, jeśli QPixmap jest pusty.
            logo_label.setText(
                "Logo missing (Failed to load)")  # Ustawia inny tekst zastępczy w przypadku problemów z załadowaniem.
            logo_label.setStyleSheet("color: red; font-size: 20px;")
        else:
            print("✅ Logo załadowane poprawnie.")  # Potwierdza pomyślne załadowanie.
            pixmap = pixmap.scaledToHeight(400,
                                           Qt.SmoothTransformation)  # Skaluje obrazek do wysokości 400 pikseli, zachowując proporcje i wygładzanie.
            logo_label.setPixmap(pixmap)  # Ustawia przeskalowany obrazek w etykiecie.

        logo_label.setAlignment(Qt.AlignCenter)  # Wyrównuje obrazek w etykiecie do środka.

        # Tytuł
        title = QLabel("🚗  MOTO VIBE 3000  🚗\nWYPOŻYCZALNIA POJAZDÓW")  # Tworzy etykietę z tytułem.
        title.setFont(QFont("Arial", 32, QFont.Bold))  # Ustawia czcionkę (Arial, rozmiar 32, pogrubiona).
        title.setAlignment(Qt.AlignCenter)  # Wyrównuje tekst tytułu do środka.
        title.setStyleSheet("color: white;")  # Ustawia kolor tekstu tytułu na biały.

        # Przyciski
        btn_login = QPushButton("Zaloguj się")  # Tworzy przycisk "Zaloguj się".
        btn_register = QPushButton("Zarejestruj się")  # Tworzy przycisk "Zarejestruj się".
        btn_exit = QPushButton("Zamknij program")  # Tworzy przycisk "Zamknij program".

        for btn in [btn_login, btn_register, btn_exit]:  # Pętla iteruje po wszystkich przyciskach.
            btn.setFont(QFont("Arial", 18))  # Ustawia czcionkę dla każdego przycisku.
            btn.setFixedHeight(50)  # Ustawia stałą wysokość 50 pikseli dla każdego przycisku.
            btn.setStyleSheet(  # Stosuje styl CSS do każdego przycisku.
                "background-color: #444;"  # Ciemnoszare tło.
                "color: white;"  # Biały kolor tekstu.
                "border-radius: 8px;"  # Zaokrąglone rogi o promieniu 8 pikseli.
            )

        # Układ
        layout.addWidget(logo_label)  # Dodaje etykietę z logo do układu pionowego.
        layout.addWidget(title)  # Dodaje tytuł do układu.
        # layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)) # Oryginalny spacer, który spychał przyciski w dół.
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum,
                                         QSizePolicy.Fixed))  # Zmieniony spacer: tworzy stały odstęp 50 pikseli wysokości, podnosząc przyciski.
        layout.addWidget(btn_login)  # Dodaje przycisk logowania.
        layout.addWidget(btn_register)  # Dodaje przycisk rejestracji.
        layout.addWidget(btn_exit)  # Dodaje przycisk wyjścia.
        layout.setAlignment(Qt.AlignTop)  # Wyrównuje całą zawartość układu do góry okna.
        self.setLayout(layout)  # Ustawia zdefiniowany układ dla okna.
        self.showMaximized()  # Wyświetla okno w trybie zmaksymalizowanym (na cały ekran).


if __name__ == '__main__':  # Standardowa konstrukcja Pythona: kod w tym bloku uruchamia się tylko, gdy skrypt jest wykonywany bezpośrednio.
    import sys  # Moduł systemowy, używany tutaj do obsługi argumentów wiersza poleceń i wyjścia z aplikacji.
    from PySide6.QtWidgets import QApplication  # Importuje główną klasę aplikacji PySide6.

    app = QApplication(sys.argv)  # Tworzy instancję aplikacji PySide6. Jest to niezbędne dla każdej aplikacji PySide6.
    window = StartWindow()  # Tworzy instancję Twojego okna StartWindow.
    window.show()  # Wyświetla okno.
    sys.exit(app.exec())  # Uruchamia główną pętlę zdarzeń aplikacji i czeka na jej zakończenie, zwracając kod wyjścia.
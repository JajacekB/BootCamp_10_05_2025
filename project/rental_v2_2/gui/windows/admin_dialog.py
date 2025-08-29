from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QSpacerItem,
    QPushButton, QGridLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer


class AdminDialog(QMainWindow):
    command_selected = Signal(str)
    logout = Signal(object)

    def __init__(self, user, session, controller):
        super().__init__()
        print("✅ Inicjalizacja AdminWindow")
        self.user = user
        self.session = session
        self.controller = controller
        self.dynamic_area = QFrame()
        self.current_widget = None
        self.active_menu_button = None

        self.setWindowTitle("Menu Admina")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: #eee;
                font-size: 18px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            }
        """)

        self._build_ui()
        QTimer.singleShot(0, self.showMaximized)

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(25, 25, 25, 25)
        self.grid_layout.setSpacing(15)

        self.grid_layout.setColumnStretch(0, 0)  # menu nie rozciąga się
        self.grid_layout.setColumnStretch(1, 1)  # dynamic_area zajmuje resztę

        central_widget.setLayout(self.grid_layout)
        self.current_widget = None

        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(15)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setAlignment(Qt.AlignTop)

        hello_label = QLabel("Menu Admina")
        hello_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        hello_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(hello_label)

        info_label = QLabel("Wybierz co chcesz robić:")
        info_label.setStyleSheet("color: #A9C1D9; font-size: 20px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(info_label)

        menu_list = self._get_menu_for_role(self.user.role.lower())

        for item_text in menu_list:
            button = QPushButton(item_text)
            button.setFixedSize(275, 45)
            button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")

            command_num = item_text.split(".")[0]
            button.clicked.connect(
                lambda checked, b=button, num=command_num: self._on_dynamic_button_clicked_with_highlight(b, num))

            menu_layout.addWidget(button, alignment=Qt.AlignCenter)

        menu_layout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        logoff_button = QPushButton("Wyloguj się")
        logoff_button.setFixedSize(255, 50)
        logoff_button.setStyleSheet("background-color: brown; color: white; font-size: 18px; border-radius: 8px; padding: 10px;")
        logoff_button.clicked.connect(self._on_logout_clicked)
        menu_layout.addWidget(logoff_button, alignment=Qt.AlignCenter)

        menu_container = QWidget()
        menu_container.setLayout(menu_layout)
        self.grid_layout.addWidget(menu_container, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.dynamic_area = QWidget()
        self.dynamic_area.setLayout(QVBoxLayout())
        self.dynamic_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.grid_layout.addWidget(self.dynamic_area, 0, 1, 1, 2)  # kolumny 1 i 2

        QTimer.singleShot(0, lambda: self._safe_show_overdue_rentals())

    def _get_menu_for_role(self, role: str) -> list[str]:
        if role == "admin":
            return [
                "1. Dodaj nowego sprzedawcę",
                "2. Usuń sprzedawcę",
                "3. Dodaj nowego klienta",
                "4. Usuń klienta",
                "5. Przeglądaj klientów",
                "6. Dodaj nowy pojazd",
                "7. Usuń pojazd z użytkowania",
                "8. Przeglądaj pojazdy",
                "9. Wypożycz pojazd klientowi",
                "10. Zwróć pojazd",
                "11. Oddaj pojazd do naprawy",
                "12. Aktualizuj profil"
            ]
        elif role == "seller":
            return [
                "1. Dodaj nowego klienta",
                "2. Usuń klienta",
                "3. Przeglądaj pojazdy",
                "4. Dodaj nowy pojazd",
                "5. Usuń pojazd z użytkowania",
                "6. Przeglądaj pojazdy",
                "7. Wypożycz pojazd klientowi",
                "8. Zwróć pojazd",
                "9. Oddaj pojazd do naprawy",
                "10. Aktualizuj profil"
            ]
        elif role == "client":
            return [
                "1. Przeglądaj pojazdy",
                "2. Wypożycz pojazd",
                "3. Zwróć pojazd",
                "4. Aktualizuj profil"
            ]
        else:
            return []

    def clear_dynamic_area(self):
        layout = self.dynamic_area.layout()
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self.current_widget = None

    def _on_dynamic_button_clicked_with_highlight(self, button, command_num):

        if self.active_menu_button:
            self.active_menu_button.setStyleSheet(
                "color: white; border-radius: 8px; padding-left: 10px; background-color: #555;"
            )

        self.active_menu_button = button
        self.active_menu_button.setStyleSheet(
            "color: black; border-radius: 8px; padding-left: 10px; background-color: beige;"
        )

        self._on_dynamic_button_clicked(command_num, button)

    def _on_dynamic_button_clicked(self, command_num: str, button):
        print(f"Emituję command_selected: {command_num}")
        self.command_selected.emit(command_num)
        self._set_active_menu_button(button)

    def _on_logout_clicked(self):
        print("Emituję sygnał logout")
        self.logout.emit(self.user)

    def load_widget(self, widget):
        self.clear_dynamic_area()
        self.dynamic_area.layout().addWidget(widget)
        self.current_widget = widget

    def _safe_show_overdue_rentals(self):
        try:
            self.controller.show_overdue_rentals_widget()
        except Exception as e:
            print(f"❌ Błąd podczas sprawdzania zaległości: {e}")

    def _set_active_menu_button(self, button):

        if self.active_menu_button:
            self.active_menu_button.setStyleSheet(
                "color: white; border-radius: 8px; padding-left: 10px; background-color: #555;"
            )

        self.active_menu_button = button
        self.active_menu_button.setStyleSheet(
            "color: black; border-radius: 8px; padding-left: 10px; background-color: beige;"
        )


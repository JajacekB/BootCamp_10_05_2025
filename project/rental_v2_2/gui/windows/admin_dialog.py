from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout,
    QPushButton, QGridLayout, QFrame
)
from PySide6.QtCore import Qt, Signal
from gui.windows.register_wiget import RegisterWidget


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
        self.showMaximized()

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

        menu_list = [
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

        for item_text in menu_list:
            button = QPushButton(item_text)
            button.setFixedSize(300, 45)
            button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")
            menu_layout.addWidget(button, alignment=Qt.AlignCenter)
            command_num = item_text.split(".")[0]
            button.clicked.connect(lambda checked, num=command_num: self._on_dynamic_button_clicked(num))

        info_label = QLabel("Wybierz co chcesz robić:")
        info_label.setStyleSheet("color: purple; font-size: 20px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(info_label)

        logoff_button = QPushButton("Wyloguj się")
        logoff_button.setFixedSize(255, 50)
        logoff_button.setStyleSheet("color: white; font-size: 18px; border-radius: 8px; padding: 10px;")
        logoff_button.clicked.connect(self._on_logout_clicked)
        menu_layout.addWidget(logoff_button, alignment=Qt.AlignCenter)

        menu_container = QWidget()
        menu_container.setLayout(menu_layout)
        self.grid_layout.addWidget(menu_container, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.dynamic_area = QWidget()
        self.dynamic_area.setLayout(QVBoxLayout())
        self.grid_layout.addWidget(self.dynamic_area, 0, 1, 1, 2)  # kolumny 1 i 2

    def show_register_widget(self, role: str = None, auto: bool = False):
        self.register_widget = RegisterWidget(
            session=self.session,
            parent=self,
            role=role,
            auto=auto
        )

        self.register_widget.registration_finished.connect(
            self.controller.on_registration_finished_widget
        )
        self.register_widget.registration_cancelled.connect(
            self.controller.on_registration_cancelled_widget
        )
        self.controller.clear_requested.connect(self.clear_dynamic_area)

        self.load_widget(self.register_widget)


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


    def _on_dynamic_button_clicked(self, command_num: str):
        print(f"Emituję command_selected: {command_num}")
        self.command_selected.emit(command_num)

    def _on_logout_clicked(self):
        print("Emituję sygnał logout")
        self.logout.emit(self.user)

    def load_widget(self, widget):
        self.clear_dynamic_area()
        self.dynamic_area.layout().addWidget(widget)
        self.current_widget = widget
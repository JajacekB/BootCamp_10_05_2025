# get_users_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox, QListWidget, QListWidgetItem, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt
from datetime import date

class GetUsersWidget(QWidget):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Klienci")
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; color: #eee; font-size: 16px; }
            QPushButton { background-color: #555; border-radius: 5px; padding: 5px; }
            QLineEdit { font-size: 14px; }
        """)

        main_layout = QVBoxLayout()

        title_label = QLabel("Przegląd klientów wypożyczalni:")
        title_label.setStyleSheet("font-size: 28px; color: white; ")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(["Wszyscy", "Z wypożyczeniem", "Bez wypożyczenia", "Nieaktywni"])

        form_layout = QFormLayout()
        form_layout.addRow("Jakich klientów chcesz przeglądać?", self.status_combo_box)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green; font-size: 20px; color: white; border-radius: 8px; padding: 5px;"
        )
        self.search_button.setFixedSize(150, 35)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        form_layout.addRow("", button_layout)

        filters_layout = QVBoxLayout()
        filters_layout.addLayout(form_layout)

        self.filters_group = QGroupBox("Filtr wyszukiwania")
        self.filters_group.setLayout(filters_layout)
        main_layout.addWidget(self.filters_group)

        self.list_widget = QListWidget()
        self.list_widget.setWordWrap(True)
        main_layout.addWidget(self.list_widget)
        self.adjust_list_height()

        main_layout.addStretch()
        self.setLayout(main_layout)

    def add_user_to_list(self, uid, user_str):
        item = QListWidgetItem(user_str)
        item.setData(Qt.UserRole, uid)
        self.list_widget.addItem(item)
        self.adjust_list_height()

    def show_user_details(self, details: dict):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()

        # Użytkownik
        user_item = QListWidgetItem(f"Użytkownik: {details['user']}" if details["user"] else "Użytkownik: brak danych")
        user_item.setFlags(Qt.NoItemFlags)
        user_item.setData(Qt.UserRole, None)
        self.list_widget.addItem(user_item)

        # Pojazd / wypożyczenie
        rent = details["rent"]
        if not rent:
            vehicle_item = QListWidgetItem("Nigdy nie wypożyczał żadnego pojazdu")
        else:
            start_str = rent.start_date.strftime("%d.%m.%Y") if rent.start_date else "brak daty startu"
            planned_str = rent.planned_return_date.strftime("%d.%m.%Y") if rent.planned_return_date else "brak daty zwrotu"
            vehicle_text = [
                f"Pojazd: {details['vehicle']}" if details["vehicle"] else "Pojazd: brak danych",
                f"Wynajęty od {start_str} do {planned_str}"
            ]
            vehicle_item = QListWidgetItem("\n".join(vehicle_text))

        vehicle_item.setFlags(Qt.NoItemFlags)
        vehicle_item.setData(Qt.UserRole, None)
        self.list_widget.addItem(vehicle_item)
        self.adjust_list_height()
        self.list_widget.blockSignals(False)

    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        visible_rows = min(10, max(5, count))
        new_height = visible_rows * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)
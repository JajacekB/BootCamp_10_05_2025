# get_users_view.py
import platform
from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QMessageBox,
        QComboBox, QListWidget, QListWidgetItem, QGroupBox, QHBoxLayout
    )
from PySide6.QtCore import Qt, Signal


class GetUsersWidget(QWidget):

    handle_search_clicked = Signal()
    handle_item_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Klienci")
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; color: #eee; font-size: 16px; }
            QPushButton { background-color: #555; border-radius: 5px; padding: 5px; }
            QLineEdit { font-size: 14px; }
        """)

        main_layout = QVBoxLayout()

        title_label = QLabel("=== Przegląd klientów wypożyczalni ===\n")
        title_label.setStyleSheet("font-size: 28px; color: #A9C1D9; ")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(["Wszyscy", "Z wypożyczeniem", "Bez wypożyczenia", "Nieaktywni"])

        form_layout = QFormLayout()
        form_layout.addRow("Jakich klientów chcesz przeglądać?", self.status_combo_box)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green; font-size: 18px; color: white; border-radius: 10px; padding: 5px;"
        )
        self.search_button.clicked.connect(self._on_clicked_search_button)
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

        font = self.list_widget.font()
        system = platform.system()
        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":
            font.setFamily("Menlo")
        else:
            font.setFamily("DejaVu Sans Mono")
        self.list_widget.setFont(font)
        self.list_widget.addItem("")
        self.adjust_list_height()

        self.list_widget.itemClicked.connect(self._on_list_item_clicked)
        main_layout.addWidget(self.list_widget)
        self.adjust_list_height()

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _on_clicked_search_button(self):
        self.handle_search_clicked.emit()

    def show_users_list(self, formatted_users, success: bool, message: str):
        self.list_widget.clear()

        if not success:
            QMessageBox.information(self, "Informacja", message)
            return

        for uid, user_str in formatted_users:
            self._add_user_to_list(uid, user_str)

    def _add_user_to_list(self, uid, user_str):
        item = QListWidgetItem(user_str)
        item.setData(Qt.UserRole, uid)
        self.list_widget.addItem(item)
        self.adjust_list_height()

    def _on_list_item_clicked(self, item):
        uid = item.data(Qt.UserRole)
        if uid is not None:
            self.handle_item_clicked.emit(uid)

    def show_user_details(self, details: dict):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()

        user = details["user"]
        user_item = f"Uzytkownik: {user}"
        header = QListWidgetItem(user_item)
        header.setFlags(Qt.NoItemFlags)
        self.list_widget.addItem(header)

        rentals = details["rent"]

        for rental in rentals:
            if rental is None:
                separator_item = QListWidgetItem("")
                separator_item.setFlags(Qt.NoItemFlags)
                self.list_widget.addItem(separator_item)
                continue

            return_date = rental.actual_return_date or rental.planned_return_date
            text = (
                f"|{rental.reservation_id:<7} "
                f"|{rental.vehicle.brand:<11} "
                f"|{rental.vehicle.vehicle_model:<13} "
                f"|{rental.vehicle.type:<9} "
                f"|{rental.start_date.strftime('%d-%m-%Y'):>11} → "
                f"{return_date.strftime('%d-%m-%Y'):<11}"
                f"|{rental.total_cost:>7} zł |"
            )

            item = QListWidgetItem(text)
            item.setFlags(Qt.NoItemFlags)
            if rental.actual_return_date is not None:
                item.setForeground(Qt.gray)

            self.list_widget.addItem(item)

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
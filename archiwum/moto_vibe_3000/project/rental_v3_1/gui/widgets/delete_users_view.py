# delete_users_view.py
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QHBoxLayout, QApplication
)
from PySide6.QtCore import Qt, Signal


class DeleteUsersWidget(QWidget):

    request_users = Signal()
    user_selected = Signal(int)
    delete_requested = Signal(int)
    cancel_requested = Signal()

    def __init__(self, role="client"):
        super().__init__()
        self.role = role
        self.user = None
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Klienci")

        self.setStyleSheet("""
                    QWidget { background-color: #2e2e2e; color: #eee; font-size: 16px; }
                    QPushButton { font-size: 18; background-color: #555; border-radius: 10px; padding: 5px; }
                    QLineEdit { font-size: 14px; }
                """)

        main_layout = QVBoxLayout()

        if self.role == "seller":
            title_label = QLabel("=== Przegląd pracowników wypożyczalni ===")
        else:
            title_label = QLabel("=== Przegląd klientów wypożyczalni niemających wypożyczeń ===")

        title_label.setStyleSheet("font-size: 24px; color: #A9C1D9;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        main_layout.addWidget(self.list_widget)
        self.adjust_list_height()

        self.search_button = QPushButton("Pokaż")
        self.search_button.setFixedSize(155, 35)
        self.search_button.setStyleSheet(
            "background-color: darkgreen;"
            "font-size: 18px; color: white;"
            "border-radius: 10px; padding: 5px;"
        )
        self.search_button.clicked.connect(lambda: self.request_users.emit())
        main_layout.addWidget(self.search_button, alignment=Qt.AlignLeft)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("color: white; font-size: 16px;")
        self.summary_label.setVisible(False)
        main_layout.addWidget(self.summary_label, alignment=Qt.AlignLeft)

        btn_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setFixedSize(155, 35)
        self.cancel_button.setStyleSheet(
            "background-color: brown; font-size: 18px; color: white; border-radius: 10px; padding: 5px;"
        )
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(lambda: self.cancel_requested.emit())
        btn_layout.addWidget(self.cancel_button)

        self.delete_user_button = QPushButton("Usuń użytkownika")
        self.delete_user_button.setFixedSize(155, 35)
        self.delete_user_button.setStyleSheet(
            "background-color: darkgreen; font-size: 18px; color: white; border-radius: 10px; padding: 5px;"
        )
        self.delete_user_button.setVisible(False)
        self.delete_user_button.clicked.connect(self._on_delete_clicked)
        btn_layout.addWidget(self.delete_user_button)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def populate_users(self, users: list):
        # usersi przekazani z zewnątrz
        self.list_widget.clear()
        if not users:
            QMessageBox.information(self, "Informacja", "Brak klientów bez aktywnego wypożyczenia.")
            return

        for u in users:
            item = QListWidgetItem(f"ID: [{u['id']:03d}] - {u['first_name']} {u['last_name']}, login: {u['login']}")
            item.setData(Qt.UserRole, u["id"])
            self.list_widget.addItem(item)
            self.adjust_list_height()

    def show_user_summary(self, user_info: str):
        self.summary_label.setText(user_info)
        self.summary_label.show()
        self.delete_user_button.show()
        self.cancel_button.show()
        self.search_button.hide()

    def reset_summary(self):
        self.summary_label.hide()
        self.delete_user_button.hide()
        self.cancel_button.hide()
        self.search_button.show()
        self.list_widget.clearSelection()

    def _on_item_clicked(self, item):
        uid = item.data(Qt.UserRole)
        self.user_selected.emit(uid)

    def _on_delete_clicked(self):
        if self.list_widget.currentItem():
            uid = self.list_widget.currentItem().data(Qt.UserRole)
            self.delete_requested.emit(uid)

    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)


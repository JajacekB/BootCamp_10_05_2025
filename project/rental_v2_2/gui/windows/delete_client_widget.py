import sys

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
    )
from PySide6.QtCore import Qt, QTimer, Signal

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
from database.base import SessionLocal


class DeleteUsersWidget(QWidget):

    def __init__(self, session=None, role="client"):
        super().__init__()
        self.session =  session or SessionLocal()
        self.role = role

        self.setWindowTitle("Klienci")

        self.setStyleSheet("""
                    QWidget {
                        background-color: #2e2e2e; /* Ciemne tło dla całego widgetu */
                        color: #eee; /* Jasny kolor tekstu */
                        font-size: 16px;
                    }
                    QPushButton {
                        background-color: #555;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QLineEdit {
                        font-size: 14px;
                    }
                """)
        self._build_ui()


    def _build_ui(self):

        main_layout = QVBoxLayout()
        if self.role == "seller":
            title_label1 = QLabel("Przegląd pracowników wypożyczalni:")
        else:
            title_label1 = QLabel("Przegląd klientów wypozyczalni niemających wypożyczeń:")

        title_label1.setStyleSheet("font-size: 28px; color: white; ")
        title_label1.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label1)

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)
        self.adjust_list_height()
        self.list_widget.itemClicked.connect(self._confirm_end_delete_client)


        self.search_button = QPushButton("Pokaż")
        self.search_button.setFixedSize(155, 45)
        self.search_button.setStyleSheet(
            "background-color: green;"
            "font-size: 24px; color: white;"
            "border-radius: 8px; padding: 5px;"
        )
        self.search_button.clicked.connect(self._choice_client_to_delete)
        main_layout.addWidget(self.search_button, alignment=Qt.AlignLeft)


        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("color: white; font-size: 14px;")
        self.summary_label.setVisible(False)
        main_layout.addWidget(self.summary_label, alignment=Qt.AlignLeft)


        cancel_delete_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setFixedSize(155, 40)
        self.cancel_button.setStyleSheet(
            "background-color: #F44336; font-size: 18px; color: white; border-radius: 8px; padding: 5px;"
        )
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self._hide_summary)
        cancel_delete_layout.addWidget(self.cancel_button, alignment=Qt.AlignLeft)


        self.delete_user_button = QPushButton("Usuń użytkownika")
        self.delete_user_button.setFixedSize(155, 40)
        self.delete_user_button.setStyleSheet(
            "background-color: #4CAF50; font-size: 18px; color: white; border-radius: 8px; padding: 5px;"
        )
        self.delete_user_button.setVisible(False)
        self.delete_user_button.clicked.connect(self._delete_client)
        cancel_delete_layout.addWidget(self.delete_user_button, alignment=Qt.AlignLeft)

        cancel_delete_layout.addStretch()

        main_layout.addLayout(cancel_delete_layout)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _choice_client_to_delete(self):
        self.list_widget.clear()

        try:

            active_renters_ids = {
                v.borrower_id
                for v in self.session.query(Vehicle.borrower_id)
                .filter(Vehicle.is_available == False, Vehicle.borrower_id != None)
                .distinct()
            }

            candidates_to_delete = self.session.query(User).filter(
                User.id.notin_(active_renters_ids),
                User.role == self.role,
                User.is_active == True
            ).all()

            if not candidates_to_delete:
                QMessageBox.information(self, "Informacja", "Brak klientów bez aktywnego wypożyczenia.")
                return

            for u in candidates_to_delete:
                user_strs = f"ID: [{u.id:03d}]  -  {u.first_name} {u.last_name},  login: {u.login}."
                item = QListWidgetItem(user_strs)
                item.setData(Qt.UserRole, u.id)
                self.list_widget.addItem(item)
                self.adjust_list_height()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")


    def _confirm_end_delete_client(self, item):
        uid = item.data(Qt.UserRole)
        try:
            self.user = self.session.query(User).filter(User.id == uid).first()
            if self.user.role == "seller":
                self.user_str = (
                    f"Czy chcesz usunąć?\n\n"
                    f"Pracownik wypozyczalni: {self.user.first_name} {self.user.last_name}\n"                
                    f"email: {self.user.email}\n"
                    f"zamieszkały: {self.user.address}\n"
                    f"login: {self.user.login}\n"
                    f""
                )
            else:
                self.user_str = (
                    f"Czy chcesz usunąć?\n\n"
                    f"Użytkownik: {self.user.first_name} {self.user.last_name}\n"                
                    f"email: {self.user.email}\n"
                    f"zamieszkały: {self.user.address}\n"
                    f"login: {self.user.login}\n"
                    f""
                )

            self.summary_label.setText(self.user_str)

            self.summary_label.show()
            self.delete_user_button.show()
            self.cancel_button.show()
            self.search_button.hide()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")

    def _hide_summary(self):
        self.summary_label.hide()
        self.delete_user_button.hide()
        self.cancel_button.hide()
        # self.search_button.show()
        self.user = None
        self.list_widget.clearSelection()

    def _delete_client(self):
        try:
            if not self.user:
                QMessageBox.warning(self, "Błąd", "Nie wybrano użytkownika.")
                return

            self.user.is_active = False
            self.session.commit()

            QMessageBox.information(self, "Sukces", "Użytkownik został dezaktywowany.")

            self._hide_summary()
            self.list_widget.clear()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas dezaktywacji użytkownika:\n{e}")


    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DeleteUsersWidget()
    main_window.show()
    sys.exit(app.exec())
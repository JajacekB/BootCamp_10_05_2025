import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal
from requests import session
from sqlalchemy import desc
from datetime import date

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

        title_label1 = QLabel("Przegląd klientów wypozyczalni niemających wypożyczeń:")
        title_label1.setStyleSheet("font-size: 28px; color: white; ")
        title_label1.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label1)

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self._confirm_end_delete_client)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setFixedSize(150, 45)
        self.search_button.setStyleSheet(
            "background-color: green;"
            "font-size: 24px; color: white;"
            "border-radius: 8px; padding: 10px;"
        )
        self.search_button.clicked.connect(lambda: self._choice_client_to_delete(self.role))
        main_layout.addWidget(self.search_button, alignment=Qt.AlignRight)


        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("color: white; font-size: 14px;")
        # self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setVisible(False)
        main_layout.addWidget(self.summary_label, alignment=Qt.AlignLeft)


        cancel_delete_layout = QGridLayout()

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setFixedSize(150, 45)
        self.cancel_button.setStyleSheet(
            "background-color: #F44336; color: white; border-radius: 8px; padding: 10px;"
        )
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self._hide_summary)
        cancel_delete_layout.addWidget(self.cancel_button, 0, 0, 1, 1, alignment=Qt.AlignLeft)


        self.delete_user_button = QPushButton("Usuń użytkownika")
        self.delete_user_button.setFixedSize(150, 45)
        self.delete_user_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px;"
        )
        self.delete_user_button.setVisible(False)
        self.delete_user_button.clicked.connect(self._delete_client)
        cancel_delete_layout.addWidget(self.delete_user_button, 0, 1, 1, 1, alignment=Qt.AlignRight)

        main_layout.addLayout(cancel_delete_layout)

        main_layout.addStretch()
        self.setLayout(main_layout)


    def _choice_client_to_delete(self, user_role = "client"):
        self.list_widget.clear()

        try:
            vehicle_with_rent = self.session.query(Vehicle).filter(
                Vehicle.is_available == False
            ).all()

            if not vehicle_with_rent:
                QMessageBox.information(self, "Informacja", "Brak klientów bez wypożyczenia.")
                return

            user_ids = [u.borrower_id for u in vehicle_with_rent]

            candidates_to_delete = self.session.query(User).filter(
                User.id.notin_(user_ids),
                User.role == user_role
            ).all()

            candidates_view = defaultdict(list)
            for u in (candidates_to_delete):
                key = (u.id, u.first_name, u.last_name, u.login)
                candidates_view[key].append(u)

            for (uid, first_name, last_name, login) in candidates_view:
                user_strs = f"ID: [{uid:03d}]  -  {first_name} {last_name},  login: {login}."
                item = QListWidgetItem(user_strs)
                item.setData(Qt.UserRole, uid)
                self.list_widget.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")


    def _confirm_end_delete_client(self, item):
        uid = item.data(Qt.UserRole)
        try:
            self.user = self.session.query(User).filter(User.id == uid).first()
            self.user_str = (
                f"Czy chcesz usunąć?\n\n"
                f"Użytkownik: {self.user.first_name} {self.user.last_name}\n"                
                f"email: {self.user.email}\n"
                f"zamieszkały: {self.user.address}\n"
                f"login: {self.user.login}\n"
                f""
            )
            self.summary_label.setText(self.user_str)

            self.summary_label.setVisible(True)
            self.delete_user_button.setVisible(True)
            self.cancel_button.setVisible(True)
            self.search_button.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")

    def _hide_summary(self):
        self.summary_label.setVisible(False)
        self.delete_user_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.search_button.setEnabled(True)

    def _delete_client(self, item):
        uid = item.data(Qt.UserRole)
        try:
            user = self.session.query(User).filter(User.id == uid).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                QMessageBox.information(self, "Sukces", "Użytkownik został usunięty.")
            else:
                QMessageBox.warning(self, "Błąd", "Nie znaleziono użytkownika.")

            self._hide_summary()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas usuwania użytkownika:\n{e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DeleteUsersWidget()
    main_window.show()
    sys.exit(app.exec())
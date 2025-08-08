import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal

from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
# from models.rental_history import RentalHistory
# from models.repair_history import RepairHistory
# from models.invoice import Invoice
from database.base import SessionLocal


class GetUsers(QWidget):

    def __init__(self, session=None):
        super().__init__()
        self.session =  session

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

        users_type_list = ["Wszyscy", "Z wypożyczeniem", "Bez wypożyczenia"]

        main_layout = QVBoxLayout()

        title_label = QLabel("Przegląd klientów wypozyczalni:")
        title_label.setStyleSheet("font-size: 28; color: white; ")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.setLayout(main_layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetUsers()
    main_window.show()
    sys.exit(app.exec())
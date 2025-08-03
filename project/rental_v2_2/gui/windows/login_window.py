import os
import sys
import bcrypt
from PySide6.QtWidgets import (
    QApplication, QWidget, QSpacerItem, QLabel, QLayout, QFormLayout,
    QPushButton, QLineEdit, QComboBox, QGridLayout, QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


from services.user_service import User
from database.base import SessionLocal


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logowanie")
        self.setGeometry(650, 150, 350, 450)
        self.setStyleSheet("""
                    QWidget {
                        background-color: #333; /* Ciemne tło dla całego okna */
                        color: #eee; /* Jasny kolor tekstu dla całego okna */
                        font-size: 16px;
                    }
                    QPushButton {
                        background-color: #555; /* Inny kolor tła dla przycisków */
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)
        self.valid_style = "border: 1px solid #4CAF50;"
        self.invalid_style = "border: 1px solid #F44336;"

        main_layout = QGridLayout()





        self.title_label = QLabel("Logowanie do >>MOTO VIBE 3000<<")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: red; font-size: 23px; /* font-weight: bold; */")
        # self.title_label.setMaximumSize(700, 150)
        main_layout.addWidget(self.title_label, 0, 0, 1, 2)


        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = LoginWindow()
    main_window.show()
    sys.exit(app.exec())


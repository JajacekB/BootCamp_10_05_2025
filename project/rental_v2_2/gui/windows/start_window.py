import os
import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QApplication
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor
from PySide6.QtCore import Qt, QTimer, Signal # Import Signal for custom signals


class StartWindow(QWidget):

    login_requested = Signal()
    register_requested = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOTO VIBE 3000 – Wypożyczalnia Pojazdów")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2e2e2e"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.title_label = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 50, 100, 50)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir_1 = os.path.dirname(base_dir)
        project_root_dir = os.path.dirname(parent_dir_1)
        logo_path = os.path.join(project_root_dir, "assets", "logo.png")

        print(f"Attempting to load logo from: {logo_path}")

        logo_label = QLabel(self)

        if not os.path.exists(logo_path):
            print(f"❌ File not found at: {logo_path}")

            logo_label.setText("Logo missing")
            logo_label.setStyleSheet("color: red; font-size: 20px;")
        else:
            print(f"✅ File found at: {logo_path}")
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                print("❌ Nie udało się załadować obrazka! (QPixmap.isNull() returned True)")

                logo_label.setText("Logo missing (Failed to load)")
                logo_label.setStyleSheet("color: red; font-size: 20px;")
            else:
                print("✅ Logo załadowane poprawnie.")
                pixmap = pixmap.scaledToHeight(400, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)

        logo_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("🚗  MOTO VIBE 3000  🚗\nWYPOŻYCZALNIA POJAZDÓW")
        self.title_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white;")

        btn_login = QPushButton("Zaloguj się")
        btn_register = QPushButton("Zarejestruj się")
        self.btn_exit = QPushButton("Zamknij program")

        for btn in [btn_login, btn_register, self.btn_exit]:
            btn.setFont(QFont("Arial", 18))
            btn.setFixedHeight(50)
            btn.setStyleSheet(
                "background-color: #444;"
                "color: white;"
                "border-radius: 8px;"
            )


        btn_login.clicked.connect(self.login_requested.emit)
        btn_register.clicked.connect(lambda: self.register_requested.emit(self))
        # Connect the exit button to the handle_exit_program function
        self.btn_exit.clicked.connect(self.handle_exit_program)

        layout.addWidget(logo_label)
        layout.addSpacerItem(QSpacerItem(20, 75, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(self.title_label)
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)
        layout.addWidget(self.btn_exit)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.showMaximized()

    def handle_exit_program(self):

        print("Do widzenia!")

        for widget in self.findChildren(QPushButton):
            widget.setEnabled(False)

        self.title_label.setText("Do widzenia!")
        self.title_label.setFont(QFont("Arial", 40, QFont.Bold)) # Make it larger for emphasis
        self.title_label.setStyleSheet("color: #FFD700;") # Change color for visibility

        QTimer.singleShot(1000, QApplication.instance().quit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = StartWindow()
    main_window.show()
    sys.exit(app.exec())
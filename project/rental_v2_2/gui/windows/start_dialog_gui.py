import os
import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QApplication
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor
from PySide6.QtCore import Qt


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOTO VIBE 3000 – Wypożyczalnia Pojazdów")

        # Tło: 18% szarości
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2e2e2e"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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
            # Optionally, set a placeholder image or display a text message
            logo_label.setText("Logo missing")
            logo_label.setStyleSheet("color: red; font-size: 20px;")
        else:
            print(f"✅ File found at: {logo_path}")

        pixmap = QPixmap(logo_path)
        if pixmap.isNull():
            print("❌ Nie udało się załadować obrazka! (QPixmap.isNull() returned True)")
            # Optionally, set a placeholder image or display a text message
            logo_label.setText("Logo missing (Failed to load)")
            logo_label.setStyleSheet("color: red; font-size: 20px;")
        else:
            print("✅ Logo załadowane poprawnie.")
            pixmap = pixmap.scaledToHeight(400, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)

        logo_label.setAlignment(Qt.AlignCenter)

        # Tytuł
        title = QLabel("🚗  MOTO VIBE 3000  🚗\nWYPOŻYCZALNIA POJAZDÓW")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")

        # Przyciski
        btn_login = QPushButton("Zaloguj się")
        btn_register = QPushButton("Zarejestruj się")
        btn_exit = QPushButton("Zamknij program")

        for btn in [btn_login, btn_register, btn_exit]:
            btn.setFont(QFont("Arial", 18))
            btn.setFixedHeight(50)
            btn.setStyleSheet(
                "background-color: #444;"
                "color: white;"
                "border-radius: 8px;"
            )

        # Układ
        layout.addWidget(logo_label)
        layout.addSpacerItem(QSpacerItem(20, 75, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(title)
        # layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)
        layout.addWidget(btn_exit)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.showMaximized()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
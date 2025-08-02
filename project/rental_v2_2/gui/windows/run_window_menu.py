import os
import sys
from PySide6.QtCore import  Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QFont
from gui.windows.register_window import RegisterWindow


class RunWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.setWindowTitle(">>> MOTO VIBE 3000 <<<")
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

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer.changeSize(
            spacer.sizeHint().width(),
            25,
            QSizePolicy.Minimum,
            QSizePolicy.Maximum
        )
        main_layout.addSpacerItem(spacer)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir_1 = os.path.dirname(base_dir)
        project_root_dir = os.path.dirname(parent_dir_1)
        logo_path = os.path.join(project_root_dir, "assets", "logo.png")

        logo_label = QLabel()
        logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logo_label.setMaximumSize(700, 500)
        logo_label.setScaledContents(True)
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                logo_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("Nie udało się wczytać logo.")
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer.changeSize(
            spacer.sizeHint().width(),
            75,
            QSizePolicy.Minimum,
            QSizePolicy.Maximum
        )
        main_layout.addSpacerItem(spacer)

        self.title_label = QLabel("🚗  MOTO VIBE 3000  🚗\nWYPOŻYCZALNIA POJAZDÓW")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: red; font-size: 42px; /* font-weight: bold; */")
        # self.title_label.setMaximumSize(700, 150)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignHCenter)

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer.changeSize(
            spacer.sizeHint().width(),
            75,
            QSizePolicy.Minimum,
            QSizePolicy.Maximum
        )
        main_layout.addSpacerItem(spacer)

        self.login_window = None
        self.login_button = QPushButton("Logowanie")
        self.login_button.setFixedSize(250, 55)
        self.login_button.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold; border-radius: 8px; padding: 10px;"
        )
        # self.login_window.clicked.connect(self.show_login_window)
        main_layout.addWidget(self.login_button, alignment=Qt.AlignHCenter)


        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer.changeSize(
            spacer.sizeHint().width(),
            25,
            QSizePolicy.Minimum,
            QSizePolicy.Maximum
        )
        main_layout.addSpacerItem(spacer)

        self.register_window = None
        self.register_button = QPushButton("Rejstracja")
        self.register_button.setFixedSize(250, 55)
        self.register_button.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold; border-radius: 8px; padding: 10px;"
        )
        self.register_button.clicked.connect(self.show_register_window)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignHCenter)

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer.changeSize(
            spacer.sizeHint().width(),
            25,
            QSizePolicy.Minimum,
            QSizePolicy.Maximum
        )
        main_layout.addSpacerItem(spacer)

        self.exit_program_button = QPushButton("Zakończ program")
        self.exit_program_button.setFixedSize(250, 55)
        self.exit_program_button.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold; border-radius: 8px; padding: 10px;"
        )
        self.exit_program_button.clicked.connect(self._exit_and_close)
        main_layout.addWidget(self.exit_program_button, alignment=Qt.AlignHCenter)

        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)
        self.showMaximized()







    def show_register_window(self):
        # Sprawdź, czy okno już istnieje, żeby uniknąć otwierania wielu okien
        if self.register_window is None:
            self.register_window = RegisterWindow()

        self.register_window.show()


    def _exit_and_close(self):
        QTimer.singleShot(500, self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RunWindow()
    main_window.show()
    sys.exit(app.exec())
import os
import sys
from PySide6.QtCore import  Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from gui.windows.register_window import RegisterWindow


class RunWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.setWindowTitle(">>> MOTO VIBE 3000 <<<")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir_1 = os.path.dirname(base_dir)
        project_root_dir = os.path.dirname(parent_dir_1)
        logo_path = os.path.join(project_root_dir, "assets", "logo.png")

        logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaledToHeight(350, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Nie udało się wczytać logo.")
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # dystans





        self.register_window = None  # Deklaracja atrybutu, który będzie przechowywał instancję okna
        self.register_button = QPushButton("Zarejestruj się")
        self.register_button.clicked.connect(self.show_register_window)

        main_layout.addWidget(self.register_button)
        self.setLayout(main_layout)







    def show_register_window(self):
        # Sprawdź, czy okno już istnieje, żeby uniknąć otwierania wielu okien
        if self.register_window is None:
            self.register_window = RegisterWindow()

        self.register_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RunWindow()
    main_window.showMaximized()
    sys.exit(app.exec())
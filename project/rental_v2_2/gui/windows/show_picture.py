import sys
import os
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "logo.png")

    print("Ścieżka do logo:", logo_path)

    pixmap = QPixmap(logo_path)
    if pixmap.isNull():
        print("❌ Nie udało się załadować obrazka!")
    else:
        print("✅ Logo załadowane poprawnie.")

    window = QWidget()
    window.setWindowTitle("Test ładowania obrazka")

    label = QLabel()
    if not pixmap.isNull():
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
    else:
        label.setText("❌ Nie udało się załadować obrazka!")

    layout = QVBoxLayout()
    layout.addWidget(label)
    window.setLayout(layout)

    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
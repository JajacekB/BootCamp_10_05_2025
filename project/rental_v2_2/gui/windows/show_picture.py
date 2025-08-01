import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLayout
from PySide6.QtGui import QPixmap, QPalette, QColor
from PySide6.QtCore import Qt

def create_simple_widow():

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("To jest coś fajnego")
    window.setGeometry(100, 100, 500, 250)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#2e2e2e"))
    window.setPalette(palette)
    window.setAutoFillBackground(True)

    layout = QVBoxLayout()
    window.setLayout(layout)

    status_label = QLabel("Stan przycisku: Włączony")
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setStyleSheet("color: white; font-size: 16px;")
    layout.addWidget(status_label)

    button_label = QLabel("Przycisk")
    button_label.setAlignment(Qt.AlignCenter)
    button_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 5px;")
    layout.addWidget(button_label)



    toggle_button = QPushButton("Przycisk dwustanowy")
    toggle_button.setCheckable(True)
    toggle_button.setFont(toggle_button.font())
    toggle_button.setStyleSheet(
        "QPushButton { background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px; }"
        "QPushButton:checked { background-color: #f44336; }"  # Kolor po włączeniu
        "QPushButton:hover { background-color: #66BB6A; }"  # Kolor przy najechaniu
        "QPushButton:checked:hover { background-color: #E57373; }"
    )

    toggle_button.setFixedSize(200, 50)
    layout.addWidget(toggle_button, alignment=Qt.AlignCenter)

    def on_button_toggled(checked):
        if checked:
            status_label.setText("Stan przycisku 'Włączony'")
            toggle_button.setText("ON")
            print("\nPrzycisk bistabilny WŁĄCZONY")
        else:
            status_label.setText("Stan przycisku 'Wyłączony'")
            toggle_button.setText("OFF")
            print("Przycisk bistabilny WYŁĄCZONY")

    toggle_button.toggled.connect(on_button_toggled)


    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    create_simple_widow()
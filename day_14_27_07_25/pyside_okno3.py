import sys
from PySide6.QtWidgets import (
QApplication, QWidget, QVBoxLayout,
QLineEdit, QLabel, QPushButton, QStyleFactory
)

def show_text():
    label.setText(textbox.text())

app = QApplication(sys.argv)

print(QStyleFactory.keys())
app.setStyle("Fusion")

dialog = QWidget()
dialog.setWindowTitle("Okno z polem tekstowym")
dialog.setGeometry(100, 100, 300, 150)

textbox = QLineEdit()
textbox.setPlaceholderText("Wpisz coś tutaj...")

label = QLabel("Tekst pojawi się tutaj...")

button = QPushButton("Wyświetl teraz")

button.clicked.connect(show_text)

textbox.returnPressed.connect(show_text)

layout = QVBoxLayout()

layout.addWidget(textbox)
layout.addWidget(button)
layout.addWidget(label)

dialog.setLayout(layout)

dialog.show()
sys.exit(app.exec())
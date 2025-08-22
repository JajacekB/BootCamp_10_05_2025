import PySide6

from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
import re
import sys



def is_valid_phone(phone: str) -> bool:
    """Sprawdza format numeru telefonu."""
    pattern = re.compile(r"^(\+\d{1,3}[ -]?)?\d{3}[ -]?\d{3}[ -]?\d{3}$")
    return bool(pattern.fullmatch(phone))

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Walidacja telefonu")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Wpisz numer telefonu")
        self.phone_input.textChanged.connect(self.validate_phone)

        self.valid_style = """
            QLineEdit {
                border: 2px solid green;
                border-radius: 4px;
                padding: 2px;
                background-color: #eaffea;
            }
        """

        self.invalid_style = """
            QLineEdit {
                border: 2px solid red;
                border-radius: 4px;
                padding: 2px;
                background-color: #ffeaea;
            }
        """

        layout = QVBoxLayout()
        layout.addWidget(self.phone_input)
        self.setLayout(layout)

    def validate_phone(self):
        text = self.phone_input.text()
        if is_valid_phone(text):
            self.phone_input.setStyleSheet(self.valid_style)
        else:
            self.phone_input.setStyleSheet(self.invalid_style)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec())
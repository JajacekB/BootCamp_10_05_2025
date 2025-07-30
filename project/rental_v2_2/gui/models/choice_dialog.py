from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QApplication, QScrollArea, QWidget
)
from PySide6.QtCore import Qt
import sys
import textwrap


class ChoiceDialog(QDialog):
    def __init__(self, prompt: str, options, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wybierz opcję")
        self.choice = None

        # Obsługa słownika i listy
        if isinstance(options, dict):
            self.options = options
        elif isinstance(options, list):
            self.options = {item: item for item in options}
        else:
            raise TypeError("Options musi być listą lub słownikiem")

        # Przygotowanie układu
        layout = QVBoxLayout()

        # Złamanie prompta jeśli za długi
        wrapped_prompt = "\n".join(textwrap.wrap(prompt, width=60))
        label = QLabel(wrapped_prompt)
        label.setWordWrap(True)
        layout.addWidget(label)

        # Scrollable area, jeśli opcji dużo
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        for key, value in self.options.items():
            btn = QPushButton(str(value))
            btn.clicked.connect(lambda checked, k=key: self.select_option(k))
            scroll_layout.addWidget(btn)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(min(len(self.options) * 40, 300))
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.adjustSize()
        self.setFixedWidth(max(self.width(), 400))

    def select_option(self, key):
        self.choice = key
        self.accept()

    @staticmethod
    def get_choice(prompt, options):
        app = QApplication.instance() or QApplication(sys.argv)
        dialog = ChoiceDialog(prompt, options)
        result = dialog.exec()
        return dialog.choice if result == QDialog.Accepted else None



if __name__ == "__main__":
    choice = ChoiceDialog.get_choice(
        "Wybierz kolor pojazdu (zostanie przypisany do wypożyczenia):",
        {"r": "Czerwony", "g": "Zielony", "b": "Niebieski"}
    )
    print("Wybrano:", choice)
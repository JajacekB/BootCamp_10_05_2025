import sys
import textwrap
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
)


class YesNoDialog(QDialog):
    def __init__(self, prompt: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Potwierdzenie")
        self.result = None

        wrapped_prompt = "\n".join(textwrap.wrap(prompt, width=60))
        label = QLabel(wrapped_prompt)
        label.setWordWrap(True)

        btn_yes = QPushButton("Tak")
        btn_no = QPushButton("Nie")

        btn_yes.clicked.connect(self.on_accept)
        btn_no.clicked.connect(self.on_reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.adjustSize()
        self.setFixedWidth(max(self.width(), 300))

    def on_accept(self):
        self.result = True
        print("Tak (True)")
        self.accept()

    def on_reject(self):
        self.result = False
        print("Nie (False)")
        self.reject()

    @staticmethod
    def ask(prompt: str) -> bool | None:
        app = QApplication.instance()
        created_app = False

        if not app:
            app = QApplication(sys.argv)
            created_app = True

        dialog = YesNoDialog(prompt)
        result = dialog.exec()

        if created_app:
            app.quit()

        return dialog.result if result in (QDialog.Accepted, QDialog.Rejected) else None


if __name__ == "__main__":
    odpowiedz = YesNoDialog.ask("Czy na pewno chcesz kontynuować?")
    print("Zwrócona wartość:", odpowiedz)
    sys.exit(0)
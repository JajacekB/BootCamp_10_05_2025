import sys
from datetime import datetime, date
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QCalendarWidget,
    QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class DatePickerDialog(QDialog):
    def __init__(self, title="Wybierz datę", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(300, 300)
        self.selected_date = None

        self.calendar = QCalendarWidget(self)
        self.calendar.setSelectedDate(date.today())
        self.calendar.setGridVisible(True)

        self.label = QLabel(f"Wybrana data: {self.calendar.selectedDate().toString('yyyy-MM-dd')}", self)

        self.calendar.selectionChanged.connect(self.update_label)

        btn_confirm = QPushButton("Zatwierdź")
        btn_cancel = QPushButton("Anuluj")

        btn_confirm.clicked.connect(self.on_confirm)
        btn_cancel.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_confirm)
        button_layout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_label(self):
        self.label.setText(f"Wybrana data: {self.calendar.selectedDate().toString('yyyy-MM-dd')}")

    def on_confirm(self):
        qdate = self.calendar.selectedDate()
        self.selected_date = date(qdate.year(), qdate.month(), qdate.day())
        self.accept()

    @staticmethod
    def get_date(title="Wybierz datę") -> date | None:
        app = QApplication.instance()
        created_app = False

        if not app:
            app = QApplication(sys.argv)
            created_app = True

        dialog = DatePickerDialog(title)
        result = dialog.exec()

        if created_app:
            app.quit()

        return dialog.selected_date if result == QDialog.Accepted else None


if __name__ == "__main__":
    selected = DatePickerDialog.get_date("Wybierz datę wypożyczenia")
    print("Wybrana data:", selected)
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QLineEdit, QToolButton,
    QCalendarWidget, QDialog, QVBoxLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat
import sys

class CalendarCombo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_date = QDate.currentDate()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(150)
        self.layout.setSpacing(0)

        self.line_edit = QLineEdit()
        self.line_edit.setText(self.selected_date.toString("dd-MM-yyyy"))
        self.layout.addWidget(self.line_edit)

        self.button = QToolButton()
        self.button.setText("▼")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.show_calendar)

        self.layout.addStretch(0)


    def show_calendar(self):
        dlg = QDialog(self)
        dlg.setWindowFlags(Qt.Popup)
        layout = QVBoxLayout(dlg)

        self.cal = QCalendarWidget()
        self.cal.setSelectedDate(self.selected_date)
        layout.addWidget(self.cal)

        fmt = QTextCharFormat()
        fmt.setForeground(Qt.black)
        self.cal.setHeaderTextFormat(fmt)
        self.cal.selectionChanged.connect(lambda: self.update_date(dlg))

        dlg.exec()


    def update_date(self, dlg):
        self.selected_date = self.cal.selectedDate()
        self.line_edit.setText(self.selected_date.toString("dd-MM-yyyy"))
        dlg.accept()


    def get_date(self):
        return self.selected_date


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CalendarCombo()
    w.show()
    sys.exit(app.exec())
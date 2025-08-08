import sys
from PySide6.QtWidgets import (
QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QRadioButton, QSlider, QDial, QLineEdit
)
from PySide6.QtCore import  Qt, QTimer
from rich.align import Align


class CustomDial(QDial):
    def wheelEvent(self, event):
        """Metoda obsługująca kręcenie kółkiem myszy."""
        if event.angleDelta().y() > 0:
            self.setValue(self.value() - 1)
        else:
            self.setValue(self.value() + 1)
        # Ważne: Akceptujemy zdarzenie, aby nie było przekazywane dalej
        event.accept()


class MyBasicWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(">>> Jack-Radio <<<")

        self.setGeometry(100, 100, 250, 250)

        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Zielony */
                color: red;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
            }
            /* Styl po najechaniu myszką */
            QPushButton:hover {
                background-color: #66BB6A; /* Jaśniejszy zielony */
                color: red;
            }
            /* Styl dla przycisku wciśniętego */
            QPushButton:pressed {
                background-color: #388E3C; /* Ciemniejszy zielony dla wciśnięcia */
                color: white; /* Zmieniamy kolor tekstu na biały dla kontrastu */
            }            
            QPushButton {
                background-color: #4CAF50;
                color: red;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
                color: red;
            }
            QPushButton:pressed {
                background-color: #388E3C;
                color: white;
            }
            QLabel {
                color: purple;
                font-size: 21px;
                font-weight: bold;
            }           
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ccc;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #5C5C5C;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.lista_osobista = [
            "RMF", "Talk Radio", "Eska", "Anty Radio", "Rock Radio", "Radio Zet",
            "Trójka", "Złote Przeboje", "Melo Radio", 'RMF MAXX', "Jazz Radio"
        ]
        self.longus = len(self.lista_osobista)


        for index, item_text in enumerate(self.lista_osobista):
            button = QPushButton(item_text)
            button.setFixedSize(255, 35)
            main_layout.addWidget(button, alignment=Qt.AlignCenter)
            button.clicked.connect(lambda checked, text=item_text: self._on_dynamic_button_clicked(text))


        self.hello_label = QLabel(">>> Hello there <<<")
        self.hello_label.setStyleSheet("color: purple; font-size: 21px; font-weight: bold;")
        self.hello_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.hello_label, alignment=Qt.AlignBottom)


        self.confirm_button = QPushButton("Turn off")
        self.confirm_button.setFixedSize(255, 50)
        self.confirm_button.setStyleSheet(
        "background-color: grey; color: white; border-radius: 8px; padding: 10px; "
        )
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)


        self.radio_button1 = QRadioButton("FM")
        self.radio_button2 = QRadioButton("AM")
        main_layout.addWidget(self.radio_button1)
        main_layout.addWidget(self.radio_button2)
        self.radio_button1.setChecked(True)


        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Podaj częstotliwość: ")
        self.input_field.setFixedSize(255, 35)

        main_layout.addWidget(self.input_field, alignment=Qt.AlignCenter)


        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setMinimum(810)
        self.gain_slider.setMaximum(1060)
        self.gain_slider.setValue(810)
        self.gain_slider.setSingleStep(1)
        self.gain_slider.setFixedSize(255, 35)
        main_layout.addWidget(self.gain_slider, alignment=Qt.AlignCenter)

        self.gain_dial = CustomDial()
        self.gain_dial.setMinimum(0)
        self.gain_dial.setMaximum(100)
        self.gain_dial.setValue(80)
        self.gain_dial.setFixedSize(100, 100)
        self.gain_dial.setNotchesVisible(True)

        main_layout.addWidget(self.gain_dial, alignment=Qt.AlignCenter)


        self.input_field.returnPressed.connect(self._on_input_entered)
        self.gain_slider.valueChanged.connect(self._update_label_from_slider)
        self.gain_dial.valueChanged.connect(self._update_label_from_dial)
        self.confirm_button.clicked.connect(self._close_and_exit)
        self.radio_button1.toggled.connect(self._on_radio_toggled)
        self.radio_button2.toggled.connect(self._on_radio_toggled)


    def _on_radio_toggled(self):
        if self.radio_button1.isChecked():
            print("Wybrano  Option1")
            self.hello_label.setText("Wybrano: FM")
        elif self.radio_button2.isChecked():
            print("Wybrano  Option2")
            self.hello_label.setText("Wybrano: AM")


    def _on_dynamic_button_clicked(self, button_text):
        trampek = button_text
        print(f"Przycisk '{button_text}' został naciśnięty")
        self.hello_label.setText(f">>> {button_text} <<<")


    def _update_label_from_slider(self, value):
        display_value = value / 10.0
        self.hello_label.setText(f"Frequency: {display_value:.1f} MHz")
        print(f"Ustawiono wartość na: {display_value:.1f}")

    def _update_label_from_dial(self, value):
        db_value = value - 80
        self.hello_label.setText(f"Volume: {db_value} dB")
        print(f"Ustawiono wzmocnienie na: {db_value} dB")


    def _dial_wheelEvent(self, event):
        current_value = self.gain_dial.value()
        if event.angleDelta().y() > 0:
            self.gain_dial.setValue(current_value + 1)
        else:
            self.gain_dial.setValue(current_value - 1)


    def _on_input_entered(self):
        input_text = self.input_field.text()
        print(f"Wprowadzono tekst: {input_text}")
        self.hello_label.setText(f"Ustawiono: {input_text} MHz")
        self.input_field.clear()


    def _close_and_exit(self, off_text):
        self.hello_label.setText(f"Goodbye")
        off_text = "Goodbye"
        print(f"ostatecznie wybrano: '{off_text}'")
        print("\nDo widzenia !!!\n Pa")
        QTimer.singleShot(5000, self.close)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyBasicWindow()
    main_window.show()
    sys.exit(app.exec())



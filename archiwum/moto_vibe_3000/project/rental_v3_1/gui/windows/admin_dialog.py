from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QSpacerItem,
    QPushButton, QGridLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from models.promotions import Promotion


class AdminDialog(QMainWindow):
    command_selected = Signal(str)
    logout = Signal(object)

    def __init__(self, user, session, controller):
        super().__init__()
        print("✅ Inicjalizacja MenuView")
        self.user = user
        self.session = session
        self.controller = controller
        self.dynamic_area = QFrame()
        self.current_widget = None
        self.active_menu_button = None

        if self.user.role == "admin":
            self.setWindowTitle("Menu Admina")
        elif self.user.role == "seller":
            self.setWindowTitle("Menu Sprzedawcy")
        else:
            self.setWindowTitle("Menu:")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: #eee;
                font-size: 18px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            }
        """)

        self._build_ui()
        QTimer.singleShot(0, self.showMaximized)

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(25, 25, 25, 25)
        self.grid_layout.setSpacing(15)

        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

        central_widget.setLayout(self.grid_layout)
        self.current_widget = None

        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(15)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setAlignment(Qt.AlignTop)

        if self.user.role == "admin":
            hello_label = QLabel("Menu Admina:")
        elif self.user.role == "seller":
            hello_label = QLabel("Menu Sprzedawcy:")
        else:
            hello_label = QLabel("Menu:")
        hello_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        hello_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(hello_label)

        info_label = QLabel("Wybierz co chcesz robić:")
        info_label.setStyleSheet("color: #A9C1D9; font-size: 20px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(info_label)

        menu_list = self._get_menu_for_role(self.user.role.lower())

        for item_text in menu_list:
            button = QPushButton(item_text)
            button.setMinimumSize(250, 35)
            button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")

            command_num = item_text.split(".")[0]
            button.clicked.connect(
                lambda checked, b=button, num=command_num: self._on_dynamic_button_clicked_with_highlight(b, num))

            menu_layout.addWidget(button, alignment=Qt.AlignCenter)

        menu_layout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        logoff_button = QPushButton("Wyloguj się")
        logoff_button.setMinimumSize(250, 35)
        logoff_button.setStyleSheet("background-color: brown; color: white; font-size: 18px; border-radius: 8px; padding: 4px;")
        logoff_button.clicked.connect(self._on_logout_clicked)
        menu_layout.addWidget(logoff_button, alignment=Qt.AlignCenter)

        self.menu_container = QWidget()
        self.menu_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.menu_container.setLayout(menu_layout)
        self.grid_layout.addWidget(self.menu_container, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.hamburger_button = QPushButton("☰")
        self.hamburger_button.setMinimumSize(40, 40)
        self.hamburger_button.setStyleSheet(
            "font-size: 22px; background-color: #444; color: white; border-radius: 5px;"
        )
        self.hamburger_button.clicked.connect(self.toggle_menu)
        self.grid_layout.addWidget(self.hamburger_button, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.hamburger_button.hide()
        QTimer.singleShot(0, self.adjust_menu_visibility)

        self.dynamic_area = QWidget()
        self.dynamic_area.setLayout(QVBoxLayout())
        self.dynamic_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.grid_layout.addWidget(self.dynamic_area, 0, 1, 1, 2)  # kolumny 1 i 2

        if self.user.role in ["admin", "seller"]:
            QTimer.singleShot(0, lambda: self._safe_show_overdue_rentals())

        if self.user.role == "client":
            QTimer.singleShot(0, lambda :self._saf_show_promo_banner())


    def _get_menu_for_role(self, role: str) -> list[str]:
        if role == "admin":
            return [
                "1. Dodaj nowego sprzedawcę",
                "2. Usuń sprzedawcę",
                "3. Dodaj nowego księgowego",
                "4. Dodaj nowego klienta",
                "5. Usuń klienta",
                "6. Przeglądaj klientów",
                "7. Dodaj nowy pojazd",
                "8. Usuń pojazd z użytkowania",
                "9. Przeglądaj pojazdy",
                "10. Wypożycz pojazd klientowi",
                "11. Zwróć pojazd",
                "12. Oddaj pojazd do naprawy",
                "13. Aktualizuj profil"
            ]
        elif role == "seller":
            return [
                "1. Dodaj nowego klienta",
                "2. Usuń klienta",
                "3. Przeglądaj klientów",
                "4. Dodaj nowy pojazd",
                "5. Usuń pojazd z użytkowania",
                "6. Przeglądaj pojazdy",
                "7. Wypożycz pojazd klientowi",
                "8. Zwróć pojazd",
                "9. Oddaj pojazd do naprawy",
                "10. Aktualizuj profil"
            ]
        elif role == "client":
            return [
                "1. Przeglądaj pojazdy",
                "2. Wypożycz pojazd",
                "3. Zwróć pojazd",
                "4. Aktualizuj profil"
            ]
        else:
            return []


    def clear_dynamic_area(self):
        layout = self.dynamic_area.layout()
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self.current_widget = None


    def _on_dynamic_button_clicked_with_highlight(self, button, command_num):

        if self.active_menu_button:
            self.active_menu_button.setStyleSheet(
                "color: white; border-radius: 8px; padding-left: 10px; background-color: #555;"
            )

        self.active_menu_button = button
        self.active_menu_button.setStyleSheet(
            "color: black; border-radius: 8px; padding-left: 10px; background-color: beige;"
        )

        self._on_dynamic_button_clicked(command_num, button)


    def _on_dynamic_button_clicked(self, command_num: str, button):
        print(f"Emituję command_selected: {command_num}")
        self.command_selected.emit(command_num)
        self._set_active_menu_button(button)


    def _on_logout_clicked(self):
        print("Emituję sygnał logout")
        self.logout.emit(self.user)


    def load_widget(self, widget):
        self.clear_dynamic_area()
        self.dynamic_area.layout().addWidget(widget)
        self.current_widget = widget


    def _safe_show_overdue_rentals(self):
        try:
            self.controller.show_overdue_rentals_widget()
        except Exception as e:
            print(f"❌ Błąd podczas sprawdzania zaległości: {e}")


    def _saf_show_promo_banner(self):
        try:
            self.controller.show_promo_banner_widget()
        except Exception as e:
            print(f"❌ Błąd podczas odczytywania promocji: {e}")


    def _set_active_menu_button(self, button):

        if self.active_menu_button:
            self.active_menu_button.setStyleSheet(
                "color: white; border-radius: 8px; padding-left: 10px; background-color: #555;"
            )

        self.active_menu_button = button
        self.active_menu_button.setStyleSheet(
            "color: black; border-radius: 8px; padding-left: 10px; background-color: beige;"
        )


    def _build_promo_banner(self):
        time_promos = self.session.query(Promotion).filter_by(type='time').order_by(Promotion.min_days).all()
        loyalty_promos = self.session.query(Promotion).filter_by(type='loyalty').all()

        banner_text = "🎉 PROMOCJE:\n"
        if time_promos:
            banner_text += "🏷️ Zniżki czasowe:\n"
            for promo in time_promos:
                banner_text += f"  • {promo.discount_percent:.0f}% za ≥ {promo.min_days} dni\n"

        if loyalty_promos:
            banner_text += "💎 Program lojalnościowy:\n"
            for promo in loyalty_promos:
                banner_text += f"  • {promo.description}\n"

        return banner_text


    def toggle_menu(self):

        if self.menu_container.isVisible():
            self.menu_container.hide()
        else:
            self.menu_container.show()


    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.adjust_menu_visibility()


    def adjust_menu_visibility(self):
        window_width = self.width()

        menu_width = self.menu_container.sizeHint().width()
        dynamic_min = 500

        if window_width < 1000:
            self.menu_container.hide()
            self.hamburger_button.show()
            self.setMinimumWidth(dynamic_min + 100)
        else:
            self.menu_container.show()
            self.hamburger_button.hide()
            self.setMinimumWidth(menu_width + dynamic_min)


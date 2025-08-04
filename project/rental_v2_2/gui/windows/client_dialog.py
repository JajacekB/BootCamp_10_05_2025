from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, Signal
from models.promotions import Promotion


class ClientDialog(QDialog):

    command_selected = Signal(str)
    logout = Signal(object)

    def __init__(self, user, session, controller):
        super().__init__()
        print("✅ Inicjalizacja AdminDialog")
        self.user = user
        self.session = session
        self.controller = controller

        self.setWindowTitle("Menu klienta")
        # self.setGeometry(650, 150, 350, 450)

        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
                color: #eee;
                font-size: 16px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.valid_style = "border: 1px solid #4CAF50;"
        self.invalid_style = "border: 1px solid #F44336;"

        self.setup_ui()
        self.showMaximized()


    def setup_ui(self):
        menu_list = [
            "1. Przeglądaj pojazdy",
            "2. Wypożycz pojazd",
            "3. Zwróć pojazd",
            "4. Aktualizuj profil"
        ]

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        self.promo_banner = QLabel(self._build_promo_banner())
        self.promo_banner.setStyleSheet("""
            color: #00FFCC;
            font-size: 14px;
            font-weight: bold;
            border: 1px dashed #888;
            padding: 10px;
            background-color: #1e1e1e;
        """)
        self.promo_banner.setWordWrap(True)
        self.promo_banner.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.promo_banner)

        for item_text in menu_list:
            button = QPushButton(item_text)
            button.setFixedSize(255, 31)
            button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")
            main_layout.addWidget(button, alignment=Qt.AlignCenter)

            command_num = item_text.split(".")[0]
            button.clicked.connect(lambda checked, num=command_num: self._on_dynamic_button_clicked(num))

        info_label = QLabel("Wybierz co chcesz robić:")
        info_label.setStyleSheet("color: purple; font-size: 18px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)

        self.logoff_button = QPushButton("Wyloguj się")
        self.logoff_button.setFixedSize(255, 50)
        self.logoff_button.setStyleSheet("color: white; font-size: 18px; border-radius: 8px; padding: 10px;")
        main_layout.addWidget(self.logoff_button, alignment=Qt.AlignCenter)

        self.logoff_button.clicked.connect(self._on_logout_clicked)


    def _on_dynamic_button_clicked(self, command_num: str):
        print(f"Emituję command_selected: {command_num}")
        self.command_selected.emit(command_num)


    def _on_logout_clicked(self):
        print("Emituję sygnał logout")
        self.logout.emit(self.user)


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


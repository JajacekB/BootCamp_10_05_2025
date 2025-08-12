from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QMainWindow, QWidget, QGridLayout, QFrame
from PySide6.QtCore import Qt, QTimer, Signal

from models.promotions import Promotion
from gui.windows.register_wiget import RegisterWidget


class ClientDialog(QMainWindow):
    command_selected = Signal(str)
    logout = Signal(object)

    def __init__(self, user, session, controller):
        super().__init__()
        print("✅ Inicjalizacja ClientDialog")
        self.user = user
        self.session = session
        self.controller = controller
        self.dynamic_area = QFrame()
        self.current_widget = None

        self.setWindowTitle("Menu klienta")
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
        # self.valid_style = "border: 1px solid #4CAF50;"
        # self.invalid_style = "border: 1px solid #F44336;"

        self._build_ui()
        self.showMaximized()


    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(25, 25, 25, 25)
        self.grid_layout.setSpacing(15)

        self.grid_layout.setColumnStretch(0, 0)  # menu nie rozciąga się
        self.grid_layout.setColumnStretch(1, 1)  # dynamic_area zajmuje resztę

        central_widget.setLayout(self.grid_layout)
        self.current_widget = None

        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(15)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setAlignment(Qt.AlignTop)

        hello_label = QLabel("Menu Admina")
        hello_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        hello_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(hello_label)

        menu_list = [
            "1. Przeglądaj pojazdy",
            "2. Wypożycz pojazd",
            "3. Zwróć pojazd",
            "4. Aktualizuj profil"
        ]

        menu_layout = QVBoxLayout(self)
        menu_layout.setContentsMargins(30, 30, 30, 30)
        menu_layout.setSpacing(15)

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
        menu_layout.addWidget(self.promo_banner)

        for item_text in menu_list:
            button = QPushButton(item_text)
            button.setFixedSize(255, 31)
            button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")
            menu_layout.addWidget(button, alignment=Qt.AlignCenter)
            command_num = item_text.split(".")[0]
            button.clicked.connect(lambda checked, num=command_num: self._on_dynamic_button_clicked(num))

        info_label = QLabel("Wybierz co chcesz robić:")
        info_label.setStyleSheet("color: purple; font-size: 18px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(info_label)

        self.logoff_button = QPushButton("Wyloguj się")
        self.logoff_button.setFixedSize(255, 50)
        self.logoff_button.setStyleSheet("color: white; font-size: 18px; border-radius: 8px; padding: 10px;")
        self.logoff_button.clicked.connect(self._on_logout_clicked)
        menu_layout.addWidget(self.logoff_button, alignment=Qt.AlignCenter)

        menu_container = QWidget()
        menu_container.setLayout(menu_layout)
        self.grid_layout.addWidget(menu_container, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.dynamic_area = QWidget()
        self.dynamic_area.setLayout(QVBoxLayout())
        self.grid_layout.addWidget(self.dynamic_area, 0, 1, 1, 2)  # kolumny 1 i 2


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


    def _on_dynamic_button_clicked(self, command_num: str):
        print(f"Emituję command_selected: {command_num}")
        self.command_selected.emit(command_num)


    def _on_logout_clicked(self):
        print("Emituję sygnał logout")
        self.logout.emit(self.user)


    def load_widget(self, widget):
        self.clear_dynamic_area()
        self.dynamic_area.layout().addWidget(widget)
        self.current_widget = widget


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


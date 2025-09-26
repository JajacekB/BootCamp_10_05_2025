from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt,Signal, QTimer


class PromoBannerView(QWidget):

    handle_promo_banner_data = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;                
            }
            QLabel {
                color: #00FFCC;
                font-size: 25px;                
                border: 2px double #A9C1D9;
                border-radius: 10px;
                padding: 10px;
                
            }
        """)
        # font-weight: bold;
        # solid  → linia ciągła
        # dashed → linia przerywana(kreski)
        # dotted → linia kropkowana
        # double → linia podwójna
        # background - color:  # 1e1e1e;

        self._build_ui()

    def _build_ui(self):

        main_layout = QVBoxLayout()

        self.promo_banner = QLabel("Trouble")

        self.promo_banner.setWordWrap(True)
        self.promo_banner.setAlignment(Qt.AlignCenter)

        spacer = QSpacerItem(20, 38, QSizePolicy.Minimum, QSizePolicy.Maximum)
        main_layout.addSpacerItem(spacer)
        main_layout.addWidget(self.promo_banner)

        main_layout.addStretch()

        self.setLayout(main_layout)
        QTimer.singleShot(0, lambda: self._handle_build_promo_banner())


    def _handle_build_promo_banner(self):

        self.handle_promo_banner_data.emit()

    def build_promo_banner(self, time_promos: str, loyalty_promos: str):

        banner_text = "\n🎉 PROMOCJE:\n"
        if time_promos:
            banner_text += "🏷️ Zniżki czasowe:\n"
            for promo in time_promos:
                banner_text += f"  • {promo.discount_percent:.0f}% za ≥ {promo.min_days} dni\n"

        if loyalty_promos:
            banner_text += "💎 Program lojalnościowy:\n"
            for promo in loyalty_promos:
                banner_text += f"  • {promo.description}\n"

        self.promo_banner.setText(banner_text)

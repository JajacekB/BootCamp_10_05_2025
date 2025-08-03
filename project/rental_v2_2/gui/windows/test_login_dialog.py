import sys
from PySide6.QtWidgets import QApplication
from database.base import SessionLocal, Session  # lub inna funkcja, która daje db_session
from gui.login_dialog import L  # zakładam, że tam masz klasę LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Pobierz sesję do bazy danych
    session = get_session()

    # Utwórz i pokaż okno logowania
    login = LoginDialog(session)
    login.exec()  # Blokująco — czeka na zamknięcie okna

    sys.exit(0)
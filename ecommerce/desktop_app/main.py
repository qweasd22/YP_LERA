import sys
from PyQt6.QtWidgets import QApplication
from api_client import APIClient
from ui.login import LoginDialog
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    client = APIClient("http://localhost:18800/")
    login = LoginDialog(client)
    if login.exec() == LoginDialog.DialogCode.Accepted:
        window = MainWindow(client)
        window.show()
        sys.exit(app.exec())
    sys.exit()

if __name__ == "__main__":
    main()

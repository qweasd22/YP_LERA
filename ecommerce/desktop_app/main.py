import sys
from PyQt6.QtWidgets import QApplication
from api_client import APIClient
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog

def main():
    app = QApplication(sys.argv)
    
    # Инициализация API-клиента
    api_client = APIClient()
    
    # Показ диалога авторизации
    login_dialog = LoginDialog(api_client)
    if login_dialog.exec() == LoginDialog.DialogCode.Accepted:
        # Запуск главного окна после успешной авторизации
        window = MainWindow(api_client)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
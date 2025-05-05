from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Авторизация")
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel("Логин"))
        self.user = QLineEdit()
        self.layout().addWidget(self.user)

        self.layout().addWidget(QLabel("Пароль"))
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout().addWidget(self.pw)

        btn = QPushButton("Войти")
        btn.clicked.connect(self._auth)
        self.layout().addWidget(btn)

    def _auth(self):
        if self.api.login(self.user.text(), self.pw.text()):
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверные учётные данные")

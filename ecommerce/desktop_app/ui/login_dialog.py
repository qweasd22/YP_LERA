from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Авторизация")
        self.layout = QVBoxLayout()
        
        # Поля ввода
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Кнопка входа
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.authenticate)
        
        # Добавление элементов
        self.layout.addWidget(QLabel("Логин:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Пароль:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_btn)
        
        self.setLayout(self.layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.api_client.login(username, password):
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверные учетные данные!")
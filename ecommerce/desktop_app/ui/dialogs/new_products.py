from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class NewProductDialog(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Новый товар")
        self.layout = QVBoxLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.wholesale_input = QLineEdit()
        self.retail_input = QLineEdit()
        self.description_input = QLineEdit()

        # Кнопка
        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self.create_product)

        # Сборка интерфейса
        self.layout.addWidget(QLabel("Название:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Оптовая цена:"))
        self.layout.addWidget(self.wholesale_input)
        self.layout.addWidget(QLabel("Розничная цена:"))
        self.layout.addWidget(self.retail_input)
        self.layout.addWidget(QLabel("Описание:"))
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def validate_input(self) -> bool:
        """Проверка корректности ввода"""
        if not self.wholesale_input.text().replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Ошибка", "Некорректная оптовая цена!")
            return False
        if not self.retail_input.text().replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Ошибка", "Некорректная розничная цена!")
            return False
        return True

    def create_product(self):
        if not self.validate_input():
            return

        data = {
            "name": self.name_input.text(),
            "wholesale_price": float(self.wholesale_input.text()),
            "retail_price": float(self.retail_input.text()),
            "description": self.description_input.text()
        }

        if self.api_client.create_product(data):
            QMessageBox.information(self, "Успех", "Товар создан!")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать товар!")
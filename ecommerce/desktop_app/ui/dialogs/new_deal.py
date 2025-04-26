from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, 
    QLineEdit, QPushButton, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt

class NewDealDialog(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Новая сделка")
        self.setMinimumWidth(400)
        self.layout = QVBoxLayout()
        
        # Элементы формы
        self.customer_combo = QComboBox()
        self.product_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.is_wholesale_check = QCheckBox("Оптовая сделка")
        
        # Загрузка данных
        self.load_customers()
        self.load_products()
        
        # Кнопки
        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self.create_deal)
        
        # Сборка интерфейса
        self.layout.addWidget(QLabel("Покупатель:"))
        self.layout.addWidget(self.customer_combo)
        self.layout.addWidget(QLabel("Товар:"))
        self.layout.addWidget(self.product_combo)
        self.layout.addWidget(QLabel("Количество:"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(self.is_wholesale_check)
        self.layout.addWidget(self.submit_btn)
        
        self.setLayout(self.layout)

    def load_customers(self):
        """Загрузка списка покупателей"""
        customers = self.api_client.get_customers()
        self.customer_combo.clear()
        for customer in customers:
            self.customer_combo.addItem(customer["name"], customer["id"])

    def load_products(self):
        """Загрузка списка товаров"""
        products = self.api_client.get_products()
        self.product_combo.clear()
        for product in products:
            self.product_combo.addItem(product["name"], product["id"])

    def validate_input(self) -> bool:
        """Проверка корректности ввода"""
        if not self.quantity_input.text().isdigit():
            QMessageBox.warning(self, "Ошибка", "Количество должно быть числом!")
            return False
        if int(self.quantity_input.text()) <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество должно быть больше нуля!")
            return False
        return True

    def create_deal(self):
        """Отправка данных на сервер"""
        if not self.validate_input():
            return

        data = {
            "customer": self.customer_combo.currentData(),
            "items": [{
                "product": self.product_combo.currentData(),
                "quantity": int(self.quantity_input.text())
            }],
            "is_wholesale": self.is_wholesale_check.isChecked(),
            "discount": 0  # Пример, можно добавить поле для скидки
        }

        if self.api_client.create_deal(data):
            QMessageBox.information(self, "Успех", "Сделка создана!")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать сделку!")
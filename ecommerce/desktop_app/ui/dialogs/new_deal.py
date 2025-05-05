from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QLineEdit, QCheckBox, QPushButton, QMessageBox
from api_client import APIClient

class NewDealDialog(QDialog):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.setWindowTitle("Новая сделка")
        form = QFormLayout(self)

        self.customer = QComboBox(); form.addRow("Покупатель:", self.customer)
        self.product = QComboBox(); form.addRow("Товар:", self.product)
        self.quantity = QLineEdit("1"); form.addRow("Количество:", self.quantity)
        self.is_wholesale = QCheckBox(); form.addRow("Оптовая сделка:", self.is_wholesale)

        btn = QPushButton("Создать")
        btn.clicked.connect(self._create)
        form.addRow(btn)

        self._load_customers(); self._load_products()

    def _load_customers(self):
        for c in self.api.get_customers():
            self.customer.addItem(c.get('name',''), c.get('id'))

    def _load_products(self):
        for p in self.api.get_products():
            self.product.addItem(p.get('name',''), p.get('id'))

    def _create(self):
        try:
            qty = int(self.quantity.text())
            if qty < 1: raise ValueError
        except:
            QMessageBox.warning(self, "Ошибка", "Количество должно быть числом >0")
            return
        data = {
            'customer': self.customer.currentData(),
            'is_wholesale': self.is_wholesale.isChecked(),
            'discount': 0,
            'items': [{'product': self.product.currentData(), 'quantity': qty}]
        }
        # скидка по порогам
        if qty >= 1000:
            data['discount'] = 20
        elif qty >= 100:
            data['discount'] = 10
        elif qty >= 10:
            data['discount'] = 5

        res = self.api.create_deal(data)
        if res:
            QMessageBox.information(self, "Успех", "Сделка создана")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать сделку")
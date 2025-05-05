from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QLineEdit, QCheckBox, QPushButton, QMessageBox

class NewDealDialog(QDialog):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Новая сделка")
        form = QFormLayout(self)

        # Загрузка клиентов и товаров
        self.customer = QComboBox()
        for c in api.get_customers():
            self.customer.addItem(c["name"], c["id"])
        form.addRow("Клиент:", self.customer)

        self.product = QComboBox()
        for p in api.get_products():
            self.product.addItem(p["name"], p["id"])
        form.addRow("Товар:", self.product)

        self.quantity = QLineEdit("1")
        form.addRow("Количество:", self.quantity)

        self.is_wholesale = QCheckBox("Оптовая сделка")
        form.addRow("", self.is_wholesale)

        btn = QPushButton("Создать")
        btn.clicked.connect(self._save)
        form.addRow(btn)

    def _save(self):
        # Валидация
        try:
            qty = int(self.quantity.text())
            if qty < 1: raise ValueError
        except:
            QMessageBox.warning(self, "Ошибка", "Количество должно быть целым > 0")
            return

        data = {
            "customer": self.customer.currentData(),
            "is_wholesale": self.is_wholesale.isChecked(),
            "discount": 0,  # сервер сам рассчитает дисконт, либо добавьте логику здесь
            "items": [
                {"product": self.product.currentData(), "quantity": qty}
            ]
        }

        if self.api.create_deal(data):
            QMessageBox.information(self, "Успех", "Сделка создана")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать сделку")

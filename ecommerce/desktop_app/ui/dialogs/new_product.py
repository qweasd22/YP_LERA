from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox

class NewProductDialog(QDialog):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Создать новый товар")

        form = QFormLayout(self)

        self.name_field = QLineEdit()
        form.addRow("Наименование:", self.name_field)

        self.price_field = QLineEdit()
        self.price_field.setPlaceholderText("Например: 199.99")
        form.addRow("Цена (₽):", self.price_field)

        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self._on_submit)
        form.addRow(self.submit_btn)

    def _on_submit(self):
        name = self.name_field.text().strip()
        price_text = self.price_field.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Наименование не может быть пустым.")
            return

        try:
            price = float(price_text)
            if price < 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену (число ≥ 0).")
            return

        data = {"name": name, "price": price}
        result = self.api.create_product(data)
        if result:
            QMessageBox.information(self, "Успех", "Товар успешно создан.")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать товар на сервере.")

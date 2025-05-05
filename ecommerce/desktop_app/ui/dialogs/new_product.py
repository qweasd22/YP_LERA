from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
from api_client import APIClient

class NewProductDialog(QDialog):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.setWindowTitle("Новый товар")
        form = QFormLayout(self)

        self.name = QLineEdit(); form.addRow("Наименование:", self.name)
        self.price = QLineEdit(); form.addRow("Цена:", self.price)

        btn = QPushButton("Создать")
        btn.clicked.connect(self._save)
        form.addRow(btn)

    def _save(self):
        try:
            name = self.name.text().strip()
            price = float(self.price.text())
            if not name:
                raise ValueError("Пустое название")
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные данные")
            return
        data = {
            "name": name,
            "price": price
        }
        res = self.api.create_product(data)
        if res:
            QMessageBox.information(self, "Успех", "Товар создан!")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать товар")

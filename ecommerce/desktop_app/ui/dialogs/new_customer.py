from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
from api_client import APIClient

class NewCustomerDialog(QDialog):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.setWindowTitle("Новый покупатель")
        form = QFormLayout(self)

        self.name = QLineEdit(); form.addRow("Название:", self.name)
        self.address = QLineEdit(); form.addRow("Адрес:", self.address)
        self.phone = QLineEdit(); form.addRow("Телефон:", self.phone)
        self.contact_person = QLineEdit(); form.addRow("Контактное лицо:", self.contact_person)

        btn = QPushButton("Создать")
        btn.clicked.connect(self._save)
        form.addRow(btn)

    def _save(self):
        data = {
            "name": self.name.text(),
            "address": self.address.text(),
            "phone": self.phone.text(),
            "contact_person": self.contact_person.text()
        }
        result = self.api.create_customer(data)
        if result:
            QMessageBox.information(self, "Успех", "Покупатель создан!")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать покупателя")
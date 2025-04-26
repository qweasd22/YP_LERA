from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox, QCheckBox

class NewCustomerDialog(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Новый покупатель")
        self.layout = QVBoxLayout()
        
        # Поля ввода
        self.name_input = QLineEdit()
        self.adress_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.contact_person_input = QLineEdit()
        
        # Кнопка создания
        self.create_btn = QPushButton("Создать")
        self.create_btn.clicked.connect(self.create_customer)
        
        # Добавление элементов
        self.layout.addWidget(QLabel("Название:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Адрес:"))
        self.layout.addWidget(self.adress_input)
        self.layout.addWidget(QLabel("Телефон:"))
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(QLabel("Контактное лицо:"))
        self.layout.addWidget(self.contact_person_input)
        self.layout.addWidget(self.create_btn)
        
        self.setLayout(self.layout)
        
    def create_customer(self):
        name = self.name_input.text()
        address = self.adress_input.text()
        phone = self.phone_input.text()
        contact_person = self.contact_person_input.text()
        
        # Правильный вызов с 4 аргументами
        if self.api_client.create_customer(name, address, phone, contact_person):
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать покупателя")
        
        
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class CustomersWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.layout = QVBoxLayout()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Название", 
            "Адрес", 
            "Телефон", 
            "Контактное лицо"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def load_data(self):
        customers = self.api_client.get_customers()
        self.table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(customer.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(customer.get("address", "")))
            self.table.setItem(row, 2, QTableWidgetItem(customer.get("phone", "")))
            self.table.setItem(row, 3, QTableWidgetItem(customer.get("contact_person", "")))

    
    
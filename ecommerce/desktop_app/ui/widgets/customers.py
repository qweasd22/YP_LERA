from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from ..dialogs.new_customres import NewCustomerDialog
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
        self.new_customer_btn = QPushButton("Новый покупатель")
        self.new_customer_btn.clicked.connect(self.show_create_dialog)
        self.layout.addWidget(self.new_customer_btn)
        self.setLayout(self.layout)
    
    def show_create_dialog(self):
        dialog = NewCustomerDialog(self.api_client)
        dialog.exec()

    def load_data(self):
        try:
            customers = self.api_client.get_customers()
            print("Customers:", customers)
            if not customers:
                print("No customers data received from API")
                return
            self.table.setRowCount(len(customers))
            for row, customer in enumerate(customers):
                print("Customer:", customer)
                self.table.setItem(row, 0, QTableWidgetItem(customer.get("name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(customer.get("address", "")))
                self.table.setItem(row, 2, QTableWidgetItem(customer.get("phone", "")))
                self.table.setItem(row, 3, QTableWidgetItem(customer.get("contact_person", "")))
        except Exception as e:
            print("Error loading customers data:", e)

    
    
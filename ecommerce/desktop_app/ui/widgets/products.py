from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from ..dialogs.new_products import NewProductDialog
class ProductsWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.layout = QVBoxLayout()
        self.init_ui()
        self.load_data()

        self.show_create_dialog_btn = QPushButton("Создать товар")
        self.show_create_dialog_btn.clicked.connect(self.show_create_dialog)
        self.layout.addWidget(self.show_create_dialog_btn)

        self.setLayout(self.layout)

    def show_create_dialog(self):
        dialog = NewProductDialog(self.api_client)
        dialog.exec()
    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Название", 
            "Оптовая цена", 
            "Розничная цена", 
            "Описание"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def load_data(self):
        products = self.api_client.get_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(product.get("wholesale_price", 0))))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.get("retail_price", 0))))
            self.table.setItem(row, 3, QTableWidgetItem(product.get("description", "")))
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt
from ..dialogs.new_deal import NewDealDialog

class DealsWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.layout = QVBoxLayout()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Дата", "Покупатель", "Тип", "Сумма", "Статус"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.new_deal_btn = QPushButton("Новая сделка")
        self.new_deal_btn.clicked.connect(self.show_create_dialog)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.new_deal_btn)
        self.setLayout(self.layout)

    def load_data(self):
        deals = self.api_client.get_deals()
        self.table.setRowCount(len(deals))
        
        for row, deal in enumerate(deals):
            date = deal.get("date", "")
            
            deal_type = "Опт" if deal.get("is_wholesale", False) else "Розница"
            total = f"{deal.get('total', 0):.2f} ₽"
            status = "Завершена" if deal.get("is_completed", False) else "В процессе"
            
            customer_name = deal.get("customer_name", "")
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(customer_name))
            self.table.setItem(row, 2, QTableWidgetItem(deal_type))
            self.table.setItem(row, 3, QTableWidgetItem(total))
            self.table.setItem(row, 4, QTableWidgetItem(status))

    def show_create_dialog(self):
        dialog = NewDealDialog(self.api_client)
        if dialog.exec():
            self.load_data()  # Обновить таблицу

    
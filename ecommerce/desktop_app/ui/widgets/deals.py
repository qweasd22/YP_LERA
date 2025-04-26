from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt
from typing import List, Dict, Any

class DealsWidget(QWidget):
    def __init__(self, api_client: Any) -> None:
        """Initialize the DealsWidget with an API client."""
        super().__init__()
        self.api_client = api_client
        self.layout = QVBoxLayout()
        self.init_ui()
        self.load_data()

    def init_ui(self) -> None:
        """Set up the user interface elements."""
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Дата", 
            "Покупатель", 
            "Тип", 
            "Сумма", 
            "Статус"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.new_deal_btn = QPushButton("Новая сделка")
        self.new_deal_btn.clicked.connect(self.show_create_dialog)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.new_deal_btn)
        self.setLayout(self.layout)

    def load_data(self) -> None:
        """Load deals data into the table."""
        deals: List[Dict[str, Any]] = self.api_client.get_deals()
        self.table.setRowCount(len(deals))
        for row, deal in enumerate(deals):
            
            self.table.setItem(row, 1, QTableWidgetItem(deal.get("customer", "")))
            self.table.setItem(row, 0, QTableWidgetItem(deal.get("date", "")))
            self.table.setItem(row, 2, QTableWidgetItem(deal.get("type", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(deal.get("total", 0))))
            self.table.setItem(row, 4, QTableWidgetItem(deal.get("status", "")))
            
    def show_create_dialog(self) -> None:
        """Show the dialog to create a new deal."""
        pass

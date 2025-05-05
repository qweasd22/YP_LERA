from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QHeaderView
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from ui.dialogs.new_deal import NewDealDialog
from api_client import APIClient

class DealLoadThread(QThread):
    data_ready = pyqtSignal(list)
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
    def run(self):
        data = self.api.get_deals()
        self.data_ready.emit(data)

class DealsWidget(QWidget):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.layout = QVBoxLayout(self)

        hl = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск сделок...")
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search)

        btn_new = QPushButton("➕ Новая сделка")
        btn_new.clicked.connect(self._new_deal)
        hl.addWidget(btn_new)
        self.layout.addLayout(hl)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Дата", "Покупатель", "Кол-во", "Скидка", "Сумма"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        self._load_data()

    def _load_data(self):
        self.thread = DealLoadThread(self.api)
        self.thread.data_ready.connect(self._fill_table)
        self.thread.start()

    def _fill_table(self, deals):
        self.all_data = deals
        self.table.setRowCount(len(deals))
        for r, d in enumerate(deals):
            date = d.get("date", "")
            cust = d.get("customer_name", "")
            items = d.get("items", [])
            qty = sum(i.get("quantity", 0) for i in items)
            disc = d.get("discount", 0)
            total = d.get("total", 0)
            self.table.setItem(r, 0, QTableWidgetItem(date))
            self.table.setItem(r, 1, QTableWidgetItem(cust))
            self.table.setItem(r, 2, QTableWidgetItem(str(qty)))
            self.table.setItem(r, 3, QTableWidgetItem(f"{disc}%"))
            self.table.setItem(r, 4, QTableWidgetItem(f"{total:.2f} ₽"))
        self._filter()

    def _filter(self):
        ft = self.search.text().lower()
        for r in range(self.table.rowCount()):
            row_text = " ".join(self.table.item(r, c).text().lower() for c in range(5))
            self.table.setRowHidden(r, ft not in row_text)

    def _new_deal(self):
        dlg = NewDealDialog(self.api)
        if dlg.exec():
            self._load_data()

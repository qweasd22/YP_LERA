from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QHeaderView
from PyQt6.QtCore import QThread, pyqtSignal
from ui.dialogs.new_customer import NewCustomerDialog
from api_client import APIClient

class CustomerLoadThread(QThread):
    data_ready = pyqtSignal(list)

    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api

    def run(self):
        data = self.api.get_customers()
        self.data_ready.emit(data)

class CustomersWidget(QWidget):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.layout = QVBoxLayout(self)

        # Поиск и кнопка создания
        hl = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск покупателей...")
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search)

        btn_new = QPushButton("➕ Новый покупатель")
        btn_new.clicked.connect(self._new_customer)
        hl.addWidget(btn_new)
        self.layout.addLayout(hl)

        # Таблица
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Название", "Адрес", "Телефон", "Контактное лицо"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        self._load_data()

    def _load_data(self):
        self.thread = CustomerLoadThread(self.api)
        self.thread.data_ready.connect(self._fill_table)
        self.thread.start()

    def _fill_table(self, data):
        self.all_data = data
        self.table.setRowCount(len(data))
        for r, cust in enumerate(data):
            self.table.setItem(r, 0, QTableWidgetItem(cust.get("name", "")))
            self.table.setItem(r, 1, QTableWidgetItem(cust.get("address", "")))
            self.table.setItem(r, 2, QTableWidgetItem(cust.get("phone", "")))
            self.table.setItem(r, 3, QTableWidgetItem(cust.get("contact_person", "")))
        self._filter()

    def _filter(self):
        ft = self.search.text().lower()
        for r in range(self.table.rowCount()):
            texts = []
            for c in range(self.table.columnCount()):
                item = self.table.item(r, c)
                texts.append(item.text().lower() if item is not None else "")
            row_text = " ".join(texts)
            self.table.setRowHidden(r, ft not in row_text)

    def _new_customer(self):
        dlg = NewCustomerDialog(self.api)
        if dlg.exec():
            self._load_data()

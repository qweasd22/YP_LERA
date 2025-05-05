from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QHeaderView
from PyQt6.QtCore import QThread, pyqtSignal
from ui.dialogs.new_product import NewProductDialog
from api_client import APIClient

class ProductLoadThread(QThread):
    data_ready = pyqtSignal(list)

    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api

    def run(self):
        products = self.api.get_products()
        self.data_ready.emit(products)

class ProductsWidget(QWidget):
    def __init__(self, api: APIClient):
        super().__init__()
        self.api = api
        self.layout = QVBoxLayout(self)

        # Поиск и кнопка создания
        hl = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск товаров...")
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search)

        btn_new = QPushButton("➕ Новый товар")
        btn_new.clicked.connect(self._new_product)
        hl.addWidget(btn_new)
        self.layout.addLayout(hl)

        # Таблица
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Наименование", "Цена"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        self._load_data()

    def _load_data(self):
        self.thread = ProductLoadThread(self.api)
        self.thread.data_ready.connect(self._fill_table)
        self.thread.start()

    def _fill_table(self, products):
        self.all_data = products
        self.table.setRowCount(len(products))
        for r, p in enumerate(products):
            name = p.get("name", "")
            price_raw = p.get("price", 0)
            # Конвертация цены в float, если она строка
            try:
                price = float(price_raw)
            except (TypeError, ValueError):
                price = 0.0

            self.table.setItem(r, 0, QTableWidgetItem(name))
            # Форматируем цену как число с двумя знаками
            self.table.setItem(r, 1, QTableWidgetItem(f"{price:.2f}"))
        self._filter()

    def _filter(self):
        ft = self.search.text().lower()
        for r in range(self.table.rowCount()):
            name_item = self.table.item(r, 0)
            price_item = self.table.item(r, 1)
            row_text = (name_item.text() if name_item else "") + " " + (price_item.text() if price_item else "")
            self.table.setRowHidden(r, ft not in row_text.lower())

    def _new_product(self):
        dlg = NewProductDialog(self.api)
        if dlg.exec():
            self._load_data()
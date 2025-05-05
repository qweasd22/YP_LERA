from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from ui.dialogs.new_customer import NewCustomerDialog

class LoadCustomersThread(QThread):
    data_ready = pyqtSignal(list)
    def __init__(self, api): super().__init__(); self.api = api
    def run(self): self.data_ready.emit(self.api.get_customers())

class CustomersWidget(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.layout = QVBoxLayout(self)

        hl = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search)

        btn_new = QPushButton("➕ Покупатель")
        btn_new.clicked.connect(self._new)
        hl.addWidget(btn_new)
        self.layout.addLayout(hl)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Имя","Адрес","Телефон","Контакт"])
        self.layout.addWidget(self.table)

        self._load()

    def _load(self):
        self.thread = LoadCustomersThread(self.api)
        self.thread.data_ready.connect(self._fill)
        self.thread.start()

    def _fill(self, data):
        self.all_data = data or []
        self.table.setRowCount(len(self.all_data))
        for r, c in enumerate(self.all_data):
            self.table.setItem(r, 0, QTableWidgetItem(c.get("name","")))
            self.table.setItem(r, 1, QTableWidgetItem(c.get("address","")))
            self.table.setItem(r, 2, QTableWidgetItem(c.get("phone","")))
            self.table.setItem(r, 3, QTableWidgetItem(c.get("contact_person","")))
        self._filter()

    def _filter(self):
        ft = self.search.text().lower()
        for r in range(self.table.rowCount()):
            texts = []
            for c in range(self.table.columnCount()):
                itm = self.table.item(r, c)
                texts.append(itm.text().lower() if itm else "")
            row_text = " ".join(texts)
            self.table.setRowHidden(r, ft not in row_text)

    def _new(self):
        dlg = NewCustomerDialog(self.api)
        if dlg.exec():
            self._load()

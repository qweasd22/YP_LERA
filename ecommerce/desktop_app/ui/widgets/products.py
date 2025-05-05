# ui/widgets/products.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import QThread, pyqtSignal
from ui.dialogs.new_product import NewProductDialog

class LoadProductsThread(QThread):
    data_ready = pyqtSignal(list)

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client

    def run(self):
        products = self.api.get_products() or []
        self.data_ready.emit(products)

class ProductsWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.thread = None  # Инициализируем атрибут потока

        # Layout
        self.layout = QVBoxLayout(self)

        # Верхняя панель (поиск + кнопка)
        top_bar = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск по названию...")
        self.search.textChanged.connect(self._filter_rows)
        top_bar.addWidget(self.search)

        btn_new = QPushButton("➕ Новый товар")
        btn_new.clicked.connect(self._open_new_dialog)
        top_bar.addWidget(btn_new)

        self.layout.addLayout(top_bar)

        # Таблица: 2 колонки
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Наименование", "Цена (₽)"])
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

        # Загружаем данные
        self.reload()

    def reload(self):
        """Запускаем поток для получения списка товаров."""
        # Если поток уже запущен и активен — корректно остановим его
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        # Новый поток загрузки
        self.thread = LoadProductsThread(self.api)
        self.thread.data_ready.connect(self._populate_table)

        # После завершения потока обнуляем ссылку на него
        self.thread.finished.connect(self._clear_thread)
        self.thread.start()

    def _clear_thread(self):
        """Сбрасываем ссылку на поток после его завершения, чтобы избежать ошибок."""
        self.thread = None

    def _populate_table(self, products):
        """Полностью перезаполняем таблицу новыми данными."""
        self.table.setSortingEnabled(False)  # Отключаем сортировку
        self.table.clearContents()
        self.table.setRowCount(len(products))
    
        for row, prod in enumerate(products):
            name = prod.get("name", "")
            
            # Безопасно приводим цену к float
            try:
    # Преобразуем строку: заменяем запятые, удаляем пробелы и символы валют
                price_str = str(prod.get("price", "0")).replace(",", ".").strip().replace("₽", "").replace(" ", "")
                price = float(price_str) if price_str else 0.0
            except (TypeError, ValueError):
                price = 0.0
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))
        
        self.table.setSortingEnabled(True)  # Включаем сортировку обратно
        self._filter_rows()

    def _filter_rows(self):
        """Скрываем строки, не соответствующие поисковому запросу."""
        query = self.search.text().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            text = item.text().lower() if item else ""
            self.table.setRowHidden(row, query not in text)

    def _open_new_dialog(self):
        """Открываем диалог создания нового товара."""
        dlg = NewProductDialog(self.api)
        if dlg.exec() == NewProductDialog.DialogCode.Accepted:
            self.reload()

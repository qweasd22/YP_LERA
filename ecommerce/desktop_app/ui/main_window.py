from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.widgets.products import ProductsWidget
from ui.widgets.customers import CustomersWidget
from ui.widgets.deals import DealsWidget

class MainWindow(QMainWindow):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Управление продажами")
        self.resize(1200, 800)

        tabs = QTabWidget()
        tabs.addTab(ProductsWidget(api), "Товары")
        tabs.addTab(CustomersWidget(api), "Покупатели")
        tabs.addTab(DealsWidget(api), "Сделки")
        self.setCentralWidget(tabs)

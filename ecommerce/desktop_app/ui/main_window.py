from PyQt6.QtWidgets import QMainWindow, QTabWidget
from .widgets.products import ProductsWidget
from .widgets.customers import CustomersWidget
from .widgets.deals import DealsWidget

class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Управление продажами")
        self.setGeometry(100, 100, 1200, 800)
        
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(ProductsWidget(api_client), "Товары")
        self.tabs.addTab(CustomersWidget(api_client), "Покупатели")
        self.tabs.addTab(DealsWidget(api_client), "Сделки")
        
        self.setCentralWidget(self.tabs)
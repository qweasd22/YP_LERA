import requests
from typing import List, Dict, Optional

class APIClient:
    def __init__(self, base_url: str = "http://localhost:18800/"):
        self.base_url = base_url
        self.token: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}api-token-auth/",
                data={"username": username, "password": password}
            )
            response.raise_for_status()
            self.token = response.json().get("token")
            return True
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            return False

    def get_products(self) -> List[Dict]:
        return self.get_data("products/")  # Передача endpoint

    def get_customers(self) -> List[Dict]:
        return self.get_data("customers/")  # Передача endpoint

    def get_data(self, endpoint: str) -> List[Dict]:
        headers = {"Authorization": f"Token {self.token}"} if self.token else {}
        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            return []
        
    def get_deals(self) -> List[Dict]:
        try:
            return self.get_data("deals/")
        except Exception as e:
            print(f"Ошибка получения сделок: {e}")
            return []
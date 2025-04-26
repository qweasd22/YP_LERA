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

    def _get(self, endpoint: str) -> List[Dict]:
        headers = {"Authorization": f"Token {self.token}"} if self.token else {}
        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def get_products(self) -> List[Dict]:
        return self._get("api/products/")

    def get_customers(self) -> List[Dict]:
        return self._get("api/customers/")

    def get_deals(self) -> List[Dict]:
        return self._get("api/deals/")

    def create_deal(self, data: Dict) -> bool:
        headers = {"Authorization": f"Token {self.token}"}
        try:
            response = requests.post(
                f"{self.base_url}api/deals/",
                json=data,
                headers=headers
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        
    def create_customer(self, name: str, address: str, phone: str, contact_person: str) -> bool:
        """Создание нового покупателя"""
        data = {
            "name": name,
            "address": address,
            "phone": phone,
            "contact_person": contact_person
        }
        headers = {"Authorization": f"Token {self.token}"}
        try:
            response = requests.post(
                f"{self.base_url}api/customers/",
                json=data,
                headers=headers
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
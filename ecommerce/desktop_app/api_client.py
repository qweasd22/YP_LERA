import requests
from typing import List, Dict, Optional

class APIClient:
    def __init__(self, base_url: str = "http://localhost:18800/"):
        self.base_url = base_url.rstrip("/") + "/"
        self.token: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        try:
            resp = requests.post(
                f"{self.base_url}api-token-auth/",
                data={"username": username, "password": password},
                timeout=5
            )
            resp.raise_for_status()
            self.token = resp.json().get("token")
            return True
        except Exception as e:
            print("Login error:", e)
            return False

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Token {self.token}"} if self.token else {}

    def _get(self, endpoint: str) -> List[Dict]:
        try:
            resp = requests.get(f"{self.base_url}api/{endpoint}", headers=self._headers(), timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"GET {endpoint} error:", e)
            return []

    def _post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        try:
            resp = requests.post(f"{self.base_url}api/{endpoint}", json=data, headers=self._headers(), timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"POST {endpoint} error:", e)
            return None

    def _put(self, endpoint: str, obj_id: int, data: Dict) -> bool:
        try:
            resp = requests.put(f"{self.base_url}api/{endpoint}{obj_id}/", json=data, headers=self._headers(), timeout=5)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"PUT {endpoint} error:", e)
            return False

    def _delete(self, endpoint: str, obj_id: int) -> bool:
        try:
            resp = requests.delete(f"{self.base_url}api/{endpoint}{obj_id}/", headers=self._headers(), timeout=5)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"DELETE {endpoint} error:", e)
            return False

    # Products
    def get_products(self):        return self._get("products/")
    def create_product(self, d):   return self._post("products/", d)
    def update_product(self, pk, d): return self._put("products/", pk, d)
    def delete_product(self, pk):  return self._delete("products/", pk)

    # Customers
    def get_customers(self):        return self._get("customers/")
    def create_customer(self, d):   return self._post("customers/", d)
    def update_customer(self, pk, d): return self._put("customers/", pk, d)
    def delete_customer(self, pk):  return self._delete("customers/", pk)

    # Deals
    def get_deals(self):            return self._get("deals/")
    def create_deal(self, data):
        url = f"{self.base_url}deals/new/"
        headers = {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                print("Сделка создана успешно")
                return True
            else:
                print(f"Ошибка при создании сделки: {response.status_code} {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return False
    def update_deal(self, pk, d):   return self._put("deals/", pk, d)
    def delete_deal(self, pk):      return self._delete("deals/", pk)
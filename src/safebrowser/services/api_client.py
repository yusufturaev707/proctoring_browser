"""
API Client - Server bilan aloqa qilish uchun
"""
import requests
from typing import Optional, Dict, Any

# Base URL (config'dan o'qilishi kerak)
BASE_URL = 'http://localhost:8000/api/v1'


class APIClient:
    """
    REST API client - server bilan aloqa
    """

    def __init__(self, base_url: str = None, timeout: int = 15):
        self.base_url = base_url or BASE_URL
        self.timeout = timeout

    def get(self, endpoint: str, params: dict = None) -> Dict[str, Any]:
        """GET request"""
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            return {"status": False, "message": "Server javob bermadi (timeout)"}
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Ulanish xatoligi: {e}"}

    def post(self, endpoint: str, data: dict = None, json: dict = None) -> Dict[str, Any]:
        """POST request"""
        try:
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                data=data,
                json=json,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            return {"status": False, "message": "Server javob bermadi (timeout)"}
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Ulanish xatoligi: {e}"}

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Response'ni qayta ishlash"""
        if response.status_code in [400, 404, 500, 502]:
            return {
                "status": False,
                "message": f"Server xatoligi: {response.status_code}"
            }
        try:
            return response.json()
        except ValueError:
            return {"status": False, "message": "JSON parse xatoligi"}

    def load_tests(self) -> Dict[str, Any]:
        """Testlar ro'yxatini yuklash"""
        result = self.get("load-tests/")
        if result.get("status") == "success":
            return {
                "status": True,
                "result": result.get("data", []),
                "message": "Muvaffaqiyatli yuklandi"
            }
        return {
            "status": False,
            "result": [],
            "message": result.get("message", "Xatolik")
        }

    def verify_face(self, embedding: list) -> Dict[str, Any]:
        """Yuzni server orqali tekshirish"""
        return self.post(
            "users/face_identification/",
            json={"embedding": str(embedding)}
        )

# utils/api_helper.py

BASE_URL = "https://fakestoreapi.com"

def get_full_url(endpoint: str) -> str:
    """
    Helper untuk menggabungkan base URL dengan endpoint.
    """
    return f"{BASE_URL}/{endpoint.strip('/')}"

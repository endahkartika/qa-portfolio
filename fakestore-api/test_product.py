import requests
import pytest
import uuid

from api_helper import get_full_url  # import helper

login_payload = {
    "username": "johnd",
    "password": "m38rmF$"
}

@pytest.fixture(scope="session")
def get_token():
    response = requests.post(get_full_url("auth/login"), json=login_payload)
    assert response.status_code == 200, "Login failed"
    token = response.json().get("token")
    assert token is not None, "Token not found in response"
    return token


def test_create_product(get_token):
    product_payload = {
        "id": str(uuid.uuid4()),
        "title": "Zara",
        "price": "109.95",
        "description": "Your perfect pack for everyday use and walks in the forest.",
        "category": "men's clothing",
        "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"
    }

    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(get_full_url("products"), json=product_payload, headers=headers)
    assert response.status_code in [200, 201]
    
    response_json = response.json()
    assert response_json["title"] == product_payload["title"]
    assert response_json["category"] == product_payload["category"]
    assert float(response_json["price"]) == float(product_payload["price"])

    print("Produk berhasil dibuat (dummy):", response_json)


def test_get_single_product():
    headers = {
        "Accept": "application/json"
    }

    product_id = 1
    response = requests.get(get_full_url(f"products/{product_id}"), headers=headers)
    assert response.status_code == 200

    product = response.json()
    assert product["id"] == product_id
    assert "title" in product
    assert "price" in product

    print("Produk ditemukan:", product["title"])


def test_update_product():
    product_id = 21

    update_payload = {
        "id": product_id,
        "title": "Zara",
        "price": "109",
        "description": "Your perfect pack for everyday use and walks in the forest.",
        "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
        "category": "men's clothing"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.put(get_full_url(f"products/{product_id}"), json=update_payload, headers=headers)
    assert response.status_code in [200, 201]

    updated_product = response.json()
    assert updated_product["id"] == product_id
    assert updated_product["title"] == update_payload["title"]
    assert float(updated_product["price"]) == float(update_payload["price"])
    assert updated_product["category"] == update_payload["category"]

    print("Produk berhasil diperbarui:", updated_product["title"])

def test_create_cart():
    cart_payload = {
        "id": str(uuid.uuid4()),
        "userId": "813817313",
        "products": [
            {
                "id": "81381731300",
                "title": "Bajuku",
                "price": "909090",
                "description": "Bajuku",
                "category": "Bajuku",
                "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"
            },
            {
                "id": "999",
                "title": "Celanaku",
                "price": "200000",
                "description": "Celana nyaman dipakai",
                "category": "pakaian",
                "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(get_full_url("carts"), json=cart_payload, headers=headers)

    assert response.status_code in [200, 201], f"Gagal membuat cart: {response.status_code}"
    
    response_json = response.json()

    assert response_json.get("userId") == cart_payload["userId"]
    assert isinstance(response_json.get("products"), list), "Produk harus berupa list"
    assert len(response_json["products"]) == len(cart_payload["products"])

    print("Cart berhasil dibuat:", response_json)

def test_create_user():
    user_payload = {
        "id": "21212121",
        "username": "Zura",
        "email": "zura233@yopmail.com",
        "password": "password"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(get_full_url("users"), json=user_payload, headers=headers)

    assert response.status_code in [200, 201], f"Gagal membuat user: {response.status_code}"
    
    user_data = response.json()


    assert "id" in user_data, "Response tidak mengandung ID user"

    print("User berhasil dibuat (dummy):", user_data)

def test_update_user():
    user_id = 1  # user ID yang akan di-update

    update_payload = {
        "id": str(user_id),
        "username": "johnd",
        "email": "john@gmail.com",
        "password": "m38rmF$"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.put(get_full_url(f"users/{user_id}"), json=update_payload, headers=headers)

    assert response.status_code in [200, 201], f"Gagal update user: {response.status_code}"
    
    updated_user = response.json()

    assert updated_user.get("id") == user_id or str(updated_user.get("id")) == str(user_id), "ID user tidak sesuai"

    print("User berhasil diupdate (dummy):", updated_user)



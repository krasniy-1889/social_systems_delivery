from cuid import cuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

CUID = cuid()
BEARER_TOKEN = ""


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Social Systems"}


def test_register_user():
    json = {
        "username": CUID,
        "password": CUID,
    }
    response = client.post("/auth/register", json=json)
    assert response.status_code == 201
    assert response.json()["username"] == CUID


def test_login_user():
    global BEARER_TOKEN
    data = {
        "grant_type": "password",
        "username": CUID,
        "password": CUID,
        "scope": "",
        "client_id": "",
        "client_secret": "string",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = client.post(
        "/auth/token",
        data=data,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    BEARER_TOKEN = response.json()["access_token"]


def test_auth_me():
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == CUID


def test_add_new_data():
    """
    Тесты нужно разбивать на мелкие части
    но т.к. проект тестовый, и времени мало, пишу все в одну кучу. Так делать на проде не нужно ;)
    """
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }
    json = {"name": CUID}
    response = client.post("/add_restaurant", headers=headers, json=json)
    restaurant_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json()["name"] == CUID
    json = {
        "name": CUID,
        "price": 10,
        "restaurant_id": restaurant_id,
    }
    response = client.post("/add_dish", headers=headers, json=json)
    dish_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json()["name"] == CUID
    json = {
        "dish_id": dish_id,
        "quantity": 10,
    }
    response = client.post("/add_to_cart", headers=headers, json=json)
    dish_id = response.json()["id"]
    assert response.status_code == 201

    response = client.post("/show_cart", headers=headers)
    assert response.status_code == 200

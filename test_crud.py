import pytest
import requests
from shortuuid import uuid

url = "http://127.0.0.1:5000"
session = requests.Session()


def test_login():
    user_payload = create_payload()
    create_user_response = create_user(user_payload)
    assert create_user_response.status_code == 200

    login_response = login_user(user_payload["username"], user_payload["password"])
    assert login_response.status_code == 200
    session.cookies.clear()


def test_create_user():
    user_payload = create_payload()
    create_user_response = create_user(user_payload)

    assert create_user_response.status_code == 200
    create_user_data = create_user_response.json()
    assert "user_id" in create_user_data
    user_id = create_user_data["user_id"]

    login_user(user_payload["username"], user_payload["password"])
    read_user_response = read_user(user_id)
    assert read_user_response.status_code == 200
    read_user_data = read_user_response.json()
    assert "username" in read_user_data
    assert read_user_data["username"] == user_payload["username"]
    session.cookies.clear()


def create_payload():
    return {
        "username": f"test_user_{uuid()}",
        "password": uuid()
    }


def create_user(payload):
    return requests.post(f"{url}/user", json=payload)


def login_user(username, password):
    session.cookies.clear()
    payload = {"username": username, "password": password}
    return session.post(f"{url}/login", json=payload)


def logout_user():
    return requests.get(f"{url}/logout")


def read_user(user_id):
    return session.get(f"{url}/user/{user_id}")


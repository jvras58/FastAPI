import os

import jwt

from app.utils.security import create_access_token
from app.utils.settings import get_settings

os.environ.setdefault(
    "SECURITY_API_SECRET_KEY",
    "test_secret_key_with_32_bytes_minimum_1234",
)
get_settings.cache_clear()


def test_jwt_token():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithms=[get_settings().SECURITY_ALGORITHM],
    )

    assert decoded["test"] == data["test"]
    assert decoded["exp"]


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clear_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"


def test_execute_user_login_valid_credentials(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clear_password},
    )
    token = response.json()
    assert response.status_code == 200
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"


def test_execute_user_login_invalid_credentials(client, user):
    response = client.post(
        "/auth/token",
        data={"username": "invalid_login", "password": user.clear_password},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}

    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": "invalid_password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_current_user_invalid_token(client, user):
    token = "invalid_token"

    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_user_with_empty_username(client, user):
    token_data = {"sub": ""}
    token = create_access_token(data=token_data)

    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

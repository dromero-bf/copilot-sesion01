import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_success():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_login_wrong_password():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post(
        "/auth/login",
        json={"username": "nobody", "password": "pass"},
    )
    assert response.status_code == 401


def test_refresh_token():
    # First obtain tokens
    login_resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    # Use the refresh token
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_with_invalid_token():
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "not.a.valid.token"},
    )
    assert response.status_code == 401


def test_refresh_with_access_token_rejected():
    """An access token must not be accepted as a refresh token."""
    login_resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    access_token = login_resp.json()["access_token"]

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": access_token},
    )
    assert response.status_code == 401


def test_protected_endpoint_with_valid_token():
    login_resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    access_token = login_resp.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_protected_endpoint_without_token():
    response = client.get("/users/me")
    assert response.status_code == 403


def test_protected_endpoint_with_refresh_token_rejected():
    """A refresh token must not grant access to protected resources."""
    login_resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert response.status_code == 401

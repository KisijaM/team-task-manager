from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

def test_register_user_success():
    user_data = {
        "username": "TestUser1",
        "password": "Password1",
        "email": "testuser1@example.com",
        "phone_number": "+123456789",
        "address": "Test Street 1"
    }

    with patch(
        "app.services.user_service.UserService.register_user",
        new_callable=AsyncMock
    ) as mock_register:
        mock_register.return_value = {
            "id": "1",
            "username": "TestUser1",
            "email": "testuser1@example.com",
            "phone_number": "+123456789",
            "address": "Test Street 1"
        }

        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["username"] == "TestUser1"


def test_login_user_success():
    login_data = {
        "username": "TestUser1",
        "password": "Password1"
    }

    with patch(
        "app.services.user_service.UserService.login_user",
        new_callable=AsyncMock
    ) as mock_login:
        mock_login.return_value = {
            "user": {"id": "1", "username": "TestUser1"},
            "access_token": "fake-token"
        }

        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()


def test_delete_user_success():
    user_id = "1"

    with patch(
        "app.services.user_service.UserService.delete_user",
        new_callable=AsyncMock
    ) as mock_delete, \
         patch("app.routes.auth.verify_token", return_value="TestUser1"):

        mock_delete.return_value = 1

        headers = {"Authorization": "Bearer faketoken"}
        response = client.delete(f"/auth/delete/{user_id}", headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

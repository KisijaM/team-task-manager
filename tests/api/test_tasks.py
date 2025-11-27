from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)


def test_get_tasks():
    with patch(
        "app.services.task_service.TaskService.get_all_tasks",
        new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = [
            {"id": "1", "title": "Test Task", "created_by": "TestUser1"}
        ]

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.get("/tasks/", headers=headers)

    assert response.status_code == 200
    data = response.json()[0]
    assert data["id"] == "1"
    assert data["title"] == "Test Task"
    assert data["created_by"] == "TestUser1"


def test_create_task():
    task_data = {"title": "New Task", "created_by": "TestUser1"}

    with patch(
        "app.services.task_service.TaskService.create_task_from_dto",
        new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = {
            "id": "1",
            "title": "New Task",
            "created_by": "TestUser1"
        }

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.post("/tasks/", headers=headers, json=task_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"
    assert data["title"] == "New Task"
    assert data["created_by"] == "TestUser1"


def test_delete_task():
    with patch(
        "app.services.task_service.TaskService.delete_task",
        new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value = True

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.delete("/tasks/1", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


def test_get_tasks_failure():
    """Service baca exception → očekujemo 500"""
    with patch(
        "app.services.task_service.TaskService.get_all_tasks",
        new_callable=AsyncMock
    ) as mock_get:
        mock_get.side_effect = Exception("Database error")

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.get("/tasks/", headers=headers)
            assert response.status_code == 500
            assert "Database error" in response.text


def test_get_tasks_unauthorized():
    """verify_token vrati None → 401 unauthorized"""
    headers = {"Authorization": "Bearer faketoken"}

    with patch("app.routes.tasks.verify_token", return_value=None):
        response = client.get("/tasks/", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_delete_task_not_found():
    """delete_task vrati False → 404 not found"""
    with patch(
        "app.services.task_service.TaskService.delete_task",
        new_callable=AsyncMock
    ) as mock_delete, \
         patch("app.routes.tasks.verify_token", return_value="TestUser1"):

        mock_delete.return_value = False

        headers = {"Authorization": "Bearer faketoken"}
        response = client.delete("/tasks/123", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

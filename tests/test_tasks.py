# tests/test_tasks.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_tasks():
    with patch("app.services.task_service.TaskService.get_all_tasks", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [
            {"id": "1", "title": "Test Task", "created_by": "TestUser1"}
        ]

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.get("/tasks/", headers=headers)
            assert response.status_code == 200
            assert response.json()[0]["title"] == "Test Task"

@pytest.mark.asyncio
async def test_create_task():
    task_data = {"title": "New Task", "created_by": "TestUser1"}

    with patch("app.services.task_service.TaskService.create_task_from_dto", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {"id": "1", "title": "New Task", "created_by": "TestUser1"}

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.post("/tasks/", headers=headers, json=task_data)
            assert response.status_code == 200
            assert response.json()["created_by"] == "TestUser1"

@pytest.mark.asyncio
async def test_delete_task():
    with patch("app.services.task_service.TaskService.delete_task", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = True

        headers = {"Authorization": "Bearer faketoken"}
        with patch("app.routes.tasks.verify_token", return_value="TestUser1"):
            response = client.delete("/tasks/1", headers=headers)
            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"

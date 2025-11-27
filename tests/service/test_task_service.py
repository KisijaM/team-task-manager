import pytest
from unittest.mock import AsyncMock, patch
from app.services.task_service import TaskService, get_task_service
from app.dto.task_create_dto import TaskCreateDTO
from app.dto.task_dto import TaskDTO


@pytest.mark.asyncio
async def test_get_all_tasks_happy():
    mock_repo = AsyncMock()
    mock_repo.find_all.return_value = [
        {"_id": 1, "title": "Test Task", "created_by": "User1"}
    ]

    service = TaskService(repository=mock_repo)

    tasks = await service.get_all_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert isinstance(task, TaskDTO)
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.created_by == "User1"


@pytest.mark.asyncio
async def test_get_all_tasks_empty():
    mock_repo = AsyncMock()
    mock_repo.find_all.return_value = []

    service = TaskService(repository=mock_repo)

    tasks = await service.get_all_tasks()
    assert tasks == []


@pytest.mark.asyncio
async def test_create_task_from_dto_happy():
    mock_repo = AsyncMock()
    mock_repo.insert_one.return_value = 1
    mock_repo.find_by_id.return_value = {"_id": 1, "title": "New Task", "created_by": "User1"}

    service = TaskService(repository=mock_repo)
    task_create = TaskCreateDTO(title="New Task", created_by="User1")

    task = await service.create_task_from_dto(task_create)
    assert isinstance(task, TaskDTO)
    assert task.id == "1"
    assert task.title == "New Task"
    assert task.created_by == "User1"


@pytest.mark.asyncio
async def test_create_task_from_dto_repo_fail():
    mock_repo = AsyncMock()
    mock_repo.insert_one.side_effect = Exception("DB error")

    service = TaskService(repository=mock_repo)
    task_create = TaskCreateDTO(title="Fail Task", created_by="User1")

    with pytest.raises(Exception) as exc:
        await service.create_task_from_dto(task_create)
    assert "DB error" in str(exc.value)


@pytest.mark.asyncio
async def test_delete_task_happy():
    mock_repo = AsyncMock()
    mock_repo.delete_by_id.return_value = True

    service = TaskService(repository=mock_repo)
    result = await service.delete_task("1")
    assert result is True


@pytest.mark.asyncio
async def test_delete_task_not_found():
    mock_repo = AsyncMock()
    mock_repo.delete_by_id.return_value = False

    service = TaskService(repository=mock_repo)
    result = await service.delete_task("999")
    assert result is False

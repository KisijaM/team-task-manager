import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId
from app.repositories.task_repository import TaskRepository


# AsyncIterator za simulaciju async for petlje
class AsyncIterator:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self._items):
            raise StopAsyncIteration
        item = self._items[self._index]
        self._index += 1
        return item


@pytest.mark.asyncio
async def test_get_tasks_by_user_id_happy():
    mock_collection = MagicMock()
    mock_collection.find.return_value = AsyncIterator([
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "title": "Task1", "user_id": "user1"},
        {"_id": ObjectId("507f1f77bcf86cd799439012"), "title": "Task2", "user_id": "user1"},
    ])

    repo = TaskRepository()
    repo.collection = mock_collection

    tasks = await repo.get_tasks_by_user_id("user1")
    assert len(tasks) == 2
    assert tasks[0]["_id"] == "507f1f77bcf86cd799439011"
    assert tasks[1]["_id"] == "507f1f77bcf86cd799439012"


@pytest.mark.asyncio
async def test_get_tasks_by_user_id_empty():
    mock_collection = MagicMock()
    mock_collection.find.return_value = AsyncIterator([])

    repo = TaskRepository()
    repo.collection = mock_collection

    tasks = await repo.get_tasks_by_user_id("user999")
    assert tasks == []

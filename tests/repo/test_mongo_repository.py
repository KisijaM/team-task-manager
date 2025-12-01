import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId
from app.repositories.mongo_repository import MongoRepository


@pytest.mark.asyncio
async def test_insert_one():
    mock_collection = AsyncMock()
    mock_collection.insert_one.return_value.inserted_id = ObjectId("507f1f77bcf86cd799439011")

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    inserted_id = await repo.insert_one({"title": "Task1"})
    assert inserted_id == "507f1f77bcf86cd799439011"


@pytest.mark.asyncio
async def test_find_one():
    mock_collection = AsyncMock()
    doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "title": "Task1"}
    mock_collection.find_one.return_value = doc

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.find_one({"title": "Task1"})
    assert result["_id"] == "507f1f77bcf86cd799439011"
    assert result["title"] == "Task1"


@pytest.mark.asyncio
async def test_find_one_not_found():
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.find_one({"title": "Missing"})
    assert result is None


@pytest.mark.asyncio
async def test_find_by_id():
    mock_collection = AsyncMock()
    doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "title": "Task1"}
    mock_collection.find_one.return_value = doc

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.find_by_id("507f1f77bcf86cd799439011")
    assert result["_id"] == "507f1f77bcf86cd799439011"
    assert result["title"] == "Task1"


@pytest.mark.asyncio
async def test_find_by_id_not_found():
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.find_by_id("507f1f77bcf86cd799439099")
    assert result is None


@pytest.mark.asyncio
async def test_delete_by_id_happy():
    mock_collection = AsyncMock()
    mock_collection.delete_one.return_value.deleted_count = 1

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.delete_by_id("507f1f77bcf86cd799439011")
    assert result == 1


@pytest.mark.asyncio
async def test_delete_by_id_not_found():
    mock_collection = AsyncMock()
    mock_collection.delete_one.return_value.deleted_count = 0

    db_client = MagicMock()
    db_client.__getitem__.return_value = mock_collection
    repo = MongoRepository(db_client=db_client, collection_name="tasks")

    result = await repo.delete_by_id("507f1f77bcf86cd799439099")
    assert result == 0


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
async def test_find_all_happy():
    mock_collection = MagicMock()
    mock_collection.find.return_value = AsyncIterator([
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "title": "Task1"},
        {"_id": ObjectId("507f1f77bcf86cd799439012"), "title": "Task2"},
    ])

    repo = MongoRepository(db_client=MagicMock(), collection_name="tasks")
    repo.collection = mock_collection

    results = await repo.find_all()
    assert len(results) == 2
    assert results[0]["_id"] == "507f1f77bcf86cd799439011"
    assert results[1]["_id"] == "507f1f77bcf86cd799439012"


@pytest.mark.asyncio
async def test_find_all_empty():
    mock_collection = MagicMock()
    mock_collection.find.return_value = AsyncIterator([])

    repo = MongoRepository(db_client=MagicMock(), collection_name="tasks")
    repo.collection = mock_collection

    results = await repo.find_all()
    assert results == []

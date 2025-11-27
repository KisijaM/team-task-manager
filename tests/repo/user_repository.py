import pytest
from unittest.mock import AsyncMock
from bson import ObjectId
from app.repositories.user_repository import UserRepository

@pytest.mark.asyncio
async def test_get_user_by_username_happy():
    mock_repo = AsyncMock()
    doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "username": "TestUser"}
    mock_repo.find_one.return_value = doc

    repo = UserRepository()
    repo.find_one = mock_repo.find_one 

    result = await repo.get_user_by_username("TestUser")
    assert result["_id"] == "507f1f77bcf86cd799439011"
    assert result["username"] == "TestUser"


@pytest.mark.asyncio
async def test_get_user_by_username_not_found():
    mock_repo = AsyncMock()
    mock_repo.find_one.return_value = None

    repo = UserRepository()
    repo.find_one = mock_repo.find_one

    result = await repo.get_user_by_username("MissingUser")
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_email_happy():
    mock_repo = AsyncMock()
    doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "email": "test@example.com"}
    mock_repo.find_one.return_value = doc

    repo = UserRepository()
    repo.find_one = mock_repo.find_one

    result = await repo.get_user_by_email("test@example.com")
    assert result["_id"] == "507f1f77bcf86cd799439011"
    assert result["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email_not_found():
    mock_repo = AsyncMock()
    mock_repo.find_one.return_value = None

    repo = UserRepository()
    repo.find_one = mock_repo.find_one

    result = await repo.get_user_by_email("missing@example.com")
    assert result is None


@pytest.mark.asyncio
async def test_delete_user_by_id_happy():
    mock_repo = AsyncMock()
    mock_repo.delete_by_id.return_value = 1

    repo = UserRepository()
    repo.delete_by_id = mock_repo.delete_by_id

    result = await repo.delete_user_by_id("507f1f77bcf86cd799439011")
    assert result == 1


@pytest.mark.asyncio
async def test_delete_user_by_id_not_found():
    mock_repo = AsyncMock()
    mock_repo.delete_by_id.return_value = 0

    repo = UserRepository()
    repo.delete_by_id = mock_repo.delete_by_id

    result = await repo.delete_user_by_id("507f1f77bcf86cd799439099")
    assert result == 0

import pytest
from unittest.mock import AsyncMock
from app.services.user_service import UserService
from app.dto.user_dto import UserRegisterDTO


@pytest.mark.asyncio
async def test_register_user_happy():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = None
    mock_repo.get_user_by_email.return_value = None
    mock_repo.insert_one.return_value = 1
    mock_repo.find_by_id.return_value = {
        "_id": 1,
        "username": "TestUser",
        "email": "test@example.com",
        "phone_number": "+123456789",
        "address": "Test Street",
        "password": "hashedpassword"
    }

    service = UserService(repository=mock_repo)
    user_dto = UserRegisterDTO(
        username="TestUser",
        password="Password1",
        email="test@example.com",
        phone_number="+123456789",
        address="Test Street"
    )

    result = await service.register_user(user_dto)
    assert result.username == "TestUser"
    assert result.email == "test@example.com"
    assert result.id == "1"


@pytest.mark.asyncio
async def test_register_user_username_exists():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = {"_id": 1, "username": "TestUser"}

    service = UserService(repository=mock_repo)
    user_dto = UserRegisterDTO(
        username="TestUser",
        password="Password1",
        email="test@example.com",
        phone_number="+123456789",
        address="Test Street"
    )

    result = await service.register_user(user_dto)
    assert result["error"] == "username_exists"


@pytest.mark.asyncio
async def test_register_user_email_exists():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = None
    mock_repo.get_user_by_email.return_value = {"_id": 2, "email": "test@example.com"}

    service = UserService(repository=mock_repo)
    user_dto = UserRegisterDTO(
        username="NewUser",
        password="Password1",
        email="test@example.com",
        phone_number="+123456789",
        address="Test Street"
    )

    result = await service.register_user(user_dto)
    assert result["error"] == "email_exists"


@pytest.mark.asyncio
async def test_login_user_happy():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = {
        "_id": 1,
        "username": "TestUser",
        "password": "hashedpassword",
        "email": "test@example.com",
        "phone_number": "+123456789",
        "address": "Test Street"
    }

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.services.user_service.verify_password", lambda pw, hashed: True)
        m.setattr("app.services.user_service.create_access_token", lambda data: "fake-token")

        service = UserService(repository=mock_repo)
        result = await service.login_user("TestUser", "Password1")

    assert result["user"].username == "TestUser"
    assert result["access_token"] == "fake-token"


@pytest.mark.asyncio
async def test_login_user_invalid_password():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = {
        "_id": 1,
        "username": "TestUser",
        "password": "hashedpassword",
        "email": "test@example.com",
        "phone_number": "+123456789",
        "address": "Test Street"
    }

    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.services.user_service.verify_password", lambda pw, hashed: False)

        service = UserService(repository=mock_repo)
        result = await service.login_user("TestUser", "WrongPassword")

    assert result is None


@pytest.mark.asyncio
async def test_delete_user_happy():
    mock_repo = AsyncMock()
    mock_repo.delete_user_by_id.return_value = 1

    service = UserService(repository=mock_repo)
    result = await service.delete_user("1")
    assert result == 1


@pytest.mark.asyncio
async def test_delete_user_not_found():
    mock_repo = AsyncMock()
    mock_repo.delete_user_by_id.return_value = 0

    service = UserService(repository=mock_repo)
    result = await service.delete_user("999")
    assert result == 0

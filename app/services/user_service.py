from typing import Optional
from app.repositories.user_repository import UserRepository
from app.dto.user_dto import UserRegisterDTO, UserLoginDTO, UserDTO
from app.security.security import hash_password, verify_password, create_access_token

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user_dto: UserRegisterDTO):
        user_data = user_dto.model_dump()
        user_data["password"] = hash_password(user_data["password"])

        existing_user = await self.repository.get_user_by_username(user_data["username"])
        if existing_user:
            return {"error": "username_exists"}

        if "email" in user_data:
            existing_email = await self.repository.get_user_by_email(user_data["email"])
            if existing_email:
                return {"error": "email_exists"}

        user_id = await self.repository.insert_one(user_data)
        created_user = await self.repository.find_by_id(user_id)

        if not created_user:
            return {"error": "creation_failed"}

        created_user["id"] = str(created_user.pop("_id"))
        return UserDTO(**created_user)

    async def login_user(self, username: str, password: str) -> Optional[dict]:
        user = await self.repository.get_user_by_username(username)
        if not user or not verify_password(password, user["password"]):
            return None

        user["id"] = str(user["_id"])
        access_token = create_access_token({"sub": user["username"]})
        return {"user": UserDTO(**user), "access_token": access_token}

    async def delete_user(self, user_id: str) -> int:
        return await self.repository.delete_user_by_id(user_id)


def get_user_service() -> UserService:
    repository = UserRepository()
    return UserService(repository)

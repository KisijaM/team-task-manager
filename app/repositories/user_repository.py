from app.repositories.mongo_repository import MongoRepository
from app.db import db  

class UserRepository(MongoRepository):
    def __init__(self):
        super().__init__(db, "users")

    async def get_user_by_username(self, username: str) -> dict | None:
        return await self.find_one({"username": username})

    async def get_user_by_email(self, email: str) -> dict | None:
        return await self.find_one({"email": email})

    async def delete_user_by_id(self, user_id: str) -> int:
        return await self.delete_by_id(user_id)

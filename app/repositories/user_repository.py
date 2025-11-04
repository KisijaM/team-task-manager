from motor.motor_asyncio import AsyncIOMotorCollection
from app.db import db
from bson import ObjectId

class UserRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["users"]

    async def create_user(
        self,
        username: str,
        password: str,
        email: str,
        phone_number: str | None = None,
        address: str | None = None
    ) -> dict | str:
        # Check if the username already exists
        existing_username = await self.collection.find_one({"username": username})
        if existing_username:
            return "username_exists"

        # Check if the email already exists
        existing_email = await self.collection.find_one({"email": email})
        if existing_email:
            return "email_exists"

        # Insert new user
        result = await self.collection.insert_one({
            "username": username,
            "password": password,
            "email": email,
            "phone_number": phone_number,
            "address": address
        })

        return {
            "id": str(result.inserted_id),
            "username": username,
            "email": email,
            "phone_number": phone_number,
            "address": address
        }

    async def get_user_by_username(self, username: str) -> dict | None:
        return await self.collection.find_one({"username": username})

    async def delete_user_by_username(self, username: str) -> int:
        result = await self.collection.delete_one({"username": username})
        return result.deleted_count

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.core.task import Task
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

class TaskRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db["tasks"]

    async def create(self, task_data: dict) -> dict:
        result = await self.collection.insert_one(task_data)
        task_data["_id"] = result.inserted_id  
        return task_data

    async def get_all(self):
        tasks = []
        cursor = self.collection.find()
        async for document in cursor:
            tasks.append(document)
        return tasks

    async def delete(self, task_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count

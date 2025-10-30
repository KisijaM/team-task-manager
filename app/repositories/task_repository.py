from bson import ObjectId
from app.core.task import Task
from app.db import db  

class TaskRepository:
    def __init__(self):
        self.collection = db["tasks"]  

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

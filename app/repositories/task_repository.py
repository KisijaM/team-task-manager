from app.db import db  
from app.repositories.mongo_repository import MongoRepository

class TaskRepository(MongoRepository):
    def __init__(self):
        super().__init__(db, "tasks")

    async def get_tasks_by_user_id(self, user_id: str) -> list[dict]:
        cursor = self.collection.find({"user_id": user_id})
        tasks = []
        async for task in cursor:
            task["_id"] = str(task["_id"])
            tasks.append(task)
        return tasks

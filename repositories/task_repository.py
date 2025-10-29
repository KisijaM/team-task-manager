from typing import List
from bson import ObjectId
from core.task import Task
from db import tasks_collection

class TaskRepository:
    async def get_all(self) -> List[Task]:
        tasks = []
        async for task in tasks_collection.find():
            task["_id"] = str(task["_id"])
            tasks.append(Task(**task))
        return tasks

    async def create(self, task: Task) -> Task:
        await tasks_collection.insert_one(task.dict())
        return task

    async def delete(self, task_id: str) -> bool:
        result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count == 1

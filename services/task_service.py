from typing import List
from core.task import Task
from db import tasks_collection

class TaskService:
    async def get_all_tasks(self) -> List[Task]:
        tasks = []
        async for task in tasks_collection.find():
            task["_id"] = str(task["_id"])
            tasks.append(Task(**task))
        return tasks

    async def create_task(self, task: Task) -> Task:
        await tasks_collection.insert_one(task.dict())
        return task

    async def delete_all_tasks(self) -> int:
        result = await tasks_collection.delete_many({})
        return result.deleted_count

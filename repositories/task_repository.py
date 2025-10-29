from typing import List
from db import tasks_collection
from core.task import Task

class TaskRepository:
    def __init__(self, collection=tasks_collection):
        self.collection = collection

    async def get_all(self) -> List[Task]:
        tasks = []
        async for task in self.collection.find({}):
            tasks.append(Task(**task))
        return tasks

    async def create_task(self, task: Task) -> Task:
        await self.collection.insert_one(task.dict())
        return task

    async def delete(self, task_id: str):
        result = await self.collection.delete_one({"id": task_id})
        return result

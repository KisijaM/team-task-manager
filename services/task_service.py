from typing import List
from core.task import Task
from repositories.task_repository import TaskRepository
from dto.task_dto import TaskDTO
from services.task_mapper import convert_task_to_dto

class TaskService:
    def __init__(self, repository: TaskRepository = None):
        self.repository = repository or TaskRepository()

    async def get_all_tasks(self) -> List[TaskDTO]:
        tasks = await self.repository.get_all()
        return [convert_task_to_dto(task) for task in tasks]

    async def create_task(self, task: Task) -> TaskDTO:
        created_task = await self.repository.create(task)
        return convert_task_to_dto(created_task)

    async def delete_task(self, task_id: str) -> bool:
        return await self.repository.delete(task_id)

# Dependency injection
def get_task_service() -> TaskService:
    return TaskService()

from repositories.task_repository import TaskRepository
from dto.task_create_dto import TaskCreateDTO
from dto.task_dto import TaskDTO
from core.task import Task

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> list[TaskDTO]:
        tasks = await self.repository.get_all()
        return [TaskDTO.from_task(task) for task in tasks]

    async def create_task_from_dto(self, task_create: TaskCreateDTO) -> TaskDTO:
        task = Task.create(task_create.title, task_create.created_by)
        await self.repository.create_task(task)
        return TaskDTO.from_task(task)

    async def delete_task(self, task_id: str) -> bool:
        result = await self.repository.delete(task_id)
        return result.deleted_count > 0

# Dependency injection
def get_task_service() -> TaskService:
    repository = TaskRepository()
    return TaskService(repository)

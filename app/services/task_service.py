from app.repositories.task_repository import TaskRepository
from app.dto.task_create_dto import TaskCreateDTO
from app.dto.task_dto import TaskDTO

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self):
        tasks = await self.repository.find_all()  
        return [
            TaskDTO(
                id=str(task["_id"]),
                title=task["title"],
                created_by=task.get("created_by", "unknown")
            )
            for task in tasks
        ]

    async def create_task_from_dto(self, task_create: TaskCreateDTO):
        task_dict = task_create.dict()
        created_task = await self.repository.insert_one(task_dict)
        
        doc = await self.repository.find_by_id(created_task)
        return TaskDTO(
            id=str(doc["_id"]),
            title=doc["title"],
            created_by=doc.get("created_by", "unknown")
        )

    async def delete_task(self, task_id: str):
        return await self.repository.delete_by_id(task_id)


# Dependency
from fastapi import Depends

def get_task_service() -> TaskService:
    repository = TaskRepository()
    return TaskService(repository)

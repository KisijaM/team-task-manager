from fastapi import APIRouter, Depends
from typing import List
from app.services.task_service import TaskService, get_task_service
from app.dto.task_create_dto import TaskCreateDTO
from app.dto.task_dto import TaskDTO  

router = APIRouter()

@router.get("/tasks", response_model=List[TaskDTO])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all_tasks()

@router.post("/tasks", response_model=TaskDTO)
async def create_task(task_create: TaskCreateDTO, service: TaskService = Depends(get_task_service)):
    return await service.create_task_from_dto(task_create)

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    success = await service.delete_task(task_id)
    if not success:
        return {"message": "Task not found"}
    return {"message": "Task deleted successfully"}

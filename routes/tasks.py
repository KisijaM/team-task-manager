from fastapi import APIRouter, Depends, HTTPException
from typing import List
from core.task import Task
from dto.task_create_dto import TaskCreate
from services.task_service import TaskService

router = APIRouter()

# Dependency injection
def get_task_service():
    return TaskService()

@router.get("/tasks", response_model=List[Task])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    try:
        return await service.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks", response_model=Task)
async def create_task(task_create: TaskCreate, service: TaskService = Depends(get_task_service)):
    task = Task(**task_create.dict())
    try:
        return await service.create_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks", response_model=dict)
async def delete_all_tasks(service: TaskService = Depends(get_task_service)):
    deleted_count = await service.delete_all_tasks()
    return {"message": f"{deleted_count} tasks deleted successfully"}

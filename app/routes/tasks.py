from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.task_service import TaskService, get_task_service
from app.dto.task_create_dto import TaskCreateDTO
from app.dto.task_dto import TaskDTO  

router = APIRouter()

@router.get("/tasks", response_model=List[TaskDTO])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    try:
        return await service.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/tasks", response_model=TaskDTO)
async def create_task(task_create: TaskCreateDTO, service: TaskService = Depends(get_task_service)):
    try:
        return await service.create_task_from_dto(task_create)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

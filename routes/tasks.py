from fastapi import APIRouter, Depends, HTTPException
from typing import List
from dto.task_create_dto import TaskCreateDTO
from dto.task_dto import TaskDTO
from services.task_service import TaskService, get_task_service
from services.task_mapper import convert_from_dto_to_task

router = APIRouter()

@router.get("/tasks", response_model=List[TaskDTO])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    try:
        return await service.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", response_model=TaskDTO)
async def create_task(task_create: TaskCreateDTO, service: TaskService = Depends(get_task_service)):
    try:
        task = convert_from_dto_to_task(task_create)
        return await service.create_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    try:
        deleted = await service.delete_task(task_id)
        if deleted:
            return {"message": "Task deleted successfully"}
        else:
            return {"message": "Task not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

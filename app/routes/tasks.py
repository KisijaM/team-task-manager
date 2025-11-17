from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from app.services.task_service import TaskService, get_task_service
from app.dto.task_create_dto import TaskCreateDTO
from app.dto.task_dto import TaskDTO
from app.security.security import verify_token

router = APIRouter()
bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username


@router.get("/", response_model=List[TaskDTO], tags=["tasks"])
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    username: str = Depends(get_current_user)
):
    """
    Get all tasks. Requires a valid JWT token.
    """
    return await service.get_all_tasks()


@router.post("/", response_model=TaskDTO, tags=["tasks"])
async def create_task(
    task_create: TaskCreateDTO,
    service: TaskService = Depends(get_task_service),
    username: str = Depends(get_current_user)  
):
    """
    Create a new task. If 'created_by' is not provided in the request, it defaults to the JWT username.
    """
    if not task_create.created_by:
        task_create.created_by = username

    return await service.create_task_from_dto(task_create)


@router.delete("/{task_id}", response_model=dict, tags=["tasks"])
async def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    username: str = Depends(get_current_user)
):
    """
    Delete a task by ID. Requires a valid JWT token.
    """
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

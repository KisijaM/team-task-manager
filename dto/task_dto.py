from pydantic import BaseModel
from datetime import datetime
from core.task import Task

class TaskDTO(BaseModel):
    id: str
    title: str
    created_by: str
    created_at: datetime

    @staticmethod
    def from_task(task: Task) -> "TaskDTO":
        return TaskDTO(
            id=task.id,
            title=task.title,
            created_by=task.created_by,
            created_at=task.created_at
        )

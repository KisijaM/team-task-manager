from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    id: Optional[str] = None 
    title: str = Field(..., max_length=100)
    created_by: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def create(title: str, created_by: str, ) -> "Task":
        return Task(
            title=title,
            created_by=created_by,
        )

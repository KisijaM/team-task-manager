from pydantic import BaseModel
from datetime import datetime

class TaskDTO(BaseModel):
    id: str
    title: str
    created_by: str
    date: datetime

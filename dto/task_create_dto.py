from pydantic import BaseModel

class TaskCreateDTO(BaseModel):
    title: str
    created_by: str

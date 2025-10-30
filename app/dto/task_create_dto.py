from pydantic import BaseModel, Field

class TaskCreateDTO(BaseModel):
    title: str = Field(..., max_length=50)
    created_by: str = Field(..., max_length=30)

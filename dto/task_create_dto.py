from pydantic import BaseModel, constr, Field

class TaskCreate(BaseModel):
    title: constr(max_length=50) = Field(default="New task")
    created_by: constr(max_length=30)

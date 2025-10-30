from pydantic import BaseModel

class TaskDTO(BaseModel):
    id: str
    title: str
    created_by: str

    @classmethod
    def from_task(cls, task_dict: dict):
        return cls(
            id=str(task_dict["_id"]),
            title=task_dict["title"],
            created_by=task_dict["created_by"]
        )

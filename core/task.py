from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

def generate_id() -> str:
    return str(ObjectId())

class Task(BaseModel):
    id: str
    title: str
    created_by: str
    created_at: datetime

    @staticmethod
    def create(title: str, created_by: str) -> "Task":
        return Task(
            id=generate_id(),
            title=title,
            created_by=created_by,
            created_at=datetime.utcnow()
        )

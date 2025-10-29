from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

# Funkcija za generisanje ObjectId kao string
def generate_object_id() -> str:
    return str(ObjectId())

# Funkcija za default timestamp
def current_datetime() -> datetime:
    return datetime.utcnow()

class Task(BaseModel):
    id: str = Field(default_factory=generate_object_id, alias="_id")
    title: str
    created_by: str
    date: datetime = Field(default_factory=current_datetime)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

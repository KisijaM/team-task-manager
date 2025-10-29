from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

# Function to generate ObjectId as a string
def generate_object_id() -> str:
    return str(ObjectId())

# Function for default timestamp
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


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr, field_validator
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from typing import List

app = FastAPI(title="Task Manager API")


MONGO_URI = "mongodb://localhost:27017"  
client = AsyncIOMotorClient(MONGO_URI)
db = client["taskdb"]
tasks_collection = db["tasks"]


def objectid_to_str(obj_id):
    return str(obj_id) if obj_id else None


class TaskModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: constr(max_length=50)
    created_by: constr(max_length=30)
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class TaskCreate(BaseModel):
    title: constr(max_length=50) = Field(default="New task")
    created_by: constr(max_length=30)


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks():
    try:
        tasks = []
        cursor = tasks_collection.find()
        async for task in cursor:
            task["_id"] = str(task["_id"])  
            tasks.append(TaskModel(**task))
        return tasks
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks", response_model=TaskModel)
async def create_task(task: TaskCreate):
    task_dict = task.model_dump()  # Pydantic V2 način
    task_dict["date"] = datetime.utcnow()
    result = await tasks_collection.insert_one(task_dict)
    new_task = await tasks_collection.find_one({"_id": result.inserted_id})
    if not new_task:
        raise HTTPException(status_code=500, detail="Task not found after creation")
    new_task["_id"] = str(new_task["_id"])
    return TaskModel(**new_task)


@app.delete("/tasks", response_model=dict)
async def delete_all_tasks():
    result = await tasks_collection.delete_many({})
    return {"message": f"{result.deleted_count} tasks deleted successfully"}

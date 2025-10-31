from fastapi import FastAPI
from app.routes import tasks  

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

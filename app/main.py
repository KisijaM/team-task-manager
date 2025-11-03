from fastapi import FastAPI
from app.routes import tasks, auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

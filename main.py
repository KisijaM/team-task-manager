from fastapi import FastAPI
from routes import tasks

app = FastAPI(title="Team Task Manager")

app.include_router(tasks.router)

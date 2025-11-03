from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter()

# Temporary in-memory DB
users_db = {}

class UserRegisterDTO(BaseModel):
    username: str
    password: str

class UserLoginDTO(BaseModel):
    username: str
    password: str

@router.post("/register", tags=["auth"])
async def register(user: UserRegisterDTO):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

@router.post("/login", tags=["auth"])
async def login(user: UserLoginDTO):
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

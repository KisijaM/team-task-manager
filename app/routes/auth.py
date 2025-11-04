from fastapi import APIRouter, HTTPException, Depends, Security
from pydantic import BaseModel, EmailStr
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import create_access_token, verify_token
from app.repositories.user_repository import UserRepository

router = APIRouter()
bearer_scheme = HTTPBearer()
user_repo = UserRepository()

# DTOs
class UserRegisterDTO(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str | None = None
    address: str | None = None

class UserLoginDTO(BaseModel):
    username: str
    password: str

# Auth Helpers
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

# Routes
@router.post("/register", tags=["auth"])
async def register(user: UserRegisterDTO):
    existing_user = await user_repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    created_user = await user_repo.create_user(
        username=user.username,
        password=user.password,
        email=user.email,
        phone_number=user.phone_number,
        address=user.address
    )

    if created_user == "username_exists":
        raise HTTPException(status_code=400, detail="Username already exists")

    if created_user == "email_exists":
        raise HTTPException(status_code=400, detail="Email already exists")

    if not isinstance(created_user, dict):
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    return {"message": "User registered successfully", "user": created_user}

@router.post("/login", tags=["auth"])
async def login(user: UserLoginDTO):
    existing_user = await user_repo.get_user_by_username(user.username)
    if not existing_user or existing_user.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": existing_user["username"],
            "email": existing_user["email"],
            "phone_number": existing_user.get("phone_number"),
            "address": existing_user.get("address")
        }
    }

@router.delete("/delete/{username}", response_model=dict, tags=["auth"])
async def delete_user(username: str, current_user: str = Depends(get_current_user)):
    """
    Delete a user by username. Requires a valid JWT token.
    Users can only delete their own account.
    """
    if username != current_user:
        raise HTTPException(status_code=403, detail="You can only delete your own account")

    deleted_count = await user_repo.delete_user_by_username(username)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

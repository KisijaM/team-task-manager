from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import UserService, get_user_service
from app.dto.user_dto import UserRegisterDTO, UserLoginDTO, UserDTO
from app.security.security import verify_token

router = APIRouter()
bearer_scheme = HTTPBearer()

# To do: change name
def verify_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> str:
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username



@router.post("/register", response_model=UserDTO, tags=["auth"])
async def register(user: UserRegisterDTO, service: UserService = Depends(get_user_service)):
    result = await service.register_user(user)
    
    if "error" in result:
        if result["error"] == "username_exists":
            raise HTTPException(status_code=400, detail="Username already exists")
        if result["error"] == "email_exists":
            raise HTTPException(status_code=400, detail="Email already exists")
        if result["error"] == "creation_failed":
            raise HTTPException(status_code=500, detail="User creation failed")
    
    return result


@router.post("/login", tags=["auth"])
async def login(user: UserLoginDTO, service: UserService = Depends(get_user_service)):
    result = await service.login_user(user.username, user.password)
    
    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return result  


@router.delete("/delete/{user_id}", response_model=dict, tags=["auth"])
async def delete_user(
    user_id: str,
    username: str = Depends(verify_current_user),
    service: UserService = Depends(get_user_service)
):
    deleted_count = await service.delete_user(user_id)
    
    if not deleted_count:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

from pydantic import BaseModel, EmailStr, Field, validator
import re
from typing import Optional

class UserDTO(BaseModel):
    id: str
    username: str = Field(..., min_length=3, max_length=20, description="Username must be between 3 and 20 characters")
    email: EmailStr
    phone_number: Optional[str] = Field(None, description="Phone number must contain 6-15 digits")
    address: Optional[str] = Field(None, max_length=100, description="Address must not exceed 100 characters")

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^\w+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r"^\+?\d{6,15}$", v):
            raise ValueError("Phone number must contain 6-15 digits")
        return v

    @validator("address")
    def validate_address(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError("Address must not exceed 100 characters")
        return v

class UserRegisterDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="Username must be between 3 and 20 characters")
    password: str = Field(..., min_length=8, max_length=50, description="Password must be at least 8 characters long and contain uppercase, lowercase, and number")
    email: EmailStr
    phone_number: Optional[str] = Field(None, description="Phone number must contain 6-15 digits")
    address: Optional[str] = Field(None, max_length=100, description="Address must not exceed 100 characters")

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^\w+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r"^\+?\d{6,15}$", v):
            raise ValueError("Phone number must contain 6-15 digits")
        return v

    @validator("address")
    def validate_address(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError("Address must not exceed 100 characters")
        return v

class UserLoginDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=50)

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^\w+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

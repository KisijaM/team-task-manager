import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

   
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": "your_app",  
        "sub": data.get("sub")  
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


def hash_password(password: str) -> str:
    """Hashes the password using Argon2"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the entered password matches the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

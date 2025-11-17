from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.security.security import verify_token

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

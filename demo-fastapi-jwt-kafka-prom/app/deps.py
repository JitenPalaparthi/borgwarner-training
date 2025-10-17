from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decode_token

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]):
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = creds.credentials
    try:
        data = decode_token(token)
        return data["sub"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

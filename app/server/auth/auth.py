from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.server.auth.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def authenticate(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sign in Required"
        )

    # Decode the token
    decoded_token = verify_access_token(token)
    return decoded_token["user"]

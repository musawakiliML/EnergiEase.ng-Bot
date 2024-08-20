import os
import json
import time
from datetime import datetime, timedelta

from fastapi import status, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ['SECRET_KEY']
refresh_token_expire = os.environ['REFRESH_TOKEN_EXPIRE_DAYS']


def create_access_token(user: str) -> str:

    payload = {
        "user": user,
        "expires": time.time() + 3600
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        expire = data.get("expires")
        print(expire)
        if expire is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Access Token Not Provided"
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Token Expired"
            )

        return data
    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Token"
        )


def create_refresh_token(data: dict):
    try:
        expire = datetime.utcnow() + timedelta(days=int(refresh_token_expire))

        to_encode = data.copy()
        to_encode.update({"expires": expire.timestamp()})

        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")

        return encoded_jwt
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Token"
        )

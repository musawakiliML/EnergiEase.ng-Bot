import os
import time
from datetime import datetime, timedelta

from fastapi import status, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ['SECRET_KEY']
refresh_token_expire = os.environ['REFRESH_TOKEN_EXPIRE_DAYS']


def create_access_token(user: str) -> str:
   """_summary_

   Args:
       user (str): _description_

   Returns:
       str: _description_
   """
   payload = {
        "user": user,
        "expires": time.time() + 3600
    }

   token = jwt.encode(payload, secret_key, algorithm="HS256")
   return token


def verify_access_token(token: str):
    """_summary_

    Args:
        token (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
      data = jwt.decode(token, secret_key, algorithms=["HS256"])
      expire = data.get("expires")
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
    """Create Refresh Token

    Args:
        data (dict): user data

    Raises:
        HTTPException: Throws exceptions

    Returns:
        dict: refresh token
    """

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

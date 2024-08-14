import os
import time
from datetime import datetime

from fastapi import status, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ['SECRET_KEY']

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


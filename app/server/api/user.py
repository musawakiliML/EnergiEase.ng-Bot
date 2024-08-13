import json
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, Form, UploadFile, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from app.server.auth.hash_password import HashPassword
from app.server.utils.supabase_util import upload_to_supabase
from app.server.database.crud import get_user_by_id, create_user, update_user_by_id, get_user_by_email
from app.server.schema.user_model import UserUpdateSchema
from app.server.auth.jwt_handler import create_access_token, verify_access_token
from app.server.auth.auth import authenticate


router = APIRouter()

# Hash Password Object for password encryption and validation
hash_password = HashPassword()

# User Authentication Routes

# Login View


@router.post("/login", status_code=status.HTTP_200_OK, response_description="User Login")
async def login_view(user: OAuth2PasswordRequestForm = Depends()):
    try:
        user_data = await get_user_by_email(email=user.username)

        if user_data.get('message') == "Successful":
            user_details = user_data.get('data')
            if hash_password.verify_hash(user.password, user_details['password']): # type: ignore
                access_token = create_access_token(
                    user_details['email_address'] # type: ignore
                )
                response = {
                    "access_token": access_token,
                    "token_type": "Bearer"
                }
                return JSONResponse(
                   content=response,
                   status_code=status.HTTP_200_OK
                )
    except Exception as e:
        response = {
            "message": "User Doesn't Exist",
            "status": status.HTTP_401_UNAUTHORIZED
        }
        return JSONResponse(
            content=response,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

# Signup View


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_description="Create A New User")
async def create_user_view(
        first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], username: Annotated[str, Form()], email_address: Annotated[str, Form()], password: Annotated[str, Form()], role: Annotated[str, Form()], active: Annotated[str, Form()], location: Annotated[str, Form()], profile_pic: UploadFile):
    try:
        # Check if user email exists
        get_user = await get_user_by_email(email=email_address)

        if get_user.get('message') == "Successful":

            response = {
                "message": "User With Email Already Exists",
                "status": status.HTTP_409_CONFLICT
            }

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=response
            )

        # Upload Image to Supabase Bucket
        upload_response = upload_to_supabase(
            profile_pic.file, profile_pic.filename)  # type: ignore

        url_response = json.loads(upload_response.body)
       #   print(url_response)

        if url_response['status'] == 200:
            public_url = url_response['public_url']

        # Create User
        user_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email_address": email_address,
            "password": hash_password.create_hash(password),
            "role": role,
            "active": active,
            "location": location,
            "profile_pic": public_url,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        user_data = await create_user(user_details=user_dict)

        if user_data.get('message') == "Successful":

            response = {
                "message": "User Created Successfully",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(user_data.get("data"))
            }

        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)

    except Exception as e:

        response = {
            "message": "Error Creating User",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": f"{str(e)}"
        }

        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)


# User Update
@router.put("/update/{id}", status_code=status.HTTP_200_OK, response_description="Update User")
async def update_user_view(id: str, user_data: UserUpdateSchema = Body(...), user: str = Depends(authenticate)):
    try:
        pass
    except Exception as e:

        response = {
            "message": "Error Updating User",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": f"{str(e)}"
        }

        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)

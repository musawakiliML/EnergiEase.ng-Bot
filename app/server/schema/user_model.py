from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """User Model

    Args:
        BaseModel (_type_): _description_
    """

    first_name: str | None
    last_name: str | None
    username: str | None
    email_address: EmailStr | None
    password: str | None
    role: str | None
    active: bool = True
    location: str | None
    profile_pic: str | None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email_address": "johndoe@example.com",
                "password": "password",
                "role": "customer support",
                "active": True,
                "location": "Lagos",
                "profile_pic": "https://supabase.com/energiease/assets/profile_pic.jpg",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            }
        }


class UserLoginSchema(BaseModel):
    email_address: EmailStr | None
    password: str | None

    class Config:
        json_schema_extra = {
            "example": {"email_address": "johndoe@example", "password": "password"}
        }


class UserToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {"example": {"access_token": "", "token_type": ""}}


class UserUpdateSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str | None
    email_address: EmailStr | None
    password: str | None
    role: str | None
    active: bool = True
    location: str | None
    profile_pic: str | None
    updated_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email_address": "johndoe@example.com",
                "password": "password",
                "role": "customer support",
                "active": True,
                "location": "Lagos",
                "profile_pic": "https://supabase.com/energiease/assets/profile_pic.jpg",
                "updated_at": str(datetime.now()),
            }
        }


class AdminUserSchema(BaseModel):
    username: str | None
    email_address: EmailStr | None
    password: str | None
    role: str | None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admiuser",
                "email_address": "admin@email.com",
                "password": "password",
                "role": "admin",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            }
        }

from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime

class UserSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    username: str = Field(...)
    first_name: str = Field(...)
    email: str = Field(...)
    created_at: Union[datetime, None] = None

class UserProfileSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    phone_number: str = Field(...)
    phone_id: str = Field(...)
    user: UserSchema
    created_at: Union[datetime, None] = None

class OrdersSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    user_profile: UserProfileSchema
    meter_distribution: str = None
    user_meter_number: str = None
    meter_owner: str = None
    meter_address: str = None
    user_amount: str = None
    meter_type: str = None
    payment_confirmation: str = None
    unit_confirmation: str = None
    token: str = None
    units: str = None
    payment_mode: str = None
    transaction_reference: str = None
    created_at: Union[datetime, None] = None

class UserSessionSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    session_id: str = Field(...)
    user_phone_number: str = Field(...)
    user_name: str = Field(...)
    entry_message: str = None
    user_input_1: str = None
    user_input_2: str = None
    meter_owner: str = None
    meter_address: str = None
    user_meter_number: str = None
    meter_type: str = None
    meter_distribution: str = None
    user_amount: str = None
    user_confirm: str = None
    payment_mode: str = None
    transaction_reference: str = None
    created_at: Union[datetime, None] = None
    user_profile: UserProfileSchema
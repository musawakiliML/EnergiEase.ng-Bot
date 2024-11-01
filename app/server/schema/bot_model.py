from typing import Optional, Union, List
from datetime import datetime
from pydantic import BaseModel, Field


class UserProfileSchema(BaseModel):
    ''' Creating a User Profile Model'''
    # id: str = Field(..., alias="_id")
    username: str = Field(...)
    full_name: str = Field(...)
    user_id: str = Field(...)
    created_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "668ee347405be690b5693300",
                "username": "johndoe",
                "full_name": "John Doe",
                "user_id": 936591022,
                "created_at": str(datetime.now())
            }
        }


class OrdersSchema(BaseModel):
    '''Creating an Order Model'''
    # id: str = Field(..., alias="_id")
    # List[Optional[str]] = [None]
    # Union[str, None]
    user_profile: UserProfileSchema
    session_id: str | None
    meter_distribution: str | None
    user_meter_number: str | None
    user_amount: str | None
    meter_type: str | None
    meter_code: str | None
    payment_confirmation: str | None
    unit_confirmation: str | None
    token: str | None
    units: str | None
    transaction_id: str | None
    transaction_reference: str | None
    order_status: str | None
    created_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "668ee347405be690b5693300",
                "userprofile": {},
                "session_id": "a2324d70872b",
                "meter_distribution": "",
                "user_meter_number": "",
                "user_amount": "",
                "meter_type": "",
                "meter_code": "",
                "payment_confirmation": "",
                "unit_confirmation": "",
                "token": "",
                "units": "",
                "transaction_id": "",
                "transaction_reference": "",
                "order_status": "",
                "created_at": str(datetime.now())
            }
        }

class UserSessionSchema(BaseModel):
    '''Creating an Order Model'''
    # id: str = Field(..., alias="_id")
    # List[Optional[str]] = [None]
    # Union[str, None]
    user_profile: UserProfileSchema
    session_id: str | None
    user_phone_number: str | None
    entry_message: str | None
    user_input_1: str | None
    user_input_2: str | None
    user_confirm: str | None
    meter_distribution: str | None
    user_meter_number: str | None
    user_amount: str | None
    meter_type: str | None
    meter_code: str | None
    payment_confirmation: str | None
    unit_confirmation: str | None
    token: str | None
    units: str | None
    transaction_id: str | None
    transaction_reference: str | None
    order_status: str | None
    created_at: Union[datetime, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "668ee347405be690b5693300",
                "userprofile": {},
                "session_id": "a2324d70872b",
                "user_phone_number": "0990767655542",
                "entry_message": "",
                "user_input_1":"",
                "user_input_2":"",
                "user_confirm":"",
                "meter_distribution": "",
                "user_meter_number": "",
                "user_amount": "",
                "meter_type": "",
                "meter_code": "",
                "payment_confirmation": "",
                "unit_confirmation": "",
                "token": "",
                "units": "",
                "transaction_id": "",
                "transaction_reference": "",
                "order_status": "",
                "created_at": str(datetime.now())
            }
        }


class MeterDetailsSchema(BaseModel):
    '''Creating a Meter Details Model'''
    session_id: str | None
    meter_owner: str | None
    meter_number: str | None
    meter_address: str | None
    meter_account_number: str | None
    meter_account_name: str | None
    meter_bank_name: str | None
    meter_package: str | None
    customer_id: str | None

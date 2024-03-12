from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime

class UserProfileSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    username: str = Field(...)
    full_name: str = Field(...)
    user_id: str = Field(...)
    created_at: Union[datetime, None] = None

class OrdersSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    user_profile: UserProfileSchema
    session_id: str = None
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
    order_status: str = None
    created_at: Union[datetime, None] = None
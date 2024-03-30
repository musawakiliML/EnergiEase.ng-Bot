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

class OrdersSchema(BaseModel):
    '''Creating an Order Model'''
    # id: str = Field(..., alias="_id")
    # List[Optional[str]] = [None]
    # Union[str, None]
    user_profile: UserProfileSchema
    session_id: str | None
    meter_distribution: str | None
    user_meter_number: str | None
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
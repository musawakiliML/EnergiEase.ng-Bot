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
    user_profile: UserProfileSchema
    session_id: List[Optional[str]] = [None]
    meter_distribution: List[Optional[str]] = [None]
    user_meter_number: List[Optional[str]] = [None]
    meter_owner: List[Optional[str]] = [None]
    meter_address: List[Optional[str]] = [None]
    user_amount: List[Optional[str]] = [None]
    meter_type: List[Optional[str]] = [None]
    meter_code: List[Optional[str]] = [None]
    payment_confirmation: List[Optional[str]] = [None]
    unit_confirmation: List[Optional[str]] = [None]
    token: List[Optional[str]] = [None]
    units: List[Optional[str]] = [None]
    transaction_id: List[Optional[str]] = [None]
    transaction_reference: List[Optional[str]] = [None]
    order_status: List[Optional[str]] = [None]
    created_at: Union[datetime, None] = None
def user_profile_serializer(input_data: dict) -> dict:
    ''' User Profile Serializer'''
    return {
        "_id": str(input_data["_id"]),
        "username": input_data["username"],
        "full_name": input_data["full_name"],
        "user_id": input_data["user_id"],
        "created_at": str(input_data["created_at"])
    }


def order_serializer(input_data: dict) -> dict:
    ''' Order Serializer ''' 
    return {
        "_id": str(input_data["_id"]),
        "user_profile": input_data["user_profile"],
        "session_id":input_data["session_id"],
        "meter_distribution": input_data["meter_distribution"],
        "user_meter_number": input_data["user_meter_number"],
        "meter_owner": input_data["meter_owner"],
        "meter_address": input_data["meter_address"],
        "user_amount": input_data["user_amount"],
        "meter_type": input_data["meter_type"],
        "meter_code":input_data["meter_code"],
        "token": input_data["token"],
        "units": input_data["units"],
        "payment_confirmation": input_data["payment_confirmation"],
        "unit_confirmation": input_data["unit_confirmation"],
        "transaction_id": input_data["transaction_id"],
        "order_status": input_data["order_status"],
        "transaction_reference": input_data["transaction_reference"],
        "created_at": str(input_data["created_at"])

     }

def meter_details_serializer(input_data: dict) -> dict:
    '''Meter Details Serializer'''
    return  {
        "session_id": input_data["session_id"],
        "meter_owner": input_data["meter_owner"],
        "meter_number": input_data["meter_number"],
        "meter_address": input_data["meter_address"],
        "meter_account_number": input_data["meter_account_number"],
        "meter_account_name": input_data["meter_account_name"],
        "meter_bank_name": input_data["meter_bank_name"],
        "meter_package": input_data["meter_package"],
        "customer_id": input_data["customer_id"],
    }
    
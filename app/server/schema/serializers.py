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
        "session_id": input_data["session_id"],
        "meter_distribution": input_data["meter_distribution"],
        "user_meter_number": input_data["user_meter_number"],
        "meter_owner": input_data["meter_owner"],
        "meter_address": input_data["meter_address"],
        "user_amount": input_data["user_amount"],
        "meter_type": input_data["meter_type"],
        "meter_code": input_data["meter_code"],
        "token": input_data["token"],
        "units": input_data["units"],
        "payment_confirmation": input_data["payment_confirmation"],
        "unit_confirmation": input_data["unit_confirmation"],
        "transaction_id": input_data["transaction_id"],
        "transaction_reference": input_data["transaction_reference"],
        "order_status": input_data["order_status"],
        "created_at": str(input_data["created_at"])

    }


def user_session_serializer(input_data: dict):
    ''' User Session Serializer '''

    return {
        "_id": str(input_data["_id"]),
        "user_profile": input_data["user_profile"],
        "session_id": input_data["session_id"],
        "user_phone_number": input_data["user_phone_number"],
        "entry_message": input_data["entry_message"],
        "user_input_1": input_data["user_input_1"],
        "user_input_2": input_data["user_input_2"],
        "user_confirm": input_data["user_confirm"],
        "meter_distribution": input_data["meter_distribution"],
        "user_meter_number": input_data["user_meter_number"],
        "meter_owner": input_data["meter_owner"],
        "meter_address": input_data["meter_address"],
        "user_amount": input_data["user_amount"],
        "meter_type": input_data["meter_type"],
        "meter_code": input_data["meter_code"],
        "token": input_data["token"],
        "units": input_data["units"],
        "payment_confirmation": input_data["payment_confirmation"],
        "unit_confirmation": input_data["unit_confirmation"],
        "transaction_id": input_data["transaction_id"],
        "transaction_reference": input_data["transaction_reference"],
        "order_status": input_data["order_status"],
        "created_at": str(input_data["created_at"])

    }


def meter_details_serializer(input_data: dict) -> dict:
    '''Meter Details Serializer'''

    return {
        "meter_owner": input_data["meter_owner"],
        "meter_number": input_data["meter_number"],
        "meter_address": input_data["meter_address"],
        "meter_package": input_data["meter_package"],
        "meter_distributions": input_data["meter_distributions"],
        "meter_code": input_data["meter_code"]
    }


def user_details_serializer(input_data: dict):
    '''User Details Serializer'''

    return {
        "first_name": input_data["first_name"],
        "last_name": input_data["last_name"],
        "username": input_data["username"],
        "email_address": input_data["email_address"],
        "password": input_data["password"],
        "role": input_data["role"],
        "active": input_data["active"],
        "location": input_data["location"],
        "profile_pic": input_data["profile_pic"],
        "created_at": input_data["created_at"],
        "updated_at": input_data["updated_at"]
    }


def admin_details_serializer(input_data: dict):
    ''' Admin User Details Serializer'''

    return {
        "username": input_data["username"],
        "email_address": input_data["email_address"],
        "password": input_data["password"],
        "role": input_data["role"],
        "created_at": input_data["created_at"],
        "updated_at": input_data["updated_at"]
    }

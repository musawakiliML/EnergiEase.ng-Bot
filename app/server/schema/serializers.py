def user_profile_serializer(input) -> dict:
    
    return {
        "_id": str(input["_id"]),
        "username": input["username"],
        "full_name": input["full_name"],
        "user_id": input["user_id"],
        "created_at": str(input["created_at"])
    }


def order_serializer(input) -> dict:
    
    return {
        "_id": str(input["_id"]),
        "user_profile": input["user_profile"],
        "session_id":input["session_id"],
        "meter_distribution": input["meter_distribution"],
        "user_meter_number": input["user_meter_number"],
        "meter_owner": input["meter_owner"],
        "meter_address": input["meter_address"],
        "user_amount": input["user_amount"],
        "meter_type": input["meter_type"],
        "token": input["token"],
        "units": input["units"],
        "payment_confirmation": input["payment_confirmation"],
        "unit_confirmation": input["unit_confirmation"],
        "payment_mode": input["payment_mode"],
        "order_status": input["order_status"],
        "transaction_reference": input["transaction_reference"],
        "created_at": str(input["created_at"])
    }
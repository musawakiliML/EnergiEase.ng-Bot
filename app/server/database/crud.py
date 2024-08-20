from bson.objectid import ObjectId

from app.server.database.config import (
    energiease_user_profile,
    energiease_user_order,
    energiease_meter_details,
    energiease_user_details,
)

from app.server.schema.serializers import (
    user_profile_serializer,
    order_serializer,
    meter_details_serializer,
    user_details_serializer,
)


# ================ Order Crud ================= #
# Create order


async def create_order(user_order_data: dict):
    '''Create an Order'''
    try:
        order = await energiease_user_order.insert_one(user_order_data)
        new_order = await energiease_user_order.find_one({"_id": order.inserted_id})
        if new_order:
            return order_serializer(new_order)
    except Exception as e:
        return {"Error in add_user_session": str(e)}


# Get single order

async def get_single_order(session_id: str):
    '''Get Single Order Details'''
    user_order = await energiease_user_order.find_one({"session_id": session_id})
    if user_order:
        return order_serializer(user_order)
    else:
        return {"message": "not_found"}


async def get_single_order_transaction(transaction_reference: str):
    '''Get single order based on Transaction reference'''
    user_order = await energiease_user_order.find_one({"transaction_reference": transaction_reference})

    if user_order:
        return order_serializer(user_order)
    else:
        return {"message": "not_found"}

# Update User Order During Session


async def update_user_order(user_order_data: list, session_id: str):
    '''Update Single User Order'''
    try:
        update_user_order = await energiease_user_order.update_one({"session_id": session_id}, {"$set": {user_order_data[0]: user_order_data[1]}})
        updated_user_order = await energiease_user_order.find_one({"session_id": session_id})

        if updated_user_order:
            return order_serializer(updated_user_order)
        else:
            return {"Message": f'No post with this id: {id} found'}
    except Exception as e:
        return {"Error in update_user_session": str(e)}

# Update User Order During transfer


async def update_user_order_transaction(user_order_data: list, transaction_id: str):
    '''Update Single User Order'''
    try:
        update_user_order = await energiease_user_order.update_one({"transaction_id": transaction_id}, {"$set": {user_order_data[0]: user_order_data[1]}})
        updated_user_order = await energiease_user_order.find_one({"transaction_id": transaction_id})

        if updated_user_order:
            return order_serializer(updated_user_order)
        else:
            return {"Message": f'No post with this id: {id} found'}
    except Exception as e:
        return {"Error in update_user_session": str(e)}

# ================ User Profile ================= #

# Create user profile


async def create_user_profile(user_profile_data: dict):
    '''Create a single user profile'''
    try:
        user_profile = await energiease_user_profile.insert_one(user_profile_data)
        new_user_profile = await energiease_user_profile.find_one({"_id": user_profile.inserted_id})
        return user_profile_serializer(new_user_profile)  # type: ignore

    except Exception as e:
        return {"message": f"{str(e)}"}

# Get user Profile


async def get_user_profile(session_id: str):
    '''Get a single user'''

    try:
        user_profile = await energiease_user_profile.find_one({"user_id": session_id})

        if user_profile:
            return user_profile_serializer(user_profile)
        else:
            return {"message": "not_found"}
    except Exception as e:
        return {"message": f"{str(e)}"}

# Get User Profile by ID


async def get_user_profile_by_id(user_id: str) -> dict:  # type: ignore
    ''' Get Single User Profile by ID'''
    try:
        user_profile = await energiease_user_profile.find_one({"_id": ObjectId(user_id)})

        if user_profile:
            data = {
                "message": "Successful",
                "data": user_profile_serializer(user_profile)
            }
            return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# Get All User profiles for dashboard


async def get_all_user_profile() -> dict:
    ''' Get All User Profile'''

    try:
        user_profiles_data = []
        async for profile in energiease_user_profile.find({}):
            user_profiles_data.append(user_profile_serializer(profile))

        data = {
            "message": "Successful",
            "data": user_profiles_data
        }
        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# ================ Orders Details =================

# Get All Order Details


async def get_all_orders() -> dict:
    ''' Retrieve All User Orders '''
    try:
        # Get all Orders
        all_orders_data = []
        async for order in energiease_user_order.find({}):
            all_orders_data.append(order_serializer(order))

        data = {
            "message": "Successful",
            "data": all_orders_data
        }

        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# Get Single Order


async def get_single_order_by_id(id: str) -> dict:  # type: ignore
    ''' Get Single User Orders'''
    try:
        # Get Single Order
        user_order = await energiease_user_order.find_one({"_id": ObjectId(id)})

        if user_order:
            data = {
                "message": "Successful",
                "data": order_serializer(user_order)
            }
            return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }


# Get All Users Order

async def get_all_users_order(id: str) -> dict:
    ''' Get All Users Order '''
    try:
        # Get User Order
        user_orders = []
        async for order in energiease_user_order.find({"user_profile._id": id}):
            user_orders.append(order_serializer(order))

        data = {
            "message": "Successful",
            "data": user_orders
        }

        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# ================ User Crud ================= #

# Create user account


async def create_user(user_details: dict) -> dict:  # type: ignore
    try:
        user_data = await energiease_user_details.insert_one(user_details)
        new_user_data = await energiease_user_details.find_one({"_id": user_data.inserted_id})

        if new_user_data:

            data = {
                "message": "Successful",
                "data": user_details_serializer(new_user_data)
            }
            return data

    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# Get User Account Information


async def get_user_by_id(id: str):
    try:
        user_data = await energiease_user_details.find_one({"_id": ObjectId(id)})

        if user_data:
            data = {
                "message": "Successful",
                "data": user_details_serializer(user_data)
            }
        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"

        }


async def get_user_by_email(email: str):
    try:
        user_data = await energiease_user_details.find_one({"email_address": email})

        if user_data:
            data = {
                "message": "Successful",
                "data": user_details_serializer(user_data)
            }
        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }


# Update User ID
async def update_user_by_id(id: str, user_data: dict):
    try:
        update_user_data = await energiease_user_details.update_one({"_id": ObjectId(id)}, {"$set": user_data})
        updated_user_data = await energiease_user_details.find_one({"_id": ObjectId(id)})

        if updated_user_data:
            data = {
                "message": "Successful",
                "data": user_details_serializer(updated_user_data)
            }
        return data
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }

# ================== Creating Meter Details CRUD ====================

# Create Meter Details


async def create_meter_details(meter_details_data: dict):
    '''Create a meter detail'''
    try:
        meter_details = await energiease_meter_details.insert_one(meter_details_data)
        new_meter_details = await energiease_meter_details.find_one({"_id": meter_details.inserted_id})
        if new_meter_details:
            return meter_details_serializer(new_meter_details)
    except Exception as e:
        return {"Error in create meter details": str(e)}

# Update Meter Details


async def update_meter_details(meter_detail_data: list, session_id: str):
    '''Update Meter Details'''
    try:
        update_meter_details_data = await energiease_meter_details.update_one({"session_id": session_id}, {"$set": {meter_detail_data[0]: meter_detail_data[1]}})
        updated_meter_details = await energiease_meter_details.find_one({"session_id": session_id})

        if updated_meter_details:
            return meter_details_serializer(updated_meter_details)
        else:
            return {"Message": f'No post with this id: {id} found'}
    except Exception as e:
        return {"Error in update_meter_details": str(e)}

# Get Meter Details


async def get_meter_details(session_id: str):
    '''Get a single meter details'''
    try:
        meter_details = await energiease_meter_details.find_one({"session_id": session_id})

        if meter_details:
            return meter_details_serializer(meter_details)
        else:
            return {"message": "Meter Details not found"}
    except Exception as e:
        return {"message": f"{str(e)}"}

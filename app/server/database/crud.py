from bson.objectid import ObjectId

from app.server.schema.bot_model import (
    UserProfileSchema,
    OrdersSchema
    )

from app.server.database.config import (
    energiease_user_profile,
    energiease_user_order
    )

from app.server.schema.serializers import (
    user_profile_serializer,
    order_serializer
    )

# Create order

async def create_order(user_order_data: dict):
    order = await energiease_user_order.insert_one(user_order_data)
    new_order = await energiease_user_order.find_one({"_id":order.inserted_id})
    return order_serializer(new_order)


# Get single order

async def get_single_order(session_id: str):
    user_order = await energiease_user_order.find_one({"session_id":session_id})
    if user_order:
        return order_serializer(user_order)
    else:
        return {"message":"not_found"}

async def get_single_order_transaction(transaction_reference: str):
    user_order = await energiease_user_order.find_one({"transaction_reference":transaction_reference})

    if user_order:
        return order_serializer(user_order)
    else:
        return {"message":"not_found"}

# Add user session

async def add_user_session(user_session_data: UserProfileSchema):
    user_session_data = user_session_data.model_dump()
    # print(user_session_data)
    try:
        user_session = await user_sessions.insert_one(user_session_data)
        new_user_session = await user_sessions.find_one({"_id": user_session.inserted_id})
        if new_user_session:
            return user_session_serializer(new_user_session)
    except Exception as e:
        print(f"Error in add_user_session: {str(e)}")

# Update User Order

async def update_user_order(user_order_data: list, session_id: str):
    try:

        updated_user_session = await user_sessions.update_one({"session_id":session_id}, {"$set":{user_session_data[0]:user_session_data[1]}})
        updated_session = await user_sessions.find_one({"session_id":session_id})

        if updated_user_session:
            # print(updated_session)
            return user_session_serializer(updated_session)
        else:
            return {"Message":f'No post with this id: {id} found'}
    except Exception as e:
        print(f"Error in update_user_session: {str(e)}")

# Create user profile

async def create_user_profile(user_profile_data: dict):
    user_profile = await energiease_user_profile.insert_one(user_profile_data)
    new_user_profile = await energiease_user_profile.find_one({"_id":user_profile.inserted_id})
    return user_profile_serializer(new_user_profile)

# Get user Profile

async def get_user_profile(session_id: str):
    user_profile = await energiease_user_profile.find_one({"user_id":session_id})
    
    if user_profile:
        return user_profile_serializer(user_profile)
    else:
        return {"message":"not_found"}  
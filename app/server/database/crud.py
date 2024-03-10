from bson.objectid import ObjectId

from app.server.models.chatbot_models import (
    UserSchema,
    UserProfileSchema,
    UserSessionSchema,
    OrdersSchema
    )

from app.server.database.db_connection import (
    user_sessions,
    user_orders,
    user_profiles,
    users
    )

from app.server.serializers.chatbot_serializers import (
    user_session_serializer,
    user_profile_serializer,
    user_serializer,
    order_serializer
    )

# get single session

async def get_single_session(session_id: str):
    # user_session = await user_sessions.find_one({"_id":ObjectId(id)})
    user_session = await user_sessions.find_one({"session_id":session_id})
    # print(user_session)
    if user_session:
        return user_session_serializer(user_session)
    else:
        return {"message":"not_found"}

async def get_single_session_transaction(transaction_reference: str):
    # user_session = await user_sessions.find_one({"_id":ObjectId(id)})
    user_session = await user_sessions.find_one({"transaction_reference":transaction_reference})
    # print(user_session)
    if user_session:
        return user_session_serializer(user_session)
    else:
        return {"message":"not_found"}

# Add user session

async def add_user_session(user_session_data: UserSessionSchema):
    user_session_data = user_session_data.model_dump()
    # print(user_session_data)
    try:
        user_session = await user_sessions.insert_one(user_session_data)
        new_user_session = await user_sessions.find_one({"_id": user_session.inserted_id})
        if new_user_session:
            return user_session_serializer(new_user_session)
    except Exception as e:
        print(f"Error in add_user_session: {str(e)}")

# Update User session

async def update_user_session(user_session_data: list, session_id: str):
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

# delete single session

async def delete_single_session(session_id: str):
    # user_session = await user_sessions.find_one({"_id":ObjectId(id)})
    await user_sessions.delete_one({"session_id":session_id})
    return {"Message":"Session Deleted Successfully!"}

# Create user

async def create_user(user_data: dict):
    user = await users.insert_one(user_data)
    new_user = await users.find_one({"_id":user.inserted_id})
    return user_serializer(new_user)


# Retrieve User

async def get_user(session_id: str):
    user = await users.find_one({"username":session_id})
    if user:
        return user_serializer(user)
    # else:
    #     return {"message":"not_found"}

# Create user profile

async def create_user_profile(user_profile_data: dict):
    user_profile = await user_profiles.insert_one(user_profile_data)
    new_user_profile = await user_profiles.find_one({"_id":user_profile.inserted_id})
    return user_profile_serializer(new_user_profile)

# get user Profile

async def get_user_profile(session_id: str):
    user_profile = await user_profiles.find_one({"phone_id":session_id})
    if user_profile:
        return user_profile_serializer(user_profile)
    else:
        return {"message":"not_found"}

# Create order

async def create_order(user_order_data: dict):
    order = await user_orders.insert_one(user_order_data)
    new_order = await user_orders.find_one({"_id":order.inserted_id})
    return order_serializer(new_order)    
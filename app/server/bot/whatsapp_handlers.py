import random
from datetime import datetime
from bson.objectid import ObjectId

from app.server.utils.whatsapp import send_whatsapp_message_normal, send_whatsapp_message_buttons
from app.server.bot.whatsapp_messages import *
# from app.server.utils.payment import init_transaction, init_bank_transfer
# from app.server.utils.vtpass_functions import vtpass, credentials

from app.server.schema.bot_model import (
    UserProfileSchema,
    UserSessionSchema,
    OrdersSchema
    )

from app.server.database.crud import (
    get_user_profile
)


# async def handle_whatsapp_chat(phonenumber, text, profilename, phoneid):
#     try:
#     #    print("Here")
#        # Check if session exists
#        get_chat = await get_single_session(phoneid)
#        if get_chat['user_phone_number'] == phonenumber:
#            chat = get_chat
#         #    print(chat)
#     except:
#         created_at = datetime.utcnow()
#         # print("Inside Except!")
#         user = await get_user(phoneid)
#         # print("After getting user!")
#         if user:
#             if user["username"] == phoneid:
#                 user = user
#                 user_profile = await get_user_profile(phoneid)
#         else:
#             # print("Creating New user!")
#            # Create User
#             user_data = {
#                "username":phoneid,
#                "first_name": profilename,
#                "email": "chat@energieasebot.ng",
#                "created_at": created_at
#            }
#             user = await create_user(user_data)
#             # print("After Creating user!!")
#            # Create User Profile
#             user_profile_data = {
#                "phone_number": phonenumber,
#                "phone_id": phoneid,
#                "user": user,
#                "created_at": created_at
#            }
#             user_profile = await create_user_profile(user_profile_data)
#             # print("After Creating User Profile")
        
#         # Create Chat Session
#         # print("Before add_user_session")
#         try:
#             chat_session_data = UserSessionSchema(
#             # _id=str(ObjectId()),
#             session_id=phoneid,
#             user_phone_number=phonenumber,
#             user_name=profilename,
#             user_profile=user_profile,
#             created_at=str(created_at)
#             )

#             chat = await add_user_session(chat_session_data)
#             # print("After add_user_session")
#         except Exception as e:
#             print(f"Exception in add_user_session: {str(e)}")

#         opening = ['hi', 'Hi', 'Hello', 'Hello', 'Hey', 'hey']
#         opening_msg = random.choice(opening).upper()

#         if text in opening or text:
#             message = welcome_menu(opening_msg, profilename)
#             send_whatsapp_message_buttons(phonenumber, message)
    
#     quit_inputs = ['q', 'Q', 'Quit', 'quit', 'QUIT']
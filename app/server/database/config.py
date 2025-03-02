import asyncio
import os

# Importing enviroment Variables
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.environ["MONGODB_URL"]

# Database Configuration

client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
client.get_io_loop = asyncio.get_event_loop

# Database Connection Test

try:
    db_connection = client.server_info()
    print("Connection to Mongo DB Server Successfull")
except Exception as e:
    print("Connection Unsuccessfull")
    print(str(e))

database = client.energiease_bot

# Database Collections

energiease_user_profile = database.get_collection("energiease_user_profiles")
energiease_user_order = database.get_collection("energiease_user_orders")
energiease_meter_details = database.get_collection("energiease_meter_details")
energiease_user_details = database.get_collection("energiease_user_details")
energiease_payment_details = database.get_collection("energiease_payment_details")
energiease_session_details = database.get_collection("energiease_sessions_whatsapp")

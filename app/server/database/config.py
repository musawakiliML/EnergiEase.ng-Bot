import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Importing enviroment Variables
from dotenv import load_dotenv

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
from venv import logger
from app.server.utils.api_config import *
from app.server.utils.buy_electricity import buy_meter_unit
from app.server.database.crud import get_single_order_transaction, update_user_order, update_user_order_transaction
from uuid6 import uuid7
from dotenv import load_dotenv

from telegram import Bot

from app.server.bot.message import order_confirmation_message, order_failed, order_successful

fintava_credentials = FintavaCredentials(api_key=False, is_live=False)

credentials = fintava_credentials.credentials()

fintava = FintavaOperations()

# Enable Bot Token
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_API"]

# Creating virtual account
def create_account(name: str, amount:str):
   """Create Virtual Accounts"""
   try:
      virtual_account = fintava.create_virtual_account(
         credentials=credentials,
         customer_name=name,
         phone="+2348135810804",
         email="musaadamuw@gmail.com",
         expire_time=15,
         merchant_reference=str(uuid7()).split("-")[4],
         description="Electricity Purchase",
         amount=amount,
      )
      if virtual_account['status'] == 200:
         account_details = {
            "Account Name": virtual_account['data']['virtualAcctName'],
            "Merchant Ref": virtual_account['data']['merchantReference'],
            "Account Number": int(virtual_account['data']['virtualAcctNo']),
            "Bank": virtual_account['data']['bank'],
            "ID": virtual_account['data']['id'],
            "Payment Status": virtual_account['data']['paymentStatus'],
            "status":"200"
         }

         return account_details

   except Exception:
      return {
         "status":virtual_account['status'],
         "message": virtual_account['message']
              }

async def verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference):
   '''Verify Payment to virtual account'''
   try:
      get_order_details = await get_single_order_transaction(transaction_reference)
      order_id = get_order_details["_id"]

      # Creating a Bot Instance to send Order confirmation and Unit Token
      bot = Bot(token=TELEGRAM_BOT_TOKEN)

      if transaction_status == "PAID" and get_order_details['transaction_reference'] == transaction_reference:
         
         # Send Order Confirmation Message
         user_id = get_order_details['user_profile']['user_id']

         await bot.send_message(chat_id=user_id, text=order_confirmation_message(order_id=order_id))

         # Buy Electricity unit
      
         buy_unit = buy_meter_unit(
            meter_number=get_order_details["user_meter_number"],
            meter_type=get_order_details["meter_type"],
            disco=get_order_details["meter_code"],
            amount=get_order_details["user_amount"]
         )
         # print(buy_unit)
         if buy_unit["status"] == "200":

            # Get Order details
            meter_token = buy_unit['meter_token']
            meter_unit = buy_unit['meter_units']
            # Send Order Confirmation Message for buying units
            user_id = get_order_details['user_profile']['user_id']

            await bot.send_message(chat_id=user_id, text=order_successful(
               meter_number=get_order_details["user_meter_number"],
               meter_unit=meter_unit,
               meter_token=meter_token
            )
            )

            # Update Database
            token_data = ["token", meter_token]
            unit_data = ["units", meter_unit]
            unit_confirmation = ["unit_confirmation", "SUCCESSFUL"]
            order_status = ["order_status", "COMPLETED"]
            await update_user_order_transaction(token_data, transaction_id)
            await update_user_order_transaction(unit_data, transaction_id)
            await update_user_order_transaction(unit_confirmation, transaction_id)
            await update_user_order_transaction(order_status, transaction_id)
            return buy_unit
         else:
            user_id = get_order_details['user_profile']['user_id']

            await bot.send_message(chat_id=user_id, text=order_failed(
               order_id=order_id
                  )
               )
            # Update Database
            unit_confirmation = ["unit_confirmation", "FAILED"]
            order_status = ["order_status", "FAILED"]
            await update_user_order_transaction(unit_confirmation, transaction_id)
            await update_user_order_transaction(order_status, transaction_id)
            return {
               "status":buy_unit['status'],
               "message": "Error Occured!"
               }
         
      # # elif transaction_status == "UNDERPAID" and get_order_details['transaction_reference'] == transaction_reference:

      #    return {
      #       'message':"underpaid"
      #       }
   except Exception:
      return {
         "status":buy_unit['status'],
         "message": buy_unit['message']
              }
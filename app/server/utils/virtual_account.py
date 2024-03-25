from app.server.utils.api_config import *
from app.server.utils.buy_electricity import buy_meter_unit
from app.server.database.crud import get_single_order_transaction
from uuid6 import uuid7

fintava_credentials = FintavaCredentials(api_key=False, is_live=False)

credentials = fintava_credentials.credentials()

fintava = FintavaOperations()

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
            "Account Number": virtual_account['data']['virtualAcctNo'],
            "Bank": virtual_account['data']['bank'],
            "ID": virtual_account['data']['id'],
            "Payment Status": virtual_account['data']['paymentStatus']
         }

         return account_details

   except Exception:
      return {
         "status_code":virtual_account['statusCode'],
         "message": virtual_account['message']
              }

async def verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference):
   '''Verify Payment to virtual account'''
   try:
      get_order_details = await get_single_order_transaction(transaction_reference)

      if transaction_status is "PAID" and get_order_details['transaction_reference'] == transaction_reference:
         # Buy Electricity unit
         
         buy_unit = buy_meter_unit(
            meter_number=get_order_details["user_meter_number"],
            meter_type=get_order_details["meter_type"],
            disco=get_order_details["meter_code"],
            amount=get_order_details["user_amount"]
         )

         if buy_unit["meter_token"]:
            return buy_unit
      
   except Exception:
      return {
         "status_code":buy_unit['statusCode'],
         "message": buy_unit['message']
              }

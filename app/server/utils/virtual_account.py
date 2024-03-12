from app.server.utils.api_config import *
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

# test = create_account("musa", "200")
# print(test)

def verify_payment(response):
   try:
      if response['']:
         pass
      
   except Exception:
      return {
         "status_code":virtual_account['statusCode'],
         "message": virtual_account['message']
              }

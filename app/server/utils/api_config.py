import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL_STAGING = os.environ["BASE_URL_STAGING"]
BASE_URL_LIVE = os.environ["BASE_URL_LIVE"]
FINTAVA_API_KEY_STAGING = os.environ["FINTAVA_API_KEY_STAGING"]
FINTAVA_API_KEY_LIVE = os.environ["FINTAVA_API_KEY_LIVE"]

# API BASE URL CLass
class GetBaseUrlAndApi:
   '''Initiliaze Urls and API keys for testing and production'''

   def __init__(self, url_live, key_live) -> None:
      self.url_live = url_live
      self.key_live = key_live
   def urls(self):
      if self.url_live == True:
         return BASE_URL_LIVE
      elif self.url_live == False:
         return BASE_URL_STAGING
      else:
         return {"message": "Input True or False"}
   
   def keys(self):
      if self.key_live == True:
         return FINTAVA_API_KEY_LIVE
      elif self.key_live == False:
         return FINTAVA_API_KEY_STAGING
      else:
         return {"message": "Input True or False"}


# API Credentials
class FintavaCredentials:
   '''Fintava Credentials for testing and live'''
   def __init__(self, api_key, is_live) -> None:
      self.api_key = api_key
      self.is_live = is_live

   def credentials(self):
      data = (self.api_key, self.is_live)
      return data


# Fintava Functions

class FintavaOperations:
   '''Implementing all the fintava operations like creating account, making transfer etc..'''
   def __init__(self) -> None:
      pass

   # Create Virtual Account
   def create_virtual_account(self, credentials, customer_name, phone, email, expire_time, merchant_reference, description, amount):
      '''Create user virtual account to pay'''
      try:
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()
         
         url = f"{base_url}/virtual-wallet/generate"

         payload = {
            "customerName": customer_name,
            "phone": phone,
            "email": email,
            "expireTimeInMin": int(expire_time),
            "merchantReference": merchant_reference,
            "description": description,
            "amount": float(amount)
         }

         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         raise {"message":str(e)}

   # Get Virtual Account Details
   def get_virtual_account_details(self, credentials, wallet_id):
      '''Get Wallet Details like payment status, and wallet's status (active/disabled).'''
      try:
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()
         
         url = f"{base_url}/virtual-wallet/{wallet_id}"


         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('GET', url, headers=headers)
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         raise {"message":str(e)}
      
   # Refresh Virtual Account
   def refresh_virtual_account(self, credentials, wallet_id):
      try:   
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()
         
         url = f"{base_url}/virtual-wallet/{wallet_id}/refresh"

         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('PATCH', url, headers=headers)
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         return {"message":str(e)}
   
   # Get List of discos
   def get_list_of_discos(self, credentials):
      try:
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()

         # print(base_api_key)
         
         url = f"{base_url}/billing/discos"

         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('GET', url, headers=headers)
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         return {"message":str(e)}
   
   
   # Preview Meter Details
   def preview_meter_details(self, credentials, meter_number, disco, plan_type):
      try:
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()
         
         url = f"{base_url}/billing/preview-meter"

         payload = {
            "planType": f"{plan_type}",
            "meternumber": f"{meter_number}",
            "disco":f"{disco}",
            }

         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         return {"message":str(e)}
      
   # Buy Electricity Units
   def buy_electricity_units(self, credentials, meter_number, disco, plan_type, amount):
      try:
         live_status = credentials[1]
         api_key_status = credentials[0]
         if live_status == True or live_status == False:
            base_url = GetBaseUrlAndApi(live_status, api_key_status).urls()
         
         if api_key_status == True or api_key_status == False:
            base_api_key = GetBaseUrlAndApi(live_status, api_key_status).keys()
         
         url = f"{base_url}/billing/electricity"

         payload = {
            "planType": f"{plan_type}",
            "meternumber": f"{meter_number}",
            "disco":f"{disco}",
            "amount":f"{amount}"
            }

         headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {base_api_key}"
         }  
         
         response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
         response_dict = json.loads(response.text)
         return response_dict
      except Exception as e:
         return {"message":str(e)}
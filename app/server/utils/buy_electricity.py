from app.server.utils.api_config import FintavaCredentials, FintavaOperations

fintava_credentials = FintavaCredentials(api_key=False, is_live=False)

credentials = fintava_credentials.credentials()

fintava = FintavaOperations()

# Get Meter details
def get_meter_details(meter_number, disco, meter_type):
   '''Get meter details'''
   try:
      meter_details = fintava.preview_meter_details(
         credentials=credentials,
         meter_number=meter_number,
         disco=disco,
         plan_type=meter_type
         )
      
      if meter_details['status'] == "00":
         user_meter_details = {
            "meter_name": meter_details["customer"]["name"],
            "meter_address": meter_details["customer"]["address"]
         }
         
         return user_meter_details
   except Exception:
      return {
         "status_code":meter_details['statusCode'],
         "message": meter_details['message']
              }

# Buy Meter Unit
def buy_meter_unit(meter_number, disco, amount, meter_type):
   '''Buy Meter units'''
   try:
      user_meter_unit = fintava.buy_electricity_units(
         credentials=credentials,
         meter_number=meter_number,
         disco=disco,
         plan_type=meter_type,
         amount=amount
      )

      if user_meter_unit["status"] == 200:
         user_meter_unit_details = {
            "meter_token": user_meter_unit["meter_token"],
            "meter_units": user_meter_unit["units"]
         }

         return user_meter_unit_details
   except Exception:
      return {
            "status_code":user_meter_unit['statusCode'],
            "message": user_meter_unit['message']
               }
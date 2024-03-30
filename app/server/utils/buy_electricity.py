from app.server.utils.api_config import FintavaCredentials, FintavaOperations

fintava_credentials = FintavaCredentials(api_key=True, is_live=True)

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
      response = meter_details.get("status", 400)
      if response == "00":
         user_meter_detail = {
            "meter_name": meter_details["customer"]["name"],
            "meter_address": meter_details["customer"]["address"],
            "status":"200"
         }
         return user_meter_detail
      else:
         return {
         "status":str(response),
         "message": "Error Occured!"
              }
         # return {
         #    "meter_name":"Musa Adamu",
         #    "meter_address":"No.5 Beside Bauchi.",
         #    "status": "200"
         # }
   except Exception:
      return {
         "status":meter_details['status'],
         "message": "Error Occured!"
              }

# test = get_meter_details("0150000896855","Jos_Disco","prepaid")
# print(test)

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
      # print(user_meter_unit)
      response_status = user_meter_unit.get("status", 400)
      if response_status == 200:
         user_meter_unit_details = {
            "meter_token": user_meter_unit["data"]["meter_token"],
            "meter_units": user_meter_unit["data"]["units"],
            "status":"200"
         }

         return user_meter_unit_details
      else:
         return {
            "status":str(response_status),
            "message": "Error Occured!"
               }
   except Exception:
      return {
            "status":str(response_status),
            "message": "Error Occured!"
               }
from app.server.utils.api_config import *
from uuid6 import uuid7

fintava_credentials = FintavaCredentials(api_key=False, is_live=False)

credentials = fintava_credentials.credentials()

fintava = FintavaOperations()


print(credentials)

# # Get Meter details
# def get_meter_details():
# return {
#          "status_code":virtual_account['statusCode'],
#          "message": virtual_account['message']
#               }




# test = fintava.get_list_of_discos(
#    credentials=credentials
#    )


# test_meter = fintava.preview_meter_details(
#    credentials=credentials,
#    meter_number="0150000896855",
#    disco="Jos_Disco",
#    plan_type="prepaid"
# )

# print(test_meter)
# print(test)
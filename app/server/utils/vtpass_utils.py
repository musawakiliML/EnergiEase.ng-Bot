""" Utilities for VTPASS Activities """
import os
import pytz
from uuid6 import uuid7
from datetime import datetime
from dotenv import load_dotenv

from app.server.utils.vtpass import VTPASS, VTPASSCredentials

load_dotenv()

api_key = os.environ['VTPASS_API_KEY']
public_key = os.environ['VTPASS_PUBLIC_KEY']
secret_key = os.environ['VTPASS_SECRET_KEY']

vtpass_credentials = VTPASSCredentials(api_key, public_key, secret_key, is_live=False)

credentials = vtpass_credentials.credentials()

vtpass = VTPASS()

def generated_request_id():
    lagos_timezone = pytz.timezone('Africa/Lagos')
    date_time_id = datetime.now(lagos_timezone).strftime('%Y%m%d%H%M')
    reference_id = str(uuid7()).split("-")[4]
    return date_time_id + reference_id

def get_token_units(electricity_response, product):
    try:
        tokens = str(electricity_response["purchased_code"].split(':')[1]).strip()
        if product == "AEDC":
            units = electricity_response['PurchasedUnits']
        elif product == "IKEDC" or product == "EEDC" or product == "BEDC" or product == "PHED" or product == "KEDCO":
            units = electricity_response['units']
        elif product == "EKEDC":
            units = electricity_response['mainTokenUnits']
        elif product == "IBEDCO" or product == "JED":
            units = electricity_response['Units']
        elif product == "KAEDCO":
            units = ""
        return {'tokens': tokens, 'units': units}
    except Exception as e:
        raise Exception({"message":str(e)})
# request_id = generated_request_id()
# test = vtpass.purchase_electricity_unit(
#             request_id,
#             "benin-electric",
#             # chat_payment_reference["user_meter_number"],
#             "1111111111111",
#             "prepaid",
#             1000,
#             "09089786543",
#             credentials
#          )

# print(test)

# test = {'code': '000', 'content': {'transactions': {'status': 'delivered', 'product_name': 'Abuja Electricity Distribution Company- AEDC', 'unique_element': '1111111111111', 'unit_price': 1000, 'quantity': 1, 'service_verification': None, 'channel': 'api', 'commission': 15, 'total_amount': 985, 'discount': None, 'type': 'Electricity Bill', 'email': 'musaadamuw@gmail.com', 'phone': '+2348135810804', 'name': None, 'convinience_fee': 0, 'amount': 1000, 'platform': 'api', 'method': 'api', 'transactionId': '16987845255804385875315820'}}, 'response_description': 'TRANSACTION SUCCESSFUL', 'requestId': '2023103121356eb4fc70052b', 'amount': '1000.00', 'transaction_date': {'date': '2023-10-31 21:35:25.000000', 'timezone_type': 3, 'timezone': 'Africa/Lagos'}, 'purchased_code': 'Token : 3359-3176-5478-0062-9598', 'MeterNumber': '04177505726', 'Token': '3359-3176-5478-0062-9598', 'ReceiptNumber': '7011202109137170448', 'PurchasedUnits': 89.9, 'DebtDescription': None, 'DebtAmount': None, 'RefundUnits': None, 'ServiceChargeVatExcl': None, 'Name': 'DOMINIC Gabriel ', 'Address': 'JABI JABI ABUJA Und St. Vendors Center', 'Reference': 'T21256131638cd89c5bf9b944168837a', 'Vat': 348.84, 'ResponseTime': '9/13/2021 1:16:44 PM', 'TariffRate': '89.9 KWH @ 51.75', 'FreeUnits': None, 'MeterCategory': 'Tariff Band A Non MD'}

# print(str(test["purchased_code"].split(':')[1]).strip())
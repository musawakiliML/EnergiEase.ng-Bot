""" Utilities for VTPASS Activities """
import os
import pytz
import logging
from uuid6 import uuid7
from datetime import datetime
from dotenv import load_dotenv

from app.server.utils.vtpass import VTPASS, VTPASSCredentials

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


load_dotenv()

api_key = os.environ['VTPASS_API_KEY']
public_key = os.environ['VTPASS_PUBLIC_KEY']
secret_key = os.environ['VTPASS_SECRET_KEY']

vtpass_credentials = VTPASSCredentials(
    api_key, public_key, secret_key, is_live=False)

credentials = vtpass_credentials.credentials()

vtpass = VTPASS()

# Generate Reference ID for VTPASS


def generated_request_id():
    lagos_timezone = pytz.timezone('Africa/Lagos')
    date_time_id = datetime.now(lagos_timezone).strftime('%Y%m%d%H%M')
    reference_id = str(uuid7()).split("-")[4]
    return date_time_id + reference_id

# Extract Token From VTPASS Purchase


def get_token_units(electricity_response, product):
    """Get Electricity Token and Units from VTPASS Purchase

    Args:
        electricity_response (dict): VTPASS Response object
        product (str): Distribution Company

    Raises:
        Exception: Any Potential Error

    Returns:
        dict: Token and Units
    """
    try:
        tokens = str(
            electricity_response["purchased_code"].split(':')[1]).strip()
        if product == "AEDC":
            units = electricity_response['PurchasedUnits']
        elif product == "IKEDC" or product == "EEDC" or product == "BEDC" or product == "PHED" or product == "KEDCO" or product == "KAEDCO":
            units = electricity_response['units']
        elif product == "EKEDC":
            units = electricity_response['mainTokenUnits']
        elif product == "IBEDCO" or product == "JED":
            units = electricity_response['Units']
        return {'tokens': tokens, 'units': units}
    except Exception as e:
        raise Exception({"message": str(e)})


def get_meter_details_vtpass(meter_number, disco, meter_type) -> dict:
    """Get Meter Details VTPASS

    Args:
       meter_number (int): User Meter Number
       disco (str): Distribution Company Name
       meter_type (str): Meter Type(Prepaid or Postpaid)

     Returns:
       dict: Meters details dictionary
    """
    try:
        meter_details = vtpass.verify_meter(
            credentials=credentials,
            billers_code=meter_number,
            service_id=disco,
            meter_type=meter_type
        )

        # logger.info(f"{meter_details}")
        response = meter_details.get("code")

        # logger.info(f"{response}")
        if response == "000":
            user_meter_detail = {
                "meter_name": meter_details['content']["Customer_Name"],
                "meter_address": meter_details['content']["Address"],
                "status": "200"
            }
            return user_meter_detail
        else:
            return {
                "status": "400",
                "message": "Error Occured!"
            }
    except Exception as e:
        return {
            "status": "400",
            "message": "Error Occured!",
            "errors": str(e)
        }

# Buy Meter Unit
def buy_meter_unit_vtpass(meter_number, disco, amount, meter_type) -> dict:
    '''Buy Meter units'''
    try:
        request_id = generated_request_id()
        user_meter_unit = vtpass.purchase_electricity_unit(
            credentials=credentials,
            request_id=request_id,
            service_id=disco,
            billers_code=meter_number,
            variation_code=meter_type,
            amount=amount,
            phone="08102778677"
        )
        response_status = user_meter_unit.get("code")
        if response_status == "000":
            if disco == "eko-electric":
                product = "EKEDC"
            elif disco == "ikeja-electric":
                product = "IKEDC"
            elif disco == "kano-electric":
                product = "KEDCO"
            elif disco == "kaduna-electric":
                product = "KAEDCO"
            elif disco == "portharcourt-electric":
                product = "PHED"
            elif disco == "jos-electric":
                product = "JED"
            elif disco == "ibadan-electric":
                product = "IBEDC"
            elif disco == "abuja-electric":
                product = "AEDC"
            elif disco == "enugu-electric":
                product = "EEDC"
            elif disco == "benin-electric":
                product = "BEDC"
            
            token_units = get_token_units(user_meter_unit, product)
            user_meter_unit_details = {
                "meter_token": token_units["tokens"],
                "meter_units": token_units["units"],
                "status": "200"
            }

            return user_meter_unit_details
        else:
            return {
                "status": "400",
                "message": "Error Occured!"
            }
    except Exception as e:
        return {
            "status": str(response_status),
            "message": "Error Occured!",
            "errors": str(e)
        }


# request_id = generated_request_id()

# meter_details = vtpass.verify_meter(
#             credentials=credentials,
#             billers_code="1111111111111",
#             service_id="jos-electric",
#             meter_type="prepaid"
#         )
# print(meter_details)
# test = vtpass.purchase_electricity_unit(
#             request_id,
#             "aba-electric",
#             # chat_payment_reference["user_meter_number"],
#             "1111111111111",
#             "postpaid",
#             1000,
#             "09089786543",
#             credentials
#          )

# print(test)

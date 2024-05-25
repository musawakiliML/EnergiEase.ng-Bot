""" VTPASS Connection for Buying Electricity """
import os
import json
import requests

from dotenv import load_dotenv


load_dotenv()

VTPASS_STAGING_URL = os.environ['VTPASS_URL_STAGING']
VTPASS_LIVE_URL = os.environ['VTPASS_URL_LIVE']

# API Base urls for testing and live production


class GetBaseUrl:
    """ Generate a base URL for accessing information"""

    def __init__(self, live):
        self.live = live

    def urls(self):
        """ Return a Base url either for live or for sandbox tests"""

        if self.live is True:
            return VTPASS_LIVE_URL
        elif self.live is False:
            return VTPASS_STAGING_URL
        else:
            # print(self.live)
            return {
                "message": "Live can either be True or False",
                "status": False
            }

# Functions to Perform operations on VTPASS


class VTPASSCredentials:
    """
       Generates credentials
    """

    def __init__(self, api_key, public_key, secret_key, is_live):
        self.api_key = api_key
        self.public_key = public_key
        self.secret_key = secret_key
        self.is_live = is_live

    def credentials(self):
        """Generates credentials

        Returns:
            tuple: Returns credentials
        """
        data = (self.api_key, self.public_key, self.secret_key, self.is_live)
        return data


class VTPASS:
    """
       Main Class for VTPASS Functions
    """

    def __init__(self) -> None:
        pass

    def get_balance(self, credentials):
        """Get My Wallet Balance

        Args:
            credentials (tuple): My wallet credentials

        Returns:
            dict: Wallet Balance
        """
        try:
            live = credentials[3]
            if live is True or live is False:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/balance"
                payload = {}
                headers = {
                    'api-key': credentials[0],
                    'public-key': credentials[1],
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    'GET', url, headers=headers, data=json.dumps(payload), timeout=60)
                response_dict = json.loads(response.text)
                return response_dict
        except Exception as e:
            return {
                "message": str(e)
            }

    def verify_meter(self, billers_code, service_id, meter_type, credentials):
        """Verifying the meter information

        Args:
            billers_code (int): The meter number you wish to make the bills payment on.
            service_id (int): Disco service ID: ikeja-electric
            meter_type (string): 
            credentials (tuple): _description_

        Returns:
            _type_: _description_
        """
        try:
            live = credentials[3]
            if live is True or live is False:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/merchant-verify"
                payload = {
                    "billersCode": billers_code,
                    "serviceID": service_id,
                    "type": meter_type
                }
                headers = {
                    'api-key': credentials[0],
                    'secret-key': credentials[2],
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    'POST', url, headers=headers, data=json.dumps(payload), timeout=60)

                response_dict = json.loads(response.text)
                return response_dict
        except Exception as e:
            return {
                "message": str(e)
            }

    def purchase_electricity_unit(self, request_id: str,
                                  service_id: str, billers_code: str,
                                  variation_code: str, amount: int,
                                  phone, credentials):
        """Buy Meter Electricity Unit for Given Meter Number

        Args:
            request_id (str): _description_
            service_id (str): _description_
            billers_code (str): _description_
            variation_code (str): _description_
            amount (int): _description_
            phone (_type_): _description_
            credentials (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            live = credentials[3]
            if live is True or live is False:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/pay"
                payload = {
                    "request_id": request_id,
                    "serviceID": service_id,
                    "billersCode": billers_code,
                    "variation_code": variation_code,
                    "amount": amount,
                    "phone": phone
                }
                headers = {
                    'api-key': credentials[0],
                    'secret-key': credentials[2],
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    'POST', url, headers=headers, data=json.dumps(payload), timeout=60)

                response_dict = json.loads(response.text)
                return response_dict
        except Exception as e:
            return {
                "message": str(e)
            }

    def transaction_status(self, request_id, credentials):
        """Get User Transactions Status

        Args:
            request_id (_type_): _description_
            credentials (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            live = credentials[3]
            if live is True or live is False:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/requery"
                payload = {
                    "request_id": request_id
                }
                headers = {
                    'api-key': credentials[0],
                    'secret-key': credentials[2],
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    'POST', url, headers=headers, data=json.dumps(payload), timeout=60)

                response_dict = json.loads(response.text)
                return response_dict
        except Exception as e:
            return {
                "message": str(e)
            }

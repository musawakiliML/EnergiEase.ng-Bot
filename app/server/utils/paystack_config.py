import os
import json
import uuid6
import requests
from dotenv import load_dotenv
from telegram import Credentials

load_dotenv()
paystack_secret_key = os.environ["PAYSTACK_SECRET_KEY"]

# API Base urls for testing and live production


class GetBaseUrl:
    """Get Base URL
    """

    def __init__(self, live):
        self.live = live

    def urls(self):
        if self.live is True:
            return 'https://api.paystack.co'
        else:
            return 'live can either be True or False'


class PaystackCredential:
    def __init__(self, secret_key, is_live):
        self.secretKey = secret_key
        self.is_live = is_live

    def credentials(self):

        data = (self.secretKey, self.is_live)
        return data


class Paystack:

    def __init__(self):
        pass

    def initialize_transaction(self, credentials,
                               amount,
                               customerEmail, paymentReference) -> dict:
        try:
            # live = credentials.is_live
            key = credentials[0]
            live = credentials[1]
            if live == True:
                baseurl = GetBaseUrl(live).urls()
                url = f'{baseurl}/transaction/initialize'

                payload = {
                    "amount": amount,
                    "email": customerEmail,
                    "reference": paymentReference,
                    "currency": "NGN",
                    "channels": ["ussd", "bank_transfer"],
                    # "bankCode": "232"
                }
                headers = {
                    'Content-Type': 'application/json',
                    "Authorization": f"Bearer {key}"
                }

                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload))

                r_dict = json.loads(response.text)
                return r_dict
        except Exception as e:
            return {"message": str(e)}


# testing

Credentials = PaystackCredential(secret_key=paystack_secret_key, is_live=True)
credentials = Credentials.credentials()
paystack = Paystack()
payment_reference = str(uuid6.uuid7())
response = paystack.initialize_transaction(credentials=credentials,
                                           amount="1000",
                                           paymentReference=payment_reference,
                                           customerEmail='johndoe@example.com')
print(response)

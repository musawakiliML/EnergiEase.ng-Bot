import json

import requests

# API Base urls for testing and live production


class GetBaseUrl:
    """Get Base URL"""

    def __init__(self, live):
        self.live = live

    def urls(self):
        if self.live is True:
            return "https://api.paystack.co"
        else:
            return "live can either be True or False"


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

    def create_customer(self, credentials, first_name, last_name, email):
        try:
            key = credentials[0]
            live = credentials[1]
            if live:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/customer"

                payload = {
                    "first_name": first_name,
                    "email": email,
                    "last_name": last_name,
                    #   "phone": "+2348177777779"
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }

                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload)
                )

                r_dict = json.loads(response.text)
                return r_dict
        except Exception as e:
            return {"message": str(e)}

    def create_dedicated_account(self, credentials, customer):
        try:
            key = credentials[0]
            live = credentials[1]
            if live:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/dedicated_account"

                payload = {"customer": customer}
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }

                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload)
                )

                r_dict = json.loads(response.text)
                return r_dict
        except Exception as e:
            return {"message": str(e)}

    def create_transaction(self, credentials, email, amount, payment_reference):
        try:
            key = credentials[0]
            live = credentials[1]
            if live:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/transaction/initialize"

                payload = {
                    "email": email,
                    "amount": amount,
                    "reference": payment_reference,
                    "channels": ["card", "ussd", "bank_transfer"],
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }

                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload)
                )

                r_dict = json.loads(response.text)
                return r_dict
        except Exception as e:
            return {"message": str(e)}

    def create_charge(self, credentials, email, amount, payment_reference):
        try:
            key = credentials[0]
            # print(key)
            live = credentials[1]
            if live:
                baseurl = GetBaseUrl(live).urls()
                url = f"{baseurl}/charge"

                payload = {
                    "email": email,
                    "amount": amount,
                    "reference": payment_reference,
                    "bank_transfer": {"account_expires_at": "2024-06-08T12:10:00Z"},
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }

                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload)
                )

                r_dict = json.loads(response.text)
                return r_dict
        except Exception as e:
            return {"message": str(e)}


# testing

# response = paystack.create_customer(credentials=credentials,
#                                            first_name="John",
#                                            last_name="Doe",
#                                            email='johndoe@example.com',
#                                            )
# response = paystack.create_dedicated_account(credentials=credentials,
#                                              customer="CUS_tz7f618xpo5ymai")

# response = paystack.create_charge(credentials=credentials,
#                                   email='johndoe@example.com',
#                                   amount="100",
#                                   payment_reference=payment_reference
#                                   )

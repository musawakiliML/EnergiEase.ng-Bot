import json
import requests
from requests.auth import HTTPBasicAuth

# API Base urls for testing and live production


class GetBaseUrl:
    def __init__(self, live):
        self.live = live

    def urls(self):
        if self.live is True:
            return 'https://api.monnify.com'
        elif self.live is False:
            return 'https://sandbox.monnify.com'
        else:
            # print(self.live)
            return 'live can either be True or False'


# Function that get all the Monnify Credentials.
# The credential is then use to authenticate all
# the Endpoint for Use

class MonnifyCredential:
    def __init__(self, api_key, secret_key, contract, wallet_account_number, is_live):
        self.apikey = api_key
        self.secretKey = secret_key
        self.contract = contract
        self.walletId = wallet_account_number
        self.is_live = is_live

    def credentials(self):

        data = (self.apikey, self.secretKey,
                self.contract, self.walletId, self.is_live)
        return data

    def get_token(self):
        live = self.is_live
        if live is True or live is False:
            baseurl = GetBaseUrl(live).urls()
            print(baseurl)
            username = self.apikey
            password = self.secretKey
            response = requests.post(f'{baseurl}/api/v1/auth/login',
                                     auth=HTTPBasicAuth(username, password))

            response_dict = json.loads(response.text)

            a = response_dict['responseBody']['accessToken']
            res = 'Bearer {}'
            token = res.format(a)

            self.tokens = token

            d = (self.tokens)
            return d
        else:

            return GetBaseUrl(live).urls()


class Monnify:

    def __init__(self):
        pass

    def one_time_payment(self, credentials,
                         amount, customerName,
                         customerEmail, paymentReference,
                         paymentDescription, redirectUrl,
                         paymentMethods) -> dict:
        # live = credentials.is_live
        live = credentials[4]
        if live == True or live == False:
            baseurl = GetBaseUrl(live).urls()
            url = f'{baseurl}/api/v1/merchant/transactions/init-transaction'
            famount = float(amount)
            payload = {
                "amount": famount,
                "customerName": customerName,
                "customerEmail": customerEmail,
                "paymentReference": paymentReference,
                "paymentDescription": paymentDescription,
                "currencyCode": "NGN",
                "contractCode": credentials[2],
                "redirectUrl": redirectUrl,
                "paymentMethods": paymentMethods
            }
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=HTTPBasicAuth(
                credentials[0], credentials[1]), headers=headers, data=json.dumps(payload))

            r_dict = json.loads(response.text)
            return r_dict
        else:
            return GetBaseUrl(live).urls()

    def pay_with_bank_transfer(self, credentials, transactionReference) -> dict:
        live = credentials[4]
        if live == True or live == False:
            baseurl = GetBaseUrl(live).urls()
            url = f'{baseurl}/api/v1/merchant/bank-transfer/init-payment'
            payload = {
                "transactionReference": transactionReference,
            }
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, auth=HTTPBasicAuth(
                credentials[0], credentials[1]), headers=headers, data=json.dumps(payload))

            r_dict = json.loads(response.text)
            return r_dict
        else:
            return GetBaseUrl(live).urls()

    def get_transaction_status(self, credentials, transactionReference, token) -> dict:
        live = credentials[4]
        if live is True or live is False:
            baseurl = GetBaseUrl(live).urls()
            url = f'{baseurl}/api/v2/transactions/{transactionReference}'
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'Authorization': token
            }

            response = requests.request(
                "GET", url, headers=headers, data=json.dumps(payload))
            r_dict = json.loads(response.text)
            return r_dict
        else:
            return GetBaseUrl(live).urls()

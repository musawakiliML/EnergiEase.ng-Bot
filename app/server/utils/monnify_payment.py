import os
import json
import uuid6

from app.server.utils.monnify_config import MonnifyCredential, Monnify

reserve = Monnify()

api_key = os.environ['MONNIFY_API_KEY']
secret_key = os.environ['MONNIFY_SECRET_KEY']
contractCode = os.environ['MONNIFY_CONTRACT_CODE']
WalletAccountNo = os.environ['MONNIFY_WALLET_ACCOUNT_NO']

merchant_credential = MonnifyCredential(
                                       api_key,
                                       secret_key,
                                       contractCode,
                                       WalletAccountNo,
                                       is_live=False
                                       )

token = merchant_credential.get_token()

def init_transaction(amount: float):

    payment_reference = str(uuid6.uuid7())
    payment_reference = json.dumps(payment_reference, default=str)

    transaction = reserve.one_time_payment(
                                    credentials=merchant_credential.credentials(),
                                    amount=amount,
                                    customerName="EnergiEase Bot Customer",
                                    customerEmail="payment@energieasebot.ng",
                                    paymentReference=payment_reference,
                                    paymentDescription="Electricity Transaction",
                                    redirectUrl="",
                                    paymentMethods=["ACCOUNT_TRANSFER"])

    if transaction['responseMessage'] == "success":
        transactionReference = transaction['responseBody']['transactionReference']
        
        response_data = {
            "transaction_reference": transactionReference,
            "status": "200",
            "message": "Success"
        }
        return response_data
    else:
        response_data = {
            "message": "Failed",
            "status": "400"
        }
        return response_data


def init_bank_transfer(transactionReference: str):

    bank_transfer = reserve.pay_with_bank_transfer(
        credentials=merchant_credential.credentials(), transactionReference=transactionReference)
    if bank_transfer['responseMessage'] == "success":
        bank_details = {
            "Account Number": bank_transfer['responseBody']['accountNumber'],
            "Account Name": bank_transfer['responseBody']['accountName'],
            "Bank Name": bank_transfer['responseBody']['bankName'],
            "Amount": bank_transfer['responseBody']['amount'],
            "status":"200",
            "message":"Success"
        }
        return bank_details
    else:
        print(bank_transfer)
        response_data = {
            "message": "Failed",
            "status": "400"
        }
        return response_data

# test = init_transaction(1000.0)
# print(test)

# tes = init_bank_transfer(test['transaction_reference'])
# print(tes)

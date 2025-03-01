import os
import uuid6
from app.server.utils import paystack_config
from dotenv import load_dotenv

load_dotenv()
paystack_secret_key = os.environ["PAYSTACK_SECRET_KEY_LIVE"]

# Initialize Paystack

Credentials = paystack_config.PaystackCredential(secret_key=paystack_secret_key, is_live=True)
credentials = Credentials.credentials()
paystack = paystack_config.Paystack()
# payment_reference = str(uuid6.uuid7())

# Create transaction url for paystack transaction
def create_transaction_url(amount,
   payment_reference,
   credentials=credentials,
   email="payment@energiease.ng",
   ):
   try:
      response = paystack.create_transaction(credentials=credentials,
                                                email=email,
                                                amount=amount,
                                                payment_reference=payment_reference
                                                )
      status = response.get("status", False)
      if status == True:
         data = {
            "status":"200",
            "transaction_url": response['data']['authorization_url']
         }
         return data
      else:
         return {
                "status": 400,
                "message": "Error has occured!!"
            }
   except Exception as e:
      return {
                "status": 400,
                "message": "Error has occured!!"
            }

# test = create_transaction_url(amount="10000", payment_reference=payment_reference)

# print(test)
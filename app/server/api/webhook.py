# Webhook For Transaction Nofication
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

import json
import logging

from app.server.utils.virtual_account import verify_payment

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def process_webhook(request: Request):
   
   try:
      
      request_body = await request.json()
      
      if request_body:
      
         transaction_details = request_body

      logger.info(request_body)
   # data: {
   #    userId: 'bf61c3cf-4894-4a01-91b1-e4c5e2fa2b08',
   #    amount: '100.00',
   #    reference: '000014231211154211281900319598',
   #    sessionID: '000914231311144221237185422093',
   #    channelCode: '3',
   #    status: 'success',
   #    accountName: 'john doe',
   #    accountNumber: '0865231291',
   #    BankVerificationCode: '22000000039'
   # }
   # }
      # if transaction_details['event'] == "account_funded":
      #    pass
            # transaction_reference = transaction_details['eventData']['transactionReference']
            # transaction_status = transaction_details['eventData']['paymentStatus']

            # await verify_payment(transaction_reference, transaction_status)

         # elif transaction_details['event'] != "account_funded":
         #    transaction_reference = transaction_details['eventData']['transactionReference']
         #    transaction_status = "FAILED"

         #    await verify_payment(transaction_reference, transaction_status)

      return JSONResponse(
            content={"status": "success", "message": "Webhook received successfully"},
            status_code=status.HTTP_200_OK,
         )
          
   except Exception:
      return {
         "status_code":request_body['statusCode'],
         "message":request_body['message']
      }

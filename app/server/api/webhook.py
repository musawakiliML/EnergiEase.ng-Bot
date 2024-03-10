# Webhook For Transaction Nofication
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

import json

from app.server.utils.virtual_account import verify_payment

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def process_webhook(request: Request):
   request_body = await request.json()
   
   if request_body:
      """If payload verification is successful, you can perform your necessary task, but if your planned processing would take time, you should first return a 200 response and process your stuff in background."""
        
      # transaction_details = json.loads(payload_in_bytes)
      transaction_details = request_body
      #print(json.loads(payload_in_bytes))

      if transaction_details['eventType'] == "SUCCESSFUL_TRANSACTION":
         transaction_reference = transaction_details['eventData']['transactionReference']
         transaction_status = transaction_details['eventData']['paymentStatus']

         await verify_payment(transaction_reference, transaction_status)
      elif transaction_details['eventType'] == "REJECTED_PAYMENT":
         transaction_reference = transaction_details['eventData']['transactionReference']
         transaction_status = "FAILED"
         await verify_payment(transaction_reference, transaction_status)

      return JSONResponse(
         content={"status": "success", "msg": "Webhook received successfully"},
         status_code=status.HTTP_200_OK,
         )
import json
import logging

# Webhook For Transaction Nofication
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.server.utils.virtual_account import verify_payment_buy_unit

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
   '''Webhook '''
   try:
      
      request_body = await request.json()

      if request_body:
         transaction_details = request_body

      # logger.info(request_body)
      
      # Check Transaction Details
      if transaction_details['status'] is "PAID" and transaction_details['paymentStatus'] is "PAID":
         transaction_reference = transaction_details['merchantReference']
         transaction_status = transaction_details['paymentStatus']
         transaction_id = transaction_details['id']

         await verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference)

      elif transaction_details['paymentStatus'] == "UNDERPAID":
         transaction_id = transaction_details['id']
         transaction_reference = transaction_details['merchantReference']
         transaction_status = transaction_details['paymentStatus']

         await verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference)
      
      return JSONResponse(
            content={"status": "success", "message": "Webhook received successfully"},
            status_code=status.HTTP_200_OK,
         )
          
   except Exception:
      return {
         "status_code":request_body['statusCode'],
         "message":request_body['message']
      }

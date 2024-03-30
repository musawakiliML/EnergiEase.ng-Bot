import logging

# Webhook For Transaction Nofication
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.server.database.crud import update_user_order_transaction
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
   '''Webhook for virtual account funding'''
   try:
      
      request_body = await request.json()

      if request_body['event'] == "VIRTUAL_WALLET_PAYMENT":
         transaction_details = request_body

         # logger.info(request_body)
         
         # Check Transaction Details
         if transaction_details['data']['status'] == "PAID" and transaction_details['data']['paymentStatus'] == "PAID":
            transaction_reference = transaction_details['data']['merchantReference']
            transaction_status = transaction_details['data']['paymentStatus']
            transaction_id = transaction_details['data']['id']
            
            user_order_data = ["payment_confirmation", transaction_status]

            await update_user_order_transaction(user_order_data, transaction_id)
            await update_user_order_transaction(["transaction_reference", transaction_reference], transaction_id)

            await verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference)

         elif transaction_details['data']['paymentStatus'] == "UNDERPAID":
            transaction_id = transaction_details['data']['id']
            transaction_reference = transaction_details['data']['merchantReference']
            transaction_status = transaction_details['data']['paymentStatus']

            await verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference)
      
      return JSONResponse(
            content={"status": "success", "message": "Webhook received successfully"},
            status_code=status.HTTP_200_OK,
         )
   except Exception:
      return {
         "status":request_body['data']['status'],
         "message":request_body['data']['message']
      }

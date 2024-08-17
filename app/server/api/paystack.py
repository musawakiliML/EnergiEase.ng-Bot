import logging

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from app.server.utils.virtual_account import verify_payment_buy_unit
from app.server.database.crud import update_user_order_transaction

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_description="Paystack Payment Webhook")
async def paystack_webhook(request: Request):
   try:
      request_body = await request.json()
      
      print(request_body)
      
      if request_body['event'] == "charge.success":
         transaction_reference = request_body['data']['reference']
         transaction_status = request_body['data']['status']
         transaction_amount = request_body['data']['amount']
         
         # Implement payment verification for paystack
         if transaction_status == "success":
            # verify transaction amount
            reference = transaction_reference.split("-")[4]
            user_order_data = ["payment_confirmation", "PAID"]
            await update_user_order_transaction(user_order_data, transaction_reference)
            
            await update_user_order_transaction(["transaction_reference", reference], transaction_reference)

            await verify_payment_buy_unit(transaction_id=transaction_reference,
                                          transaction_status="PAID",
                                          transaction_reference=reference,
                                          payment_platform="Paystack",
                                          amount_paid=transaction_amount)
         else:
            transaction_reference = request_body['data']['reference']
            transaction_status = request_body['data']['status']
            reference = transaction_reference.split("-")[4]
            
            await verify_payment_buy_unit(transaction_id=transaction_reference,
                                          transaction_status="FAILED",
                                          transaction_reference=reference,
                                          payment_platform="Paystack",
                                          amount_paid=transaction_amount)
            
      response_body = {
         "message":"Webhook Received Successfully",
         "status": status.HTTP_200_OK
      }
      return JSONResponse(
         content=response_body,
         status_code=status.HTTP_200_OK
      )
      
   except Exception as e:
      response_body = {
         "message":"Error Processing Webhook",
         "status": status.HTTP_400_BAD_REQUEST
      }
      return JSONResponse(
         content=response_body,
         status_code=status.HTTP_400_BAD_REQUEST
      )

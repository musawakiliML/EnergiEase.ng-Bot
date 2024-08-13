import logging
import hashlib
import json
import hmac
import os

from app.server.utils.virtual_account import verify_payment_buy_unit
from app.server.database.crud import update_user_order_transaction
# Webhook For Transaction Nofication
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

router = APIRouter()

monnify_secret_key = os.environ['MONNIFY_SECRET_KEY']
monnify_ip = os.environ['MONNIFY_IP']

# ============ Monnify Webhook ================================


def verify_hash(payload_in_bytes, monnify_hash):
    """
    Recieves the monnify payload in bytes and perform a SHA-512 hash
    with your secret key which is also encoded in byte.
    uses hmac.compare_digest rather than "=" sign as the former helps
    to prevent timing attacks.
    """
    secret_key_bytes = monnify_secret_key.encode(
        "utf-8"
    )  # encodes your secret key as byte
    your_hash_in_bytes = hmac.new(
        secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
    )
    your_hash_in_hex = your_hash_in_bytes.hexdigest()  # Hexlify generated hash
    return hmac.compare_digest(your_hash_in_hex, monnify_hash)


def get_sender_ip(headers):
    """
    Get senders' IP address, by first checking if your API server
    is behind a proxy by checking for HTTP_X_FORWARDED_FOR
    if not gets sender actual IP address using REMOTE_ADDR
    """

    x_forwarded_for = headers.get("x-forwarded-for")
    if x_forwarded_for:
        # in some cases this might be in the second index ie [1]
        # depending on your hosting environment
        return x_forwarded_for.split(",")[0]
    else:
        return headers.get("remote-addr")


def verify_monnify_webhook(payload_in_bytes, monnify_hash, headers):
    """
    The interface that does the verification by calling necessary functions.
    Though everything has been tested to work well, but if you have issues
    with this function returning False, you can remove the get_sender_ip
    function to be sure that the verify_hash is working, then you can check
    what header contains the IP address.
    """

    return get_sender_ip(headers) == monnify_ip and verify_hash(
        payload_in_bytes, monnify_hash
    )


# @router.post("/", status_code=status.HTTP_200_OK)
# async def process_webhook(request: Request):
#     """
#     A function based view implementing the receipt of the webhook payload.
#     The webhook payload should be received as bytes rather than json
#     that would be converted to bytes.This is most likely one of the
#     cause for failed webhook verification.
#     After the webhook verification, you can get a json format of the byte
#     object by simply calling json.loads(payload_in_bytes)
#     """

#     payload_in_bytes = await request.body()
#     monnify_hash = request.headers["monnify-signature"]
#     confirmation = verify_monnify_webhook(
#         payload_in_bytes, monnify_hash, request.headers)
#     request_body = await request.json()


#     logger.info(request_body)
#     if request_body:
#         """
#         if payload verification is successful, you can perform your necessary task, but if your planned processing would take time, you should first return a 200 response and process your stuff in background.
#         """

#         transaction_details = request_body

#         if transaction_details['eventType'] == "SUCCESSFUL_TRANSACTION":
#             transaction_reference = transaction_details['eventData']['transactionReference']
#             transaction_status = transaction_details['eventData']['paymentStatus']

#             user_order_data = ["payment_confirmation", transaction_status]

#             await update_user_order_transaction(user_order_data, transaction_reference)
#             await update_user_order_transaction(["transaction_reference", transaction_reference], transaction_reference)
#             logger.info("Passed Request")
#             await verify_payment_buy_unit(transaction_status, transaction_reference)

#         elif transaction_details['eventType'] == "REJECTED_PAYMENT":
#             transaction_reference = transaction_details['eventData']['transactionReference']
#             transaction_status = "FAILED"

#             await verify_payment_buy_unit(transaction_status, transaction_reference)

#         return JSONResponse(
#             content={"status": "success", "msg": "Webhook received successfully"}, status_code=status.HTTP_200_OK)

@router.post("/", status_code=status.HTTP_200_OK)
async def process_webhook(request: Request):
    '''Webhook for virtual account funding'''
    try:

        request_body = await request.json()

        if request_body['event'] == "VIRTUAL_WALLET_PAYMENT":
            transaction_details = request_body

            logger.info(request_body)
            

            # Check Transaction Details
            if transaction_details['data']['status'] == "PAID": #and transaction_details['data']['paymentStatus'] == "PAID":
                transaction_reference = transaction_details['data']['merchantReference']
                transaction_status = transaction_details['data']['status'] #['paymentStatus']
                transaction_id = transaction_details['data']['id']

                user_order_data = ["payment_confirmation", transaction_status]

                await update_user_order_transaction(user_order_data, transaction_id)
                await update_user_order_transaction(["transaction_reference", transaction_reference], transaction_id)

                await verify_payment_buy_unit(transaction_id,
                                              transaction_status,
                                              transaction_reference)

            else:
                transaction_id = transaction_details['data']['id']
                transaction_reference = transaction_details['data']['merchantReference']
                transaction_status = transaction_details['data']['status']

                await verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference)

        return JSONResponse(
            content={"status": "success",
                     "message": "Webhook received successfully"},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        return {
            "status": request_body['data']['status'],
            "message": request_body['data']['message']
        }

# import hashlib
# import hmac
# import os

# from cryptography.hazmat.primitives import serialization
# from fastapi import APIRouter, Header, HTTPException, Request
# from fastapi.responses import PlainTextResponse

# from app.server.utils.whatsappflowsutils import decrypt_request, encrypt_response

# # from encryption import decrypt_request, encrypt_response, FlowEndpointException
# # from flow import get_next_screen


# router = APIRouter()

# # Load the private key string
# APP_SECRET = os.getenv("APP_SECRET")
# PRIVATE_KEY = os.getenv("PRIVATE_KEY")
# PASSPHRASE = os.getenv("PASSPHRASE", "")

# # Recieve Data from Whatsapp Flow


# @router.post("/data")
# async def recieve_data(request: Request):
#     try:
#         # Parse the request body
#         body = await request.json()

#         # Read the request fields
#         encrypted_flow_data_b64 = body["encrypted_flow_data"]
#         encrypted_aes_key_b64 = body["encrypted_aes_key"]
#         initial_vector_b64 = body["initial_vector"]

#         decrypted_data, aes_key, iv = decrypt_request(
#             encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64
#         )
#         # print(decrypted_data)

#         # Return the next screen & data to the client
#         response = {"screen": "QUESTION_ONE", "data": {"some_key": "some_value"}}

#         # Return the response as plaintext
#         encrypted_response = encrypt_response(response, aes_key, iv)
#         print("passed!!")
#         return PlainTextResponse(content=encrypted_response, media_type="text/plain")
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Internal Server Error!")


# if not PRIVATE_KEY:
#     raise ValueError(
#         'Private key is empty. Please check your environment variable "PRIVATE_KEY".'
#     )

# private_key = serialization.load_pem_private_key(
#     PRIVATE_KEY.encode(), password=PASSPHRASE.encode() if PASSPHRASE else None
# )


# def is_request_signature_valid(raw_body: bytes, signature_header: str) -> bool:
#     if not APP_SECRET:
#         print("Warning: App Secret is not set up. Request validation skipped.")
#         return True

#     try:
#         signature = bytes.fromhex(signature_header.replace("sha256=", ""))
#         digest = hmac.new(APP_SECRET.encode(), raw_body, hashlib.sha256).digest()
#         if not hmac.compare_digest(digest, signature):
#             print("Error: Request signature did not match")
#             return False
#         return True
#     except Exception as e:
#         print(f"Error validating signature: {e}")
#         return False


# @router.post("/flow")
# async def root(request: Request, x_hub_signature_256: str = Header(...)):

#     raw_body = await request.body()

#     if not is_request_signature_valid(raw_body, x_hub_signature_256):
#         raise HTTPException(status_code=432, detail="Invalid request signature")

#     try:
#         decrypted_request = decrypt_request(raw_body, private_key)
#         aes_key_buffer = decrypted_request["aesKeyBuffer"]
#         initial_vector_buffer = decrypted_request["initialVectorBuffer"]
#         decrypted_body = decrypted_request["decryptedBody"]

#         print("\ud83d\udcac Decrypted Request:", decrypted_body)

#         # Optional flow token validation
#         # if not is_valid_flow_token(decrypted_body.get("flow_token")):
#         #     error_response = {"error_msg": "The message is no longer available"}
#         #     return PlainTextResponse(
#         #         content=encrypt_response(error_response, aes_key_buffer, initial_vector_buffer),
#         #         status_code=427
#         #     )

#         screen_response = await get_next_screen(decrypted_body)
#         print("\u261b Response to Encrypt:", screen_response)

#         return PlainTextResponse(
#             content=encrypt_response(
#                 screen_response, aes_key_buffer, initial_vector_buffer
#             ),
#             media_type="text/plain",
#         )
#     except FlowEndpointException as e:
#         print(e)
#         raise HTTPException(status_code=e.status_code)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# # # {
# # #     "version": "<VERSION>",
# # #     "action": "<ACTION_NAME>",
# # #     "screen": "<SCREEN_NAME>",
# # #     "data": {
# # #       "prop_1": "value_1",
# # #        …
# # #       "prop_n": "value_n"
# # #     },
# # #    "flow_token": "<FLOW-TOKEN>"
# # # }


# # # {
# # #     "screen": "<SCREEN_NAME>",
# # #     "data": {
# # #       "property_1": "value_1",
# # #        ...
# # #       "property_n": "value_n",
# # #       "error_message": "<ERROR-MESSAGE>"
# # #     }
# # # }

# # # {
# # #   "messages": [{
# # #     "context": {
# # #       "from": "16315558151",
# # #       "id": "gBGGEiRVVgBPAgm7FUgc73noXjo"
# # #     },
# # #     "from": "<USER_ACCOUNT_NUMBER>",
# # #     "id": "<MESSAGE_ID>",
# # #     "type": "interactive",
# # #     "interactive": {
# # #       "type": "nfm_reply",
# # #       "nfm_reply": {
# # #         "name": "flow",
# # #         "body": "Sent",
# # #         "response_json": "{\"flow_token\": \"<FLOW_TOKEN>\", \"optional_param1\": \"<value1>\", \"optional_param2\": \"<value2>\"}"
# # #       }
# # #     },
# # #     "timestamp": "<MESSAGE_SEND_TIMESTAMP>"
# # #   }]
# # # }

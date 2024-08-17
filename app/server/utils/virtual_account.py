import os
from uuid6 import uuid7
from telegram import Bot
from dotenv import load_dotenv

from app.server.utils.api_config import *
from app.server.utils.vtpass_utils import buy_meter_unit_vtpass
from app.server.database.crud import (get_single_order_transaction,
                                      update_user_order,
                                      update_user_order_transaction)

from app.server.bot.message import (
    order_confirmation_message,
    order_failed,
    order_successful
)
# from app.server.utils.monnify_payment import (
#     init_bank_transfer,
#     init_transaction
# )

fintava_credentials = FintavaCredentials(api_key=True, is_live=True)

credentials = fintava_credentials.credentials()

fintava = FintavaOperations()

# Enable Bot Token
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_API"]

# Creating virtual account
def create_account(name: str, amount: str) -> dict:
    """Create Virtual Accounts"""
    try:
        virtual_account = fintava.create_virtual_account(
            credentials=credentials,
            customer_name=name,
            phone="+2348135810804",
            email="musaadamuw@gmail.com",
            expire_time=30,
            merchant_reference=str(uuid7()).split("-")[4],
            description="Electricity Purchase",
            amount=amount,
        )
        # print(virtual_account)
        status = virtual_account.get("status", 400)
        if status == 200:
            account_details = {
                "Account Name": virtual_account['data']['virtualAcctName'],
                "Merchant Ref": virtual_account['data']['merchantReference'],
                "Account Number": virtual_account['data']['virtualAcctNo'],
                "Bank": virtual_account['data']['bank'],
                "ID": virtual_account['data']['id'],
                "Payment Status": virtual_account['data']['paymentStatus'],
                "status": "200"
            }

            return account_details
        else:
            return {
                "status": 400,
                "message": "Error has occured!!"
            }
            

    except Exception:
        return {
            "status": virtual_account['status'],
            "message": virtual_account['message']
        }


async def verify_payment_buy_unit(transaction_id, transaction_status, transaction_reference):
    '''Verify Payment to virtual account'''
    try:
        get_order_details = await get_single_order_transaction(transaction_reference)
        order_id = get_order_details["_id"]

        # Creating a Bot Instance to send Order confirmation and Unit Token
        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        if transaction_status == "PAID" and get_order_details['transaction_id'] == transaction_id:

            # Send Order Confirmation Message
            user_id = get_order_details['user_profile']['user_id'] # type: ignore

            await bot.send_message(chat_id=user_id, text=order_confirmation_message(order_id=order_id)) # type: ignore

            # Buy Electricity unit
            # buy_unit = buy_meter_unit_vtpass(
            #     meter_number=get_order_details["user_meter_number"],
            #     meter_type=get_order_details["meter_type"],
            #     disco=get_order_details["meter_code"],
            #     amount=get_order_details["user_amount"]
            # )
            
            buy_unit = {
                "status": "200",
                "meter_token": "3032-1376-7369-2456-1296",
                "meter_units": "16.2"
            }
            
            
            if buy_unit["status"] == "200":

                # Get Order details
                meter_token = buy_unit['meter_token']
                meter_unit = buy_unit['meter_units']

                # Send Order Confirmation Message for buying units
                user_id = get_order_details['user_profile']['user_id'] # type: ignore

                await bot.send_message(chat_id=user_id, text=order_successful( # type: ignore
                    meter_number=get_order_details["user_meter_number"],
                    meter_unit=meter_unit,
                    meter_token=meter_token
                )
                )
                # Update Database
                token_data = ["token", meter_token]
                unit_data = ["units", meter_unit]
                unit_confirmation = ["unit_confirmation", "SUCCESSFUL"]
                order_status = ["order_status", "COMPLETED"]
                # transaction_id = transaction_reference
                await update_user_order_transaction(token_data, transaction_id)
                await update_user_order_transaction(unit_data, transaction_id)
                await update_user_order_transaction(unit_confirmation, transaction_id)
                await update_user_order_transaction(order_status, transaction_id)
                return buy_unit
            else:
                # Send Order Failed Message
                user_id = get_order_details['user_profile']['user_id'] # type: ignore

                await bot.send_message(chat_id=user_id, text=order_failed( # type: ignore
                    order_id=order_id
                )
                )
                
                # Update Database
                unit_confirmation = ["unit_confirmation", "FAILED"]
                order_status = ["order_status", "FAILED"]
                
                transaction_id = transaction_reference
                await update_user_order_transaction(unit_confirmation, transaction_id)
                await update_user_order_transaction(order_status, transaction_id)
                
                return {
                    "status": "400",
                    "message": "Error Occured!"
                }
        else:
            # Send Order Failed Message
            user_id = get_order_details['user_profile']['user_id'] # type: ignore

            await bot.send_message(chat_id=user_id, text=order_failed( # type: ignore
                order_id=order_id
            )
            )
            
            # Update Database
            unit_confirmation = ["unit_confirmation", "FAILED"]
            order_status = ["order_status", "FAILED"]
            
            transaction_id = transaction_reference
            await update_user_order_transaction(unit_confirmation, transaction_id)
            await update_user_order_transaction(order_status, transaction_id)
            
            return {
                "status": "400",
                "message": "Error Occured!"
            }
                
    except Exception:
        return {
            "status": "400",
            "message": "Error Occured!"
        }

# test = create_account(name="Musa", amount="100")
# print(test)

# def create_account_monnify(amount: str) -> dict:
#     """Create Virtual Accounts"""
#     try:
#         transaction_reference = init_transaction(int(amount))
#         if transaction_reference['status'] == "200":
#             virtual_account_details = init_bank_transfer(
#                 transaction_reference['transaction_reference'])
#         if virtual_account_details['status'] == "200":
#             account_details = {
#                 "Account Name": virtual_account_details["Account Name"],
#                 "Account Number": virtual_account_details['Account Number'],
#                 "Bank": virtual_account_details['Bank Name'],
#                 "ID": transaction_reference['transaction_reference'],
#                 "Payment Status": "NOT PAID",
#                 "Status": "200"
#             }

#             return account_details

#     except Exception:
#         return {
#             "Status": "400",
#             "message": "Failed"
#         }
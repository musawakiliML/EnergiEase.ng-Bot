import os
from typing import Annotated
from telegram import Bot
from dotenv import load_dotenv
from collections import Counter

from fastapi import APIRouter, status, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from app.server.database.crud import (
    get_user_profile_by_id,
    get_all_user_profile,
    get_all_orders,
    get_single_order_by_id,
    get_all_users_order,
    update_user_order_transaction
)

from app.server.auth.auth import authenticate
from app.server.utils.vtpass_utils import buy_meter_unit_vtpass


# Enable Bot Token
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_API"]


# Initialize Router
router = APIRouter()

# User Profile Views

# Get All User Profiles


@router.get('/user_profiles', status_code=status.HTTP_200_OK, response_description="Get All User Profiles")
async def get_user_profile(user: str = Depends(authenticate)):
    try:
        # Get User Profile from DB
        user_profile_data = await get_all_user_profile()
        if user_profile_data.get('message') == 'Successful':
            return_dict = {
                "message": "User Profiles Fetch Successfully",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(user_profile_data.get('data'))
            }

            return JSONResponse(content=return_dict, status_code=status.HTTP_200_OK)

    except Exception as e:
        response = {
            "message": "User Profiles Not Found",
            "status": status.HTTP_404_NOT_FOUND
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)


# Get Single User Profile

@router.get('/user_profile/{id}', status_code=status.HTTP_200_OK, response_description="Get Single User Profile")
async def get_single_user_profile(id: str, user: str = Depends(authenticate)):
    try:
        user_profile = await get_user_profile_by_id(id)
        if user_profile.get("message") == "Successful":
            response = {
                "message": "User Successfully Retrieved",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(user_profile.get("data"))
            }

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "message": "User Profile not found",
            "status": status.HTTP_404_NOT_FOUND
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)


# User Order Views

# Get All Orders


@router.get('/user_orders', status_code=status.HTTP_200_OK, response_description="Get All User Orders")
async def get_all_orders_view(user: str = Depends(authenticate)):

    try:
        # Get All Orders
        user_orders = await get_all_orders()

        if user_orders.get("message") == "Successful":

            response = {
                "message": "All Successfuly Orders Retrieved",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(user_orders.get("data"))
            }

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "message": "User Orders Not Found",
            "status": status.HTTP_404_NOT_FOUND
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)

# Get Single Order


@router.get('/user_orders/{id}', status_code=status.HTTP_200_OK, response_description="Get Single Order")
async def get_single_order_view(id: str, user: str = Depends(authenticate)):
    try:
        user_order = await get_single_order_by_id(id)
        if user_order.get("message") == "Successful":

            return_dict = {
                "message": "User Order Successfully Retrieved",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(user_order.get('data'))
            }

            return JSONResponse(content=return_dict, status_code=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "message": "User Order Not Found",
            "status": status.HTTP_404_NOT_FOUND
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)


# Get User Based Order

@router.get("/user_order/{id}", response_description="Get All User Orders")
async def get_user_order(id: str, user: str = Depends(authenticate)) -> JSONResponse:  # type: ignore
    try:
        # Get User Orders
        user_orders = await get_all_users_order(id)

        if user_orders.get("message") == "Successful":
            orders = []
            order_list = user_orders['data']

            for order in order_list:

                order_dict = {
                    "_id": order['_id'],
                    "session_id": order['session_id'],
                    "meter_distribution": order['meter_distribution'],
                    "user_meter_number": order['user_meter_number'],
                    "meter_owner": order['meter_owner'],
                    "meter_address": order['meter_address'],
                    "user_amount": order['user_amount'],
                    "meter_type": order['meter_type'],
                    "meter_code": order['meter_code'],
                    "token": order['token'],
                    "units": order['units'],
                    "payment_confirmation": order['payment_confirmation'],
                    "unit_confirmation": order['unit_confirmation'],
                    "transaction_id": order['transaction_id'],
                    "transaction_reference": order['transaction_reference'],
                    "order_status": order['order_status'],
                    "created_at": order['created_at']
                }
                orders.append(order_dict)

            response = {
                "message": "User Orders Successfuly Fetched",
                "status": status.HTTP_200_OK,
                "data": jsonable_encoder(orders)
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:

        response = {
            "message": "User Orders Not Found",
            "status": status.HTTP_404_NOT_FOUND,
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)


# ======================= User Dashboard Analytics =====================================

@router.get("/analytics", response_description="Dashboard Analytics")
async def dashboard_analytics(user: str = Depends(authenticate)):
    try:
        # Get all orders
        get_order_details = await get_all_orders()
        get_all_user_profiles = await get_all_user_profile()

        if get_order_details.get("message") == "Successful":
            order_details = get_order_details['data']

            total_amount_of_units_purchased = 0
            total_number_of_units_purchased = 0
            meter_counter = Counter()
            user_counter = Counter()
            distribution = Counter()
            most_purchasing_meter = ""
            most_purchasing_user = ""
            successful_payments = 0
            successful_orders = 0
            successful_units = 0
            failed_payments = 0
            failed_orders = 0
            failed_units = 0
            not_completed_payments = 0
            not_completed_orders = 0
            not_completed_units = 0
            total_number_of_user_profiles = 0
            distro_success_counter = Counter()
            distro_failed_counter = Counter()
            distro_not_completed_counter = Counter()

            # Analytics Calculations
            for order in order_details:
                # Total Amount Of Units Purchased
                if order["user_amount"] and order['payment_confirmation'] == "PAID":
                    total_amount_of_units_purchased += order["user_amount"]

                # Total Number of Units Purchased
                if order['payment_confirmation'] == "PAID" and order["unit_confirmation"] == "SUCCESSFUL":
                    total_number_of_units_purchased += float(order['units'])

                # Most Purchasing Meter (Top 3)
                if order['user_meter_number'] and order["unit_confirmation"] == "SUCCESSFUL":
                    meter_counter[order['user_meter_number']] += 1
                    distribution[order['meter_distribution']] += 1

                # Most Purchasing User (Top 3)
                if order['user_profile']['full_name'] and order["unit_confirmation"] == "SUCCESSFUL":
                    user_counter[order['user_profile']['full_name']] += 1

                # Successful/Failed/Not Completed Payment
                if order['payment_confirmation'] == "PAID":
                    successful_payments += 1
                elif order["payment_confirmation"] == "NO_PAYMENT":
                    failed_payments += 1
                else:
                    not_completed_payments += 1

                # Successful/Failed/Not Completed Unit and distro
                if order['unit_confirmation'] == "SUCCESSFUL":
                    successful_units += 1
                elif order['unit_confirmation'] == "FAILED":
                    failed_units += 1
                else:
                    not_completed_units += 1

                # Sucessful/Failed/Not Completed Order
                if order['order_status'] == "COMPLETED":
                    successful_orders += 1
                elif order['order_status'] == "FAILED":
                    failed_orders += 1
                else:
                    not_completed_orders += 1

                # Successful/Failed/Not Completed distribution summary
                if order['meter_distribution'] and order['unit_confirmation'] == "SUCCESSFUL":
                    distro_success_counter[order['meter_distribution']] += 1
                elif order['unit_confirmation'] == "FAILED":
                    distro_failed_counter[order['meter_distribution']] += 1
                else:
                    distro_not_completed_counter[order['meter_distribution']] += 1

            # Most Purchased Distribution (Top 3)
            most_purchased_distribution = distribution.most_common(3)

            most_purchasing_meter = meter_counter.most_common(3)

            most_purchasing_user = user_counter.most_common(3)

            most_purchasing_distribution_list = []
            # Total Number of Orders Receive
            total_orders_recieved = successful_orders + failed_orders + not_completed_orders

            # Total Number of User Profiles
            total_number_of_user_profiles = len(get_all_user_profiles['data'])

            # Most Purchasing Meters Top (3)
            most_purchasing_meter_list = []

            # Most Purchasing User Top (3)
            most_purchasing_user_list = []

            for i in range(3):
                most_purchasing_meter_list.append(
                    {
                        "meter": most_purchasing_meter[i][0],
                        "number": most_purchasing_meter[i][1]
                    })
                most_purchasing_user_list.append(
                    {
                        "user": most_purchasing_user[i][0],
                        "number": most_purchasing_user[i][1]
                    }
                )

                most_purchasing_distribution_list.append(
                    {
                        "name": most_purchased_distribution[i][0],
                        "number": most_purchased_distribution[i][1]
                    }
                )

            # All distributions order summary
            all_distribution_order_summary = distribution.items()

            # All Meter Order Summary
            all_meter_order_summary = meter_counter.items()

            # Numbers For Each Distro of Successful/Failed/Not Completed
            all_distribution_success_failed_summary = {
                "Successful": distro_success_counter,
                "Failed": distro_failed_counter,
                "Not Completed": distro_not_completed_counter
            }

        response = {
            "message": "Successfully Generated Analytics",
            "status": status.HTTP_200_OK,
            "data": {
                "total_amount_of_units_purchased": total_amount_of_units_purchased,
                "total_number_of_units_purchased": total_number_of_units_purchased,
                "most_purchasing_meters": most_purchasing_meter_list,
                "most_purchasing_users": most_purchasing_user_list,
                "payment_summary": {
                    "successful": successful_payments,
                    "failed": failed_payments,
                    "not_completed": not_completed_payments
                },
                "unit_summary": {
                    "successful": successful_units,
                    "failed": failed_units,
                    "not_completed": not_completed_units
                },
                "orders_summary": {
                    "successful": successful_orders,
                    "failed": failed_orders,
                    "not_completed": not_completed_orders
                },
                "total_orders_received": total_orders_recieved,
                "total_number_of_user_profiles": total_number_of_user_profiles,
                "most_purchased_distribution": most_purchasing_distribution_list,
                "all_distribution_order_summary": jsonable_encoder(all_distribution_order_summary),
                "all_meter_order_summary": jsonable_encoder(all_meter_order_summary),
                "all_distribution_successful_failed_summary": jsonable_encoder(all_distribution_success_failed_summary),
                # Add more analytics here...
            }
        }
        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        response = {
            "message": "Error Fetching Results",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": f"{str(e)}"
        }

        return JSONResponse(
            content=response,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# Generate Meter token

@router.post("/generate_meter_token", response_description="Generate Meter Token")
async def generate_meter_token(user_id: Annotated[str, Form()], user: str = Depends(authenticate)):
    try:
        # Get User Id
        user_data = await get_single_order_by_id(user_id)
        user_details = user_data["data"]
        
        # Creating a Bot Instance to send Order confirmation and Unit Token
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Send Order Confirmation Message for buying units
        user_id = user_details['user_profile']['user_id'] # type: ignore

        transaction_id = user_details['transaction_id']
        if user_data.get("message") == "Successful" and user_details['payment_confirmation'] == "PAID":

            # Buy the meter Unit
            buy_meter_unit = buy_meter_unit_vtpass(
                meter_number=user_details['user_meter_number'],
                disco=user_details['meter_code'],
                amount=user_details['user_amount'],
                meter_type=user_details['meter_type']
            )

            if buy_meter_unit['status'] == "200":
                # Get Order details
                meter_token = buy_meter_unit['meter_token']
                meter_unit = buy_meter_unit['meter_units']

               
                await bot.send_message(chat_id=user_id, text=order_successful( # type: ignore
                     meter_number=user_details["user_meter_number"],
                     meter_unit=meter_unit,
                     meter_token=meter_token
                  ), parse_mode="markdown")
               
                # Details to update
                token_data = ["token", meter_token]
                unit_data = ["units", meter_unit]
                unit_confirmation = ["unit_confirmation", "SUCCESSFUL"]
                order_status = ["order_status", "COMPLETED"]

                # Update Database
                await update_user_order_transaction(
                    transaction_id=transaction_id,
                    user_order_data=token_data
                )
                await update_user_order_transaction(
                    transaction_id=transaction_id,
                    user_order_data=unit_data
                )
                await update_user_order_transaction(
                    transaction_id=transaction_id,
                    user_order_data=unit_confirmation
                )
                await update_user_order_transaction(
                    transaction_id=transaction_id,
                    user_order_data=order_status
                )

            response = {
                "message": "Successfully Vended Unit and Update User Order",
                "status": status.HTTP_200_OK,
                "data": {
                    "meter_token": meter_token,
                    "meter_unit": meter_unit
                }
            }
            return JSONResponse(
                content=response,
                status_code=status.HTTP_200_OK
            )
    except Exception as e:
        response = {
            "message": "Error Generating Meter Token",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": f"{str(e)}"
        }
        return JSONResponse(
            content=response,
            status_code=status.HTTP_400_BAD_REQUEST
        )

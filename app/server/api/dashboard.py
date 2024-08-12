from fastapi import APIRouter, status, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from app.server.database.crud import get_user_profile_by_id, get_all_user_profile, get_all_orders, get_single_order_by_id, get_all_users_order, update_user_order_transaction
from app.server.auth.auth import authenticate
from app.server.utils.vtpass_utils import buy_meter_unit_vtpass


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
async def get_user_order(id: str, user: str = Depends(authenticate)) -> JSONResponse:
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
        if get_order_details.get("message") == "Successful":
            order_details = get_order_details['data']
            
            total_amount_of_units_purchased = 0
            total_number_of_units_purchased = 0
            most_purchasing_meter = ""
            most_purchasing_user = ""
            count_meter_purchases = 0
            # meters_list = [order_details['user_meter_number'] for i in order_details]
            
            # print(meters_list)
            
            # Analytics Calculations
            for order in order_details:
               # Total Amount Of Units Purchased
               if order["user_amount"] == "":
                  continue
               elif order["user_amount"] and order['payment_confirmation'] == "PAID":
                  total_amount_of_units_purchased += order["user_amount"]
                  
               # Total Number of Units Purchased
               if order['units'] == "":
                  continue
               elif order['payment_confirmation'] == "PAID" and order["unit_confirmation"] == "SUCCESSFUL":
                  total_number_of_units_purchased += float(order['units'])
                  # Most Purchasing Meter
                  # count_meter_details['user_meter_details'] = ""
               
               # Most Purchasing User
               # Successful/Failed/Not Completed Payment
               # Successful/Failed/Not Completed Unit
               # Sucessful/Failed/Not Completed Order
               # Total Number of Orders Received
               # Total Number of User Profiles
               # Most Purchased Distribution
               # Numbers For Each Distro of Successful/Failed/Not Completed
        response = {
            "message": "Successfully Generated Analytics",
            "status": status.HTTP_200_OK,
            "data": {
                "total_amount_of_units_purchased": total_amount_of_units_purchased,
                "total_number_of_units_purchased": total_number_of_units_purchased,
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
            "message":"Successfully Vended Unit and Update User Order",
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
         "message":"Error Generating Meter Token",
         "status": status.HTTP_400_BAD_REQUEST,
         "error": f"{str(e)}"
      }
      return JSONResponse(
         content=response,
         status_code=status.HTTP_400_BAD_REQUEST
      )
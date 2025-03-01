import logging
from datetime import datetime

from app.server.bot.whatsapp_messages import (
    bill_amount_menu,
    customer_support,
    meter_number_menu,
    order_failed_whatsapp,
    order_payment_updated,
    order_summary_updated,
    quit_chat,
)

# Database Modules
from app.server.database.crud import (
    create_order,
    create_user_profile,
    create_user_session,
    delete_user_session,
    get_single_session,
    get_user_profile,
    update_user_order,
    update_user_session,
)
from app.server.utils.paystack_payment import create_transaction_url

# Get Account Creation Modules and Electricity bills
from app.server.utils.virtual_account import create_account
from app.server.utils.vtpass_utils import get_meter_details_vtpass
from app.server.utils.whatsapp import (
    send_call_to_action_payment_whatsapp,
    send_confirm_order_message,
    send_disco_list_message,
    send_meter_type_buttons,
    send_whatsapp_message_normal,
    send_whatsapp_message_opening_buttons,
)

logging.basicConfig(level=logging.INFO)


async def handle_whatsapp_chat(phonenumber, text, profilename, phoneid):
    try:
        # Check if session exists
        get_chat = await get_single_session(phoneid)

        if get_chat["user_phone_number"] == phonenumber:

            chat = get_chat

    except Exception:
        created_at = datetime.now()

        # Check if User profile Exists

        user_profile = await get_user_profile(phoneid)

        if user_profile and (user_profile.get("user_id", None) == phoneid):
            user_profile = user_profile

        else:

            # Create User Profile if it doesnt exists

            user_profile_data = {
                "username": profilename,
                "full_name": profilename.upper(),
                "user_id": phoneid,
                "created_at": created_at,
            }

            user_profile = await create_user_profile(user_profile_data)

        # Create Chat Session

        try:
            # session_id = "WAT" + str(uuid7()).split("-")[4]
            created_at = datetime.now()

            chat_session_data = {
                "user_profile": user_profile,
                "session_id": phoneid,
                "user_phone_number": phonenumber,
                "entry_message": None,
                "user_input_1": None,
                "user_input_2": None,
                "meter_distribution": None,
                "user_meter_number": None,
                "meter_owner": None,
                "meter_address": None,
                "user_amount": None,
                "meter_type": None,
                "meter_code": None,
                "user_confirm": None,
                "token": None,
                "units": None,
                "payment_confirmation": None,
                "unit_confirmation": None,
                "transaction_id": None,
                "order_status": None,
                "transaction_reference": None,
                "created_at": created_at,
            }

            # Create the chat session

            chat = await create_user_session(chat_session_data)

        except Exception as e:
            print(f"Exception in Creating User Session: {str(e)}")

        # Bot Coversations
        opening = ["hi", "Hi", "Hello", "Hello", "Hey", "hey", "start", "Start"]
        # opening_msg = random.choice(opening).upper()

        # Check user input and send opening message
        if text in opening:

            send_whatsapp_message_opening_buttons(phonenumber, profilename)
        else:
            message = f"Hey {profilename}, I'm a Bot To help you buy electricity unit, Just type 'Hi, Hey, or Hello' to start."
            send_whatsapp_message_normal(phonenumber, message)

    quit_inputs = ["q", "Q", "Quit", "quit", "QUIT"]

    # Bot Conversational Logic

    created_at = datetime.now()

    if chat["entry_message"]:  # type: ignore
        if chat["user_input_1"]:  # type: ignore
            if chat["user_input_2"]:  # type: ignore
                if chat["user_meter_number"]:  # type: ignore
                    if chat["meter_type"]:  # type: ignore
                        if chat["user_amount"]:  # type: ignore
                            if chat["user_confirm"]:  # type: ignore
                                if text in quit_inputs:

                                    message = quit_chat()
                                    send_whatsapp_message_normal(phonenumber, message)

                                    await delete_user_session(phoneid)

                                    update_data = ["order_status", "FAILED"]

                                    await update_user_order(update_data, phoneid)
                                    await update_user_order(
                                        ["unit_confirmation", "FAILED"], phoneid
                                    )

                                else:
                                    message = "We are Already Processing Your Order!!!"
                                    send_whatsapp_message_normal(phonenumber, message)
                            else:
                                try:
                                    if text == "Confirm":
                                        update_data = ["user_confirm", text]
                                        data = await update_user_session(
                                            update_data, phoneid
                                        )

                                        # Generate Payment Details
                                        amount = chat["user_amount"]  # type: ignore

                                        generate_virtual_account = create_account(
                                            name=profilename, amount=amount
                                        )
                                        if generate_virtual_account["status"] == "200":
                                            account_number = generate_virtual_account[
                                                "Account Number"
                                            ]
                                            account_name = generate_virtual_account[
                                                "Account Name"
                                            ]
                                            bank_name = generate_virtual_account["Bank"]
                                            transaction_id = generate_virtual_account[
                                                "ID"
                                            ]
                                            payment_status = generate_virtual_account[
                                                "Payment Status"
                                            ]

                                            # Create Transaction URL for Paystack Payment
                                            transaction_url: dict = (
                                                create_transaction_url(
                                                    amount=int(amount) * 100,
                                                    payment_reference=transaction_id,
                                                )
                                            )
                                            status = transaction_url.get("status", None)

                                            if status == "200":
                                                # Get the transaction url

                                                response_url = transaction_url.get(
                                                    "transaction_url"
                                                )

                                                account_details = order_payment_updated(
                                                    str(amount),
                                                    account_number,
                                                    account_name,
                                                    bank_name,
                                                )

                                                send_call_to_action_payment_whatsapp(
                                                    phone_number=phonenumber,
                                                    body_text=account_details,
                                                    transaction_url=response_url,
                                                )

                                            else:
                                                account_details = order_payment_updated(
                                                    str(amount),
                                                    account_number,
                                                    account_name,
                                                    bank_name,
                                                )

                                                send_call_to_action_payment_whatsapp(
                                                    phone_number=phonenumber,
                                                    body_text=account_details,
                                                    transaction_url="https://www.energiease.ng",
                                                )

                                            await update_user_session(
                                                ["transaction_id", transaction_id],
                                                phoneid,
                                            )
                                            await update_user_session(
                                                [
                                                    "payment_confirmation",
                                                    payment_status,
                                                ],
                                                phoneid,
                                            )

                                            # Create order
                                            order_data = {
                                                "user_profile": chat["user_profile"],  # type: ignore
                                                "session_id": phoneid,  # type: ignore
                                                "meter_distribution": chat["meter_distribution"],  # type: ignore
                                                "user_meter_number": chat["user_meter_number"],  # type: ignore
                                                "meter_owner": chat["meter_owner"],  # type: ignore
                                                "meter_address": chat["meter_address"],  # type: ignore
                                                "user_amount": chat["user_amount"],  # type: ignore
                                                "meter_type": chat["meter_type"],  # type: ignore
                                                "meter_code": chat["meter_code"],  # type: ignore
                                                "token": None,
                                                "units": None,
                                                "payment_confirmation": payment_status,
                                                "unit_confirmation": "",
                                                "transaction_id": transaction_id,
                                                "order_status": "",
                                                "transaction_reference": None,
                                                "created_at": created_at,
                                            }  # type: ignore

                                            await create_order(order_data)

                                            # await delete_user_session(phoneid)

                                        elif (
                                            generate_virtual_account["status"] == "400"
                                        ):

                                            reply_text = order_failed_whatsapp(
                                                order_id=chat["_id"]  # type: ignore
                                            )

                                            # Create order
                                            order_data = {
                                                "user_profile": chat["user_profile"],  # type: ignore
                                                "session_id": phoneid,
                                                "meter_distribution": chat["meter_distribution"],  # type: ignore
                                                "user_meter_number": chat["user_meter_number"],  # type: ignore
                                                "meter_owner": chat["meter_owner"],  # type: ignore
                                                "meter_address": chat["meter_address"],  # type: ignore
                                                "user_amount": chat["user_amount"],  # type: ignore
                                                "meter_type": chat["meter_type"],  # type: ignore
                                                "meter_code": chat["meter_code"],  # type: ignore
                                                "token": None,
                                                "units": None,
                                                "payment_confirmation": "NO_PAYMENT",
                                                "unit_confirmation": "FAILED",
                                                "transaction_id": None,
                                                "order_status": "FAILED",
                                                "transaction_reference": None,
                                                "created_at": created_at,
                                            }  # type: ignore

                                            send_whatsapp_message_normal(
                                                phonenumber, reply_text
                                            )

                                            await create_order(order_data)

                                            await delete_user_session(phoneid)

                                    elif text == "Cancel":
                                        # Create a Failed Order and Delete Session

                                        order_data = {
                                            "user_profile": chat["user_profile"],  # type: ignore
                                            "session_id": phoneid,  # type: ignore
                                            "meter_distribution": chat["meter_distribution"],  # type: ignore
                                            "user_meter_number": chat["user_meter_number"],  # type: ignore
                                            "meter_owner": chat["meter_owner"],  # type: ignore
                                            "meter_address": chat["meter_address"],  # type: ignore
                                            "user_amount": chat["user_amount"],  # type: ignore
                                            "meter_type": chat["meter_type"],  # type: ignore
                                            "meter_code": chat["meter_code"],  # type: ignore
                                            "token": None,
                                            "units": None,
                                            "payment_confirmation": "NO_PAYMENT",
                                            "unit_confirmation": "FAILED",
                                            "transaction_id": None,
                                            "order_status": "FAILED",
                                            "transaction_reference": None,
                                            "created_at": created_at,
                                        }  # type: ignore

                                        await create_order(order_data)

                                        message = order_failed_whatsapp(
                                            chat["_id"]
                                        )  # type: ignore
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )

                                        message = quit_chat()
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )

                                        await delete_user_session(phoneid)
                                    else:
                                        message = "Oops 😓 Please Enter a Valid Input:"
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )

                                except Exception:
                                    if text in quit_inputs:
                                        message = quit_chat()
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )
                                        await delete_user_session(phoneid)
                                    else:
                                        message = "Oops 😓 Please Enter a Valid Input:"
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )
                        else:
                            try:
                                check_type = int(text.replace(" ", ""))
                                if check_type >= 1000:
                                    update_data = ["user_amount", text]
                                    data = await update_user_session(
                                        update_data, phoneid
                                    )

                                    # Get Meter Details
                                    user_meter_details = get_meter_details_vtpass(
                                        # type: ignore
                                        meter_number=data["user_meter_number"],  # type: ignore
                                        meter_type=data["meter_type"],  # type: ignore
                                        disco=data["meter_code"],  # type: ignore
                                    )

                                    if user_meter_details["status"] == "200":
                                        # get from api call
                                        meter_owner = user_meter_details["meter_name"]
                                        # get from api call
                                        meter_address = user_meter_details[
                                            "meter_address"
                                        ]

                                        # Update user Session
                                        await update_user_session(
                                            ["meter_owner", meter_owner], phoneid
                                        )
                                        await update_user_session(
                                            ["meter_address", meter_address], phoneid
                                        )

                                        message = order_summary_updated(
                                            meter_owner,
                                            data["user_amount"],  # type: ignore
                                            data["user_meter_number"],  # type: ignore
                                            data["meter_type"],  # type: ignore
                                            meter_address,
                                        )

                                        send_confirm_order_message(phonenumber, message)
                                    else:
                                        # Create a Failed Order and Delete Session

                                        order_data = {
                                            "user_profile": chat["user_profile"],  # type: ignore
                                            "session_id": phoneid,
                                            "meter_distribution": chat["meter_distribution"],  # type: ignore
                                            "user_meter_number": chat["user_meter_number"],  # type: ignore
                                            "meter_owner": chat["meter_owner"],  # type: ignore
                                            "meter_address": chat["meter_address"],  # type: ignore
                                            "user_amount": chat["user_amount"],  # type: ignore
                                            "meter_type": chat["meter_type"],  # type: ignore
                                            "meter_code": chat["meter_code"],  # type: ignore
                                            "token": None,
                                            "units": None,
                                            "payment_confirmation": "NO_PAYMENT",
                                            "unit_confirmation": "FAILED",
                                            "transaction_id": None,
                                            "order_status": "FAILED",
                                            "transaction_reference": None,
                                            "created_at": created_at,
                                        }

                                        await create_order(order_data)
                                        message = order_failed_whatsapp(
                                            chat["_id"]
                                        )  # type: ignore
                                        send_whatsapp_message_normal(
                                            phonenumber, message
                                        )
                                        await delete_user_session(phoneid)
                                else:

                                    message = "Oops 😓 ❗Please enter an amount not below 1000:"
                                    send_whatsapp_message_normal(phonenumber, message)
                            except Exception:
                                if text in quit_inputs:
                                    message = quit_chat()
                                    send_whatsapp_message_normal(phonenumber, message)
                                    await delete_user_session(phoneid)
                                else:
                                    message = "Oops 😓 ❗Please enter an amount not below 1000:"
                                    send_whatsapp_message_normal(phonenumber, message)
                    else:
                        try:
                            if text == "Prepaid":

                                data = await update_user_session(
                                    ["meter_type", "prepaid"], phoneid
                                )
                                message = bill_amount_menu()
                                send_whatsapp_message_normal(phonenumber, message)

                                if data["meter_distribution"] == "IKEDC":  # type: ignore
                                    billers_id = "ikeja-electric"
                                elif data["meter_distribution"] == "AEDC":  # type: ignore
                                    billers_id = "abuja-electric"
                                elif data["meter_distribution"] == "EEDC":  # type: ignore
                                    billers_id = "enugu-electric"
                                elif data["meter_distribution"] == "EKEDC":  # type: ignore
                                    billers_id = "eko-electric"
                                elif data["meter_distribution"] == "IBEDCO":  # type: ignore
                                    billers_id = "ibadan-electric"
                                elif data["meter_distribution"] == "JED":  # type: ignore
                                    billers_id = "jos-electric"
                                elif data["meter_distribution"] == "KAEDCO":  # type: ignore
                                    billers_id = "kano-electric"
                                elif data["meter_distribution"] == "KEDCO":  # type: ignore
                                    billers_id = "kaduna-electric"
                                elif data["meter_distribution"] == "PHED":  # type: ignore
                                    billers_id = "portharcourt-electric"
                                elif data["meter_distribution"] == "BEDC":  # type: ignore
                                    billers_id = "benin-electric"
                                elif data["meter_distribution"] == "ABA":  # type: ignore
                                    billers_id = "aba-electric"
                                elif data["meter_distribution"] == "YEDC":  # type: ignore
                                    billers_id = "yola-electric"

                                # Update Database
                                await update_user_session(
                                    ["meter_code", billers_id], phoneid
                                )

                            elif text == "Postpaid":

                                data = await update_user_session(
                                    ["meter_type", "postpaid"], phoneid
                                )
                                message = bill_amount_menu()
                                send_whatsapp_message_normal(phonenumber, message)

                                if data["meter_distribution"] == "IKEDC":  # type: ignore
                                    billers_id = "ikeja-electric"
                                elif data["meter_distribution"] == "AEDC":  # type: ignore
                                    billers_id = "abuja-electric"
                                elif data["meter_distribution"] == "EEDC":  # type: ignore
                                    billers_id = "enugu-electric"
                                elif data["meter_distribution"] == "EKEDC":  # type: ignore
                                    billers_id = "eko-electric"
                                elif data["meter_distribution"] == "IBEDCO":  # type: ignore
                                    billers_id = "ibadan-electric"
                                elif data["meter_distribution"] == "JED":  # type: ignore
                                    billers_id = "jos-electric"
                                elif data["meter_distribution"] == "KAEDCO":  # type: ignore
                                    billers_id = "kano-electric"
                                elif data["meter_distribution"] == "KEDCO":  # type: ignore
                                    billers_id = "kaduna-electric"
                                elif data["meter_distribution"] == "PHED":  # type: ignore
                                    billers_id = "portharcourt-electric"
                                elif data["meter_distribution"] == "BEDC":  # type: ignore
                                    billers_id = "benin-electric"
                                elif data["meter_distribution"] == "ABA":  # type: ignore
                                    billers_id = "aba-electric"
                                elif data["meter_distribution"] == "YEDC":  # type: ignore
                                    billers_id = "yola-electric"

                                # Update Database
                                await update_user_session(
                                    ["meter_code", billers_id], phoneid
                                )

                            else:
                                message = "Oops 😓 Please Enter a Valid Amount:"
                                send_whatsapp_message_normal(phonenumber, message)
                        except Exception:
                            if text in quit_inputs:
                                message = quit_chat()
                                send_whatsapp_message_normal(phonenumber, message)
                                await delete_user_session(phoneid)
                            else:
                                message = "Oops 😓 Please Enter a Valid Input"
                                send_whatsapp_message_normal(phonenumber, message)
                else:
                    try:
                        if len(text) != 11 and len(text) != 13:
                            message = f"Oops 😓 Please Enter a Valid Meter Number (11 or 13 Digits){len(text)}:"
                            send_whatsapp_message_normal(phonenumber, message)

                        else:

                            send_meter_type_buttons(phonenumber)

                            update_data = ["user_meter_number", text]
                            await update_user_session(update_data, phoneid)

                    except Exception:
                        if text in quit_inputs:
                            message = quit_chat()
                            send_whatsapp_message_normal(phonenumber, message)
                            await delete_user_session(phoneid)
                        else:
                            message = "Oops 😓 Please Enter a Valid Meter Number (11 or 13 Digits):"
                            send_whatsapp_message_normal(phonenumber, message)
            else:
                try:

                    if text in [
                        "AEDC",
                        "EEDC",
                        "EKEDC",
                        "IBEDCO",
                        "IKEDC",
                        "JED",
                        "KAEDCO",
                        "KEDCO",
                        "PHED",
                        "BEDC",
                    ]:

                        message = meter_number_menu()
                        send_whatsapp_message_normal(phonenumber, message)

                        update_data = ["user_input_2", text]
                        await update_user_session(update_data, phoneid)

                        await update_user_session(["meter_distribution", text], phoneid)
                    else:
                        message = "Oops 😓 Please Enter a valid input:"
                        send_whatsapp_message_normal(phonenumber, message)

                except Exception:

                    if text in quit_inputs:

                        message = quit_chat()
                        send_whatsapp_message_normal(phonenumber, message)
                        await delete_user_session(phoneid)
                    else:
                        message = "Oops 😓 Please Enter a valid input:"

                        send_whatsapp_message_normal(phonenumber, message)
        else:
            try:
                if text == "Buy Electricity":

                    send_disco_list_message(phonenumber)

                    update_data = ["user_input_1", text]
                    await update_user_session(update_data, phoneid)

                elif text == "Customer Support":

                    message = customer_support()
                    send_whatsapp_message_normal(phonenumber, message)

                    update_data = ["user_input_1", text]
                    await update_user_session(update_data, phoneid)

                elif text == "Meter KTC":

                    message = customer_support()
                    send_whatsapp_message_normal(phonenumber, message)

                    update_data = ["user_input_1", text]
                    await update_user_session(update_data, phoneid)

                else:
                    message = "Oops 😓 Please Enter a Number:"
                    send_whatsapp_message_normal(phonenumber, message)

            except Exception:
                if text in quit_inputs:
                    message = quit_chat()
                    send_whatsapp_message_normal(phonenumber, message)
                    await delete_user_session(phoneid)
                else:
                    message = "Oops 😓 Please Enter a Number:"
                    send_whatsapp_message_normal(phonenumber, message)
    else:
        if text in opening:
            update_data = ["entry_message", text]
            await update_user_session(update_data, phoneid)

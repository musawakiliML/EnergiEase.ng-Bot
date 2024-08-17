import logging
import telegram
from uuid6 import uuid7
from datetime import datetime
from telegram.ext import ContextTypes

from telegram import (
    ReplyKeyboardRemove, Update,
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from telegram.ext import (
    CallbackContext, ConversationHandler
)

# Get Modules for chatbot messages
from app.server.bot.message import *

# Get Account Creation Modules and Electricity bills
from app.server.utils.virtual_account import *
from app.server.utils.vtpass_utils import (
    get_meter_details_vtpass
)
from app.server.utils.paystack_payment import create_transaction_url

# Database Modules
from app.server.database.crud import (
    get_single_order,
    create_order,
    get_user_profile,
    create_user_profile,
    update_user_order,
    create_meter_details,
    get_meter_details,
    update_meter_details
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define chatbot states for conversation flow
START_CHOICE, CHOOSE_DISTRO, COLLECT_METER_NUMBER, VERIFY_METER_NUMBER, CHOOSE_METER_TYPE, ELECTRICTY_AMOUNT, ORDER_CONFIRMATION, ACCOUNT_DETAILS, PAYMEMT_STATUS, UNIT_STATUS = range(
    10)

# Define callback_data for the conversation flow
BUY_ELECTRICITY, CANCEL_ORDER, CONFIRM_ORDER, CANCEL_PAYMENT, CONFIRM_PAYMENT, SUPPORT = range(
    6)

# Define the Start Command


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the bot with a message to select an option when the command /start is issued."""
    reply_keyboard = [[
        InlineKeyboardButton(
            text="Buy Electricity⚡",
            callback_data=str(BUY_ELECTRICITY)
        ),
        InlineKeyboardButton(
            text="Customer Support ☎️",
            callback_data=str(SUPPORT)
        )
    ]]
    markup = InlineKeyboardMarkup(reply_keyboard)

    # Get user Details
    user = update.effective_user
    name = user.full_name # type: ignore
    username = user.username # type: ignore
    user_id = user.id # type: ignore
    created_at = datetime.now()

    # logger.info(f"{username}, {user_id}")

    # Create User Profile
    user_profile = await get_user_profile(user_id) # type: ignore
    # logger.info(f"{user_profile}")
    try:
        # Check if user profile exists
        if user_profile and (user_profile['user_id'] == user_id):

            user_profile = user_profile

            # logger.info(f"{user_profile}")
    except:
        # Create User Profile
        user_profile_data = {
            "username": username,
            "full_name": name,
            "user_id": user_id,
            "created_at": created_at
        }
        user_profile = await create_user_profile(user_profile_data)
    logger.info(f"{context.user_data}")
    # Create a new Order
    session_id = str(uuid7()).split("-")[4]
    created_at = datetime.utcnow()

    user_order_data = {
        "user_profile": user_profile,
        "session_id": session_id,
        "meter_distribution": "",
        "user_meter_number": "",
        "meter_owner": "",
        "meter_address": "",
        "user_amount": "",
        "meter_type": "",
        "meter_code": "",
        "token": "",
        "units": "",
        "payment_confirmation": "",
        "unit_confirmation": "",
        "transaction_id": "",
        "order_status": "",
        "transaction_reference": "",
        "created_at": created_at
    }

    user_order_session = await create_order(user_order_data)

    context.user_data["session_id"] = session_id # type: ignore

    reply_message = welcome_menu(name)
    logger.info(f"{update.effective_chat.id}") # type: ignore
    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text=reply_message,
        parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
        reply_markup=markup,
    )

    return START_CHOICE

# Choosing the Distro


async def distro_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for the distribution company"""
    query = update.callback_query
    await query.answer() # type: ignore

    distribution_companies = [
        "AEDC", "EEDC", "EKEDC", "IBEDCO", "IKEDC",
        "JED", "KAEDCO", "KEDCO", "PHED", "BEDC", "ABA", "YEDC"
    ] # "ABA", "YEDC"

    buttons_per_row = 3  # Set the number of buttons per row
    reply_keyboard = [
        [
            InlineKeyboardButton(text=company, callback_data=company)
            for company in distribution_companies[i:i + buttons_per_row]
        ]
        for i in range(0, len(distribution_companies), buttons_per_row)
    ]

    markup = InlineKeyboardMarkup(reply_keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text=f"{options_menu()}",
        reply_markup=markup,
    )

    return CHOOSE_DISTRO

# Handling the meter distribution company


async def choose_distro(update: Update, context: CallbackContext) -> int:
    '''Handling the meter distribution choice from the choice input
    Collect meter number from user and Validate the collected meter number'''

    query = update.callback_query
    await query.answer() # type: ignore

    # save user input in context memory
    context.user_data["distribution_company"] = update.callback_query.data # type: ignore

    # Save to database
    session_id = context.user_data["session_id"] # type: ignore
    user_order_data = ["meter_distribution", update.callback_query.data] # type: ignore
    await update_user_order(user_order_data, session_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text=f"{meter_number_menu()}",
    )
    return COLLECT_METER_NUMBER

# Verifying Meter Number


async def validate_meter_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate the collected meter number and get meter type"""
    user_input = update.message.text.strip() # type: ignore

    if not user_input.isdigit() or (len(user_input) != 11 and len(user_input) != 13):
        
        await update.message.reply_text("Invalid meter number. Please enter a 11 or 13-digit number.") # type: ignore

        return COLLECT_METER_NUMBER

    # Save meter number
    context.user_data["meter_number"] = user_input # type: ignore

    # Save to database
    session_id = context.user_data["session_id"] # type: ignore
    user_order_data = ["user_meter_number", user_input]
    await update_user_order(user_order_data, session_id)

    reply_keyboard = [
        [
            InlineKeyboardButton(
                text="Prepaid",
                callback_data="prepaid"
            ),
            InlineKeyboardButton(
                text="Postpaid",
                callback_data="postpaid"
            ),
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text="Choose your meter type:",
        reply_markup=markup,
    )

    return CHOOSE_METER_TYPE

# Choose Meter Type


async def choose_meter_type(update: Update, context: CallbackContext) -> int:
    '''Collecting Meter type: Prepaid or Postpaid'''

    query = update.callback_query
    await query.answer() # type: ignore

    # save user meter type
    context.user_data["meter_type"] = update.callback_query.data # type: ignore

    # Check Meter type and distro for equivalent data
    if context.user_data["distribution_company"] == "AEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "abuja-electric"
    elif context.user_data["distribution_company"] == "AEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "abuja-electric"
    elif context.user_data["distribution_company"] == "EEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "enugu-electric"
    elif context.user_data["distribution_company"] == "EEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "enugu-electric"
    elif context.user_data["distribution_company"] == "EKEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "eko-electric"
    elif context.user_data["distribution_company"] == "EKEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "eko-electric"
    elif context.user_data["distribution_company"] == "IBEDCO" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "ibadan-electric"
    elif context.user_data["distribution_company"] == "IBEDCO" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "ibadan-electric"
    elif context.user_data["distribution_company"] == "IKEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "ikeja-electric"
    elif context.user_data["distribution_company"] == "IKEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "ikeja-electric"
    elif context.user_data["distribution_company"] == "JED" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "jos-electric"
    elif context.user_data["distribution_company"] == "JED" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "jos-electric"
    elif context.user_data["distribution_company"] == "ABA" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "aba-electric"
    elif context.user_data["distribution_company"] == "ABA" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "aba-electric"
    elif context.user_data["distribution_company"] == "KAEDCO" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "kaduna-electric"
    elif context.user_data["distribution_company"] == "KAEDCO" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "kaduna-electric"
    elif context.user_data["distribution_company"] == "KEDCO" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "kano-electric"
    elif context.user_data["distribution_company"] == "KEDCO" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "kano-electric"
    elif context.user_data["distribution_company"] == "PHED" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "portharcourt-electric"
    elif context.user_data["distribution_company"] == "PHED" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "portharcourt-electric"
    elif context.user_data["distribution_company"] == "BEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "benin-electric"
    elif context.user_data["distribution_company"] == "BEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "benin-electric"
    elif context.user_data["distribution_company"] == "YEDC" and update.callback_query.data == "prepaid": # type: ignore
        meter_code = "yola-electric"
    elif context.user_data["distribution_company"] == "YEDC" and update.callback_query.data == "postpaid": # type: ignore
        meter_code = "yola-electric"

    # Save to database
    session_id = context.user_data["session_id"] # type: ignore
    user_order_data = ["meter_type", update.callback_query.data] # type: ignore
    user_meter_code = ["meter_code", meter_code]
    await update_user_order(user_order_data, session_id)
    await update_user_order(user_meter_code, session_id)

    reply_message = bill_amount_menu()

    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text=reply_message,
    )
    return ELECTRICTY_AMOUNT

# Get Electricity Amount


async def get_electricity_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Get Electricity Amount and validate it'''
    try:
        electricity_amount = int(update.message.text) # type: ignore
        if electricity_amount < 1000:
            await update.message.reply_text("❗Please enter an amount not below 1000:") # type: ignore

            return ELECTRICTY_AMOUNT

        # Save Electricity Amount
        context.user_data["electricity_amount"] = electricity_amount # type: ignore

        # Save to database
        session_id = context.user_data["session_id"] # type: ignore
        user_order_data = ["user_amount", electricity_amount]
        await update_user_order(user_order_data, session_id)

        # Confirmation of the order
        reply_keyboard = [
            [
                InlineKeyboardButton(
                    "Cancel ❌",
                    callback_data=str(CANCEL_ORDER)
                ),
                InlineKeyboardButton(
                    "Confirm ✅",
                    callback_data=str(CONFIRM_ORDER)
                )
            ]
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        # distro = context.user_data['distribution_company']
        # meter_number = context.user_data['meter_number']
        # meter_type = context.user_data['meter_type']
        # amount = context.user_data['electricity_amount']

        # Get user meter details from database
        user_meter_info = await get_single_order(session_id)
        distro_code = user_meter_info["meter_code"]
        meter_number = user_meter_info["user_meter_number"]
        meter_type = user_meter_info["meter_type"]
        amount = user_meter_info["user_amount"]

        # Get meter details
        user_meter_details = get_meter_details_vtpass(
            meter_number=meter_number,
            meter_type=meter_type,
            disco=distro_code
        )
        # logger.info(f"{user_meter_details}")
        if user_meter_details["status"] == "200":
            meter_owner = user_meter_details["meter_name"]  # get from api call
            # get from api call
            meter_address = user_meter_details["meter_address"]
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, # type: ignore
                text=order_failed(user_meter_info["_id"]),
                parse_mode="markdown"
            )
            # Update Order Details 
            unit_confirmation = ["unit_confirmation", "FAILED"]
            order_status = ["order_status", "FAILED"]
            payment_confirmation = ['payment_confirmation', "NO_PAYMENT"]
            
            await update_user_order(unit_confirmation, session_id)
            await update_user_order(order_status, session_id)
            await update_user_order(payment_confirmation, session_id)
            return ConversationHandler.END

        session_id = context.user_data["session_id"] # type: ignore
        user_meter_name = ["meter_owner", meter_owner]
        user_meter_address = ["meter_address", meter_address]

        await update_user_order(user_meter_name, session_id)
        await update_user_order(user_meter_address, session_id)

        reply_text = order_summary(
            meter_number=meter_number,
            owner=meter_owner,
            amount=amount,
            package=meter_type,
            address=meter_address)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text=reply_text,
            parse_mode="markdown",
            reply_markup=markup,
        )

        return ORDER_CONFIRMATION
    except ValueError:
        await update.message.reply_text("❗Please enter a valid number:") # type: ignore
        return ELECTRICTY_AMOUNT

# Handling Order Confirmation


async def order_confirmation(update: Update, context: CallbackContext) -> int: # type: ignore
    ''' Handling order confirmation '''

    if update.callback_query.data == str(CANCEL_ORDER): # type: ignore
        # Get user meter details from database
        session_id = context.user_data["session_id"] # type: ignore
        user_meter_info = await get_single_order(session_id)
        
        # Add Order Failed Message
        reply_text = cancel_order(
            order_id=user_meter_info["_id"]
        )
        
        # Update Order Details 
        unit_confirmation = ["unit_confirmation", "FAILED"]
        order_status = ["order_status", "FAILED"]
        payment_confirmation = ['payment_confirmation', "NO_PAYMENT"]
        
        await update_user_order(unit_confirmation, session_id)
        await update_user_order(order_status, session_id)
        await update_user_order(payment_confirmation, session_id)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text=reply_text,
            parse_mode="markdown"
        )
        
        return ConversationHandler.END

    elif update.callback_query.data == str(CONFIRM_ORDER): # type: ignore
        # Generate account details using API
        user = update.effective_user
        name = user.full_name # type: ignore

        session_id = context.user_data['session_id'] # type: ignore
        user_order_details = await get_single_order(session_id)

        amount = user_order_details["user_amount"]

        generate_virtual_account = create_account(
            name=name,
            amount=amount
        )
        if generate_virtual_account['status'] == "200":
            account_number = generate_virtual_account['Account Number']
            account_name = generate_virtual_account['Account Name']
            bank_name = generate_virtual_account['Bank']
            transaction_id = generate_virtual_account["ID"]
            payment_status = generate_virtual_account["Payment Status"]
            
            # Create Transaction URL for Paystack Payment
            transaction_url: dict = create_transaction_url(
                amount=amount,
                payment_reference=transaction_id
            )
            status = transaction_url.get("status", None)
            
            if status == "200":
                # Get the transaction url
                
                response_url = transaction_url.get("transaction_url")
                account_details = order_payment(
                    amount, account_number, account_name, bank_name, transaction_url=response_url)
                
            else:
                account_details = order_payment(
                    amount, account_number, account_name, bank_name, transaction_url="")

            await context.bot.send_message(chat_id=update.effective_chat.id, text=account_details, parse_mode="markdown") # type: ignore

            await update_user_order(["transaction_id", transaction_id], session_id)
            await update_user_order(["payment_confirmation", payment_status], session_id)

            return ConversationHandler.END
        elif generate_virtual_account['status'] == "400":
            reply_text = order_failed(
                order_id=user_order_details["_id"]
            )
            
            await context.bot.send_message(
                    chat_id=update.effective_chat.id, # type: ignore
                    text=reply_text,
                    parse_mode="markdown"
                    )
            
            # Update Order Details 
            unit_confirmation = ["unit_confirmation", "FAILED"]
            order_status = ["order_status", "FAILED"]
            payment_confirmation = ['payment_confirmation', "NO_PAYMENT"]
            
            await update_user_order(unit_confirmation, session_id)
            await update_user_order(order_status, session_id)
            await update_user_order(payment_confirmation, session_id)
            
            return ConversationHandler.END


# Customer Support
async def customer_support_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user to chat the Customer Support on a Number"""
    query = update.callback_query
    await query.answer() # type: ignore

    await query.edit_message_text( # type: ignore
        "Welcome to Customer Support 🧑‍💻"
        "Reach Us on t.me/musawakiliml. For your inquiries."
        "Thank You."
    ) 

    return START_CHOICE

# Cancel Chat Sessions


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    
    session_id = str(context.user_data.get('session_id', 'None')) # type: ignore
    logger.info(f"Session ID: {session_id}")
    if session_id != "None":
        user_order_details = await get_single_order(session_id)
        # Add Order Failed Message
        reply_text = cancel_order(
            order_id=user_order_details["_id"]
        )
        await update_user_order(["unit_confirmation", "FAILED"], session_id)
        await update_user_order(["order_status", "FAILED"], session_id)
        await update_user_order(["payment_confirmation", "NO_PAYMENT"], session_id)
        
        await update.message.reply_text( # type: ignore
        f"{reply_text}", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown"
    )
        
    else:
        await update.message.reply_text( # type: ignore
        f"{quit_chat()}", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown"
    )
    
    # # Clear user data to avoid lingering issues
    # context.user_data.clear() # type: ignore

    return ConversationHandler.END

# Help Command


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Display Bot Help Menu To User'''
    await update.message.reply_text( # type: ignore
        f"{help_menu()}"
    )
    return ConversationHandler.END

# Customer Support Command


async def customer_support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user to chat the Customer Support on a Number"""

    await update.message.reply_text( # type: ignore
        "Welcome to EnergiEase Customer Support 🧑‍💻"
        "Reach Us on t.me/musawakiliml. For your inquiries."
        "Thank You."
    )
    return ConversationHandler.END

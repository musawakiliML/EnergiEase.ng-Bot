import logging
from uuid6 import uuid7
from datetime import datetime
from telegram.ext import ContextTypes

from telegram import (
   ReplyKeyboardRemove, Update,
   InlineKeyboardButton, InlineKeyboardMarkup
)

from telegram.ext import (
   CallbackContext, ConversationHandler
)

# Get Modules for chatbot messages
from app.server.bot.message import *

# Get Account Creation Modules and Electricity bills
from app.server.utils.virtual_account import *
from app.server.utils.buy_electricity import *

# Database Modules
from app.server.database.crud import (
   get_single_order,
   create_order,
   get_user_profile,
   create_user_profile,
   update_user_order
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define chatbot states for conversation flow
START_CHOICE, CHOOSE_DISTRO, COLLECT_METER_NUMBER, VERIFY_METER_NUMBER, CHOOSE_METER_TYPE, ELECTRICTY_AMOUNT, ORDER_CONFIRMATION, ACCOUNT_DETAILS, PAYMEMT_STATUS, UNIT_STATUS = range(10)

# Define callback_data for the conversation flow
BUY_ELECTRICITY, CANCEL_ORDER, CONFIRM_ORDER, CANCEL_PAYMENT, CONFIRM_PAYMENT, SUPPORT = range(6)

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
   name = user.full_name
   username = user.username
   user_id = user.id
   created_at = datetime.now()

   # logger.info(f"{username}, {user_id}")

   # Create User Profile
   user_profile = await get_user_profile(user_id)
   # logger.info(f"{user_profile}")
   try:
      # Check if user profile exists
      if user_profile and (user_profile['user_id'] == user_id):
         
         user_profile = user_profile

         # logger.info(f"{user_profile}")
   except:
      # Create User Profile
      user_profile_data = {
         "username":username,
         "full_name": name,
         "user_id": user_id,
         "created_at": created_at
      }
      user_profile = await create_user_profile(user_profile_data)
   
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
      "meter_code":"",
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

   context.user_data["session_id"] = session_id

   reply_message = welcome_menu(name)
   logger.info(f"{update.effective_chat.id}")
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=reply_message,
      reply_markup=markup,
   )

   return START_CHOICE

# Choosing the Distro
async def distro_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Ask the user for the distribution company"""
   query = update.callback_query
   await query.answer()

   distribution_companies = [
        "AEDC", "EEDC", "EKEDC", "IBEDCO", "IKEDC",
        "JED", "KAEDCO", "KEDCO", "PHED", "BEDC"
    ]

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
      chat_id=update.effective_chat.id,
      text=f"{options_menu()}",
      reply_markup=markup,
      )
   
   return CHOOSE_DISTRO

# Handling the meter distribution company
async def choose_distro(update: Update, context: CallbackContext) -> int:
   '''Handling the meter distribution choice from the choice input
   Collect meter number from user and Validate the collected meter number'''

   query = update.callback_query
   await query.answer()

   # save user input in context memory
   context.user_data["distribution_company"] = update.callback_query.data

   # Save to database
   session_id = context.user_data["session_id"]
   user_order_data = ["meter_distribution", update.callback_query.data]
   await update_user_order(user_order_data, session_id)

   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=f"{meter_number_menu()}",
      )
   return COLLECT_METER_NUMBER

# Verifying Meter Number
async def validate_meter_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Validate the collected meter number and get meter type"""
   user_input = update.message.text.strip()

   if not user_input.isdigit() or len(user_input) != 13:
      await update.message.reply_text("Invalid meter number. Please enter a 13-digit number.")
      
      return COLLECT_METER_NUMBER
   
   # Save meter number
   context.user_data["meter_number"] = user_input

   # Save to database
   session_id = context.user_data["session_id"]
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
      chat_id=update.effective_chat.id,
      text="Choose your meter type:",
      reply_markup=markup,
      )

   return CHOOSE_METER_TYPE

# Choose Meter Type
async def choose_meter_type(update: Update, context: CallbackContext) -> int:
   '''Collecting Meter type: Prepaid or Postpaid'''
   
   query = update.callback_query
   await query.answer()

   # save user meter type
   context.user_data["meter_type"] = update.callback_query.data

   # Check Meter type and distro for equivalent data
   if context.user_data["distribution_company"] == "AEDC" and update.callback_query.data == "prepaid":
      meter_code = "AEDC"
   elif context.user_data["distribution_company"] == "AEDC" and update.callback_query.data == "postpaid":
      meter_code = "AEDC_Postpaid"
   elif context.user_data["distribution_company"] == "EEDC" and update.callback_query.data == "prepaid":
      meter_code = "Enugu_Electricity_Distribution_Prepaid"
   elif context.user_data["distribution_company"] == "EEDC" and update.callback_query.data == "postpaid":
      meter_code = "Enugu_Electricity_Distribution_Postpaid"
   elif context.user_data["distribution_company"] == "EKEDC" and update.callback_query.data == "prepaid":
      meter_code = "Eko_Prepaid"
   elif context.user_data["distribution_company"] == "EKEDC" and update.callback_query.data == "postpaid":
      meter_code = "Eko_Postpaid"
   elif context.user_data["distribution_company"] == "IBEDCO" and update.callback_query.data == "prepaid":
      meter_code = "Ibadan_Disco_Prepaid"
   elif context.user_data["distribution_company"] == "IBEDCO" and update.callback_query.data == "postpaid":
      meter_code = "Ibadan_Disco_Postpaid"
   elif context.user_data["distribution_company"] == "IKEDC" and update.callback_query.data == "prepaid":
      meter_code = "Ikeja_Electric_Bill_Payment"
   elif context.user_data["distribution_company"] == "IKEDC" and update.callback_query.data == "postpaid":
      meter_code = "Ikeja_Token_Purchase"
   elif context.user_data["distribution_company"] == "JED" and update.callback_query.data == "prepaid":
      meter_code = "Jos_Disco"
   elif context.user_data["distribution_company"] == "JED" and update.callback_query.data == "postpaid":
      meter_code = "Jos_Disco_Postpaid"
   elif context.user_data["distribution_company"] == "AEDC" and update.callback_query.data == "prepaid":
      meter_code = "AEDC"
   elif context.user_data["distribution_company"] == "KAEDCO" and update.callback_query.data == "prepaid":
      meter_code = "Kaduna_Electricity_Disco"
   elif context.user_data["distribution_company"] == "KAEDCO" and update.callback_query.data == "postpaid":
      meter_code = "Kaduna_Electricity_Disco_Postpaid"
   elif context.user_data["distribution_company"] == "KEDCO" and update.callback_query.data == "prepaid":
      meter_code = "Kano_Electricity_Disco"
   elif context.user_data["distribution_company"] == "KEDCO" and update.callback_query.data == "postpaid":
      meter_code = "Kano_Electricity_Disco_Postpaid"
   elif context.user_data["distribution_company"] == "PHED" and update.callback_query.data == "prepaid":
      meter_code = "PhED_Electricity"
   elif context.user_data["distribution_company"] == "PHED" and update.callback_query.data == "postpaid":
      meter_code = "PH_Disco"
   elif context.user_data["distribution_company"] == "BEDC" and update.callback_query.data == "prepaid":
      meter_code = "BEDC"
   elif context.user_data["distribution_company"] == "BEDC" and update.callback_query.data == "postpaid":
      meter_code = "BEDC_Postpaid"
   
   # Save to database
   session_id = context.user_data["session_id"]
   user_order_data = ["meter_type", update.callback_query.data]
   user_meter_code = ["meter_code", meter_code]
   await update_user_order(user_order_data, session_id)
   await update_user_order(user_meter_code, session_id)

   reply_message = bill_amount_menu()

   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=reply_message,
      )
   return ELECTRICTY_AMOUNT

# Get Electricity Amount
async def get_electricity_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   '''Get Electricity Amount and validate it'''
   try:
      electricity_amount = int(update.message.text)
      if electricity_amount < 1000:
         await update.message.reply_text("❗Please enter an amount not below 1000:")
   
         return ELECTRICTY_AMOUNT

      # Save Electricity Amount 
      context.user_data["electricity_amount"] = electricity_amount
      
      # Save to database
      session_id = context.user_data["session_id"]
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
      user_meter_details = get_meter_details(
         meter_number=meter_number,
         meter_type=meter_type,
         disco=distro_code
      )
      logger.info(f"{user_meter_details}")
      if user_meter_details["status"] == "200":
         meter_owner = user_meter_details["meter_name"] # get from api call
         meter_address = user_meter_details["meter_address"] # get from api call
      else:
         await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text=order_failed(user_meter_info["_id"])
      )
         return ConversationHandler.END

      session_id = context.user_data["session_id"]
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
         chat_id=update.effective_chat.id,
         text=reply_text,
         reply_markup=markup,
         )
      
      return ORDER_CONFIRMATION
   except ValueError:
      await update.message.reply_text("❗Please enter a valid number:")
      return ELECTRICTY_AMOUNT

# Handling Order Confirmation
async def order_confirmation(update: Update, context: CallbackContext) -> int:
   ''' Handling order confirmation '''

   if update.callback_query.data == str(CANCEL_ORDER):
      reply_text = quit_chat()
   
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text=reply_text
      )
      return ConversationHandler.END
   
   elif update.callback_query.data == str(CONFIRM_ORDER):
      # Generate account details using API
      user = update.effective_user
      name = user.full_name
      
      session_id = context.user_data['session_id']
      user_order_details = await get_single_order(session_id)

      amount = user_order_details["user_amount"]
      
      generate_virtual_account = create_account(
         name=name,
         amount=amount
      )
      account_number = generate_virtual_account['Account Number']
      account_name = generate_virtual_account['Account Name']
      bank_name = generate_virtual_account['Bank']
      transaction_id = generate_virtual_account["ID"]
      payment_status = generate_virtual_account["Payment Status"]

      account_details = order_payment(amount, int(account_number), account_name, bank_name)

      await context.bot.send_message(chat_id=update.effective_chat.id, text=account_details)

      await update_user_order(["transaction_id", transaction_id], session_id)
      await update_user_order(["payment_confirmation", payment_status], session_id)
      
      return ConversationHandler.END
      

# Customer Support
async def customer_support_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Ask the user to chat the Customer Support on a Number"""
   query = update.callback_query
   await query.answer()

   await query.edit_message_text(
        "Welcome to Customer Support 🧑‍💻"
        "Reach Us on @musawakiliml. For your inquiries."
        "Thank You."
    )

   return START_CHOICE

# Cancel Chat Sessions
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Cancels and ends the conversation."""
   await update.message.reply_text(
        f"{quit_chat()}", reply_markup=ReplyKeyboardRemove()
   )

   return ConversationHandler.END

# Help Command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   '''Display Bot Help Menu To User'''
   await update.message.reply_text(
      f"{help_menu()}"
   )
   return ConversationHandler.END

# Customer Support Command
async def customer_support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Ask the user to chat the Customer Support on a Number"""
   
   await update.message.reply_text(
      "Welcome to EnergiEase Customer Support 🧑‍💻"
      "Reach Us on @musawakiliml. For your inquiries."
      "Thank You."
   )
   return ConversationHandler.END
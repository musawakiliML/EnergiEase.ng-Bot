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
   user = update.effective_user
   name = user.full_name
   reply_message = welcome_menu(name)
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
      await update.message.reply_text("Invalid meter number. Please enter a 11-digit number.")
      
      return COLLECT_METER_NUMBER
   
   # Save meter number
   context.user_data["meter_number"] = user_input

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
      distro = context.user_data['distribution_company']
      meter_number = context.user_data['meter_number']
      meter_type = context.user_data['meter_type']
      amount = context.user_data['electricity_amount']
      meter_owner = "John Doe" # get from api call
      meter_address = "No.1 Street One." # get from api call

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
      
      amount = context.user_data['electricity_amount']

      generate_virtual_account = create_account(
         name=name,
         amount=amount
      )
      account_number = generate_virtual_account['Account Number']
      account_name = generate_virtual_account['Account Name']
      bank_name = generate_virtual_account['Bank']

      account_details = order_payment(amount, account_number, account_name, bank_name)

      await context.bot.send_message(chat_id=update.effective_chat.id, text=account_details)

      # Perform API calls and confirm payment
      
      payment_status="successful"
      if payment_status == "successful":
         reply_text = order_confirmation_message(order_id="1123-1234-1243")
         
         await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

         # Generate unit tokens
         meter_number = "1233445554"
         meter_units = "12.8"
         token_status = "successful"
         meter_token = "889909877665444"
         if token_status == "successful":
            reply_text = order_successful(
               meter_number=meter_number,
               meter_token=meter_token,
               meter_unit=meter_units)
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=quit_chat())
            
            # End conversation and close chat session
            return ConversationHandler.END
         
         else:
            reply_text = order_failed(order_id="1123-1222-1123")
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=quit_chat())

            return ConversationHandler.END
         
      else: 
         reply_text = order_failed(order_id="1123-1222-1123")
         await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
         await context.bot.send_message(chat_id=update.effective_chat.id, text=quit_chat())
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
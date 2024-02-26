import os
from dotenv import load_dotenv

import logging

from telegram.ext import Application, ContextTypes

from telegram import (
   ReplyKeyboardMarkup,
   ReplyKeyboardRemove, Update,
   InlineKeyboardButton, InlineKeyboardMarkup
)

from telegram.ext import (
   CommandHandler, CallbackContext,
   ConversationHandler, MessageHandler,
   filters, Updater, CallbackQueryHandler
)

# Get Modules
from bot.message import *

# Enable Bot Token
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["Telegram_Bot_API"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

STARTCHOICE, CHOOSE_DISTRO, COLLECT_METER_NUMBER, CHOOSE_METER_TYPE, ELECTRICTY_AMOUNT = range(5)

# Define the Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Start the bot with a message to select an option when the command /start is issued."""
   reply_keyboard = [[
         InlineKeyboardButton(
            text="Buy Electricity⚡",
            callback_data="electricity"
         ),
         InlineKeyboardButton(
            text="Customer Support ☎️",
            callback_data="support"
         )
      ]]
   # reply_keyboard = [["Buy Electricity⚡", "Customer Support ☎️" ]]
   
   markup = InlineKeyboardMarkup(reply_keyboard)
   user = update.effective_user
   reply_message = welcome_menu(user.mention_html())
   await update.message.reply_html(
      rf"{reply_message}"
      "\n\n Send /cancel to stop talking to me.\n\n",
      reply_markup=markup,
   )

   return STARTCHOICE


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

   return STARTCHOICE

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
    
    await query.edit_message_text(text=f"{options_menu()}", reply_markup=markup)
   
    return CHOOSE_DISTRO


async def collect_meter_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   """Collect meter number from user."""
   query = update.callback_query
   await query.answer()
   
   context.user_data["distro"] = query.data

   context.user_data['next_state'] = CHOOSE_METER_TYPE

   await query.edit_message_text(text=f"{meter_number_menu()}")

   return COLLECT_METER_NUMBER

async def validate_meter_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate the collected meter number"""
    user_input = update.message.text.strip()

    if not user_input.isdigit() or len(user_input) != 13:
        await update.message.reply_text("Invalid meter number. Please enter a 13-digit number.")
        return COLLECT_METER_NUMBER

    # Valid meter number, store it in user_data
    context.user_data['meter_number'] = user_input

    # Move to the next state
    next_state = context.user_data.get('next_state', None)
    return next_state

async def choose_meter_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   reply_keyboard = [[
         InlineKeyboardButton(
            text="Prepaid",
            callback_data="prepaid"
         ),
         InlineKeyboardButton(
            text="Postpaid",
            callback_data="postpaid"
         )
      ]]
   
   query = update.callback_query
   await query.answer()
   context.user_data["meter_number"] = query.data

   markup = InlineKeyboardMarkup(reply_keyboard)
   reply_message = meter_type_menu()
   await update.message.reply_text(
      f"{reply_message}",
      reply_markup=markup,
   )

   return ELECTRICTY_AMOUNT

async def get_electricity_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
   pass



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        f"{quit_chat()}", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
   """Start the bot."""

   try:
      # Create the Application and pass it your bot's token.
      application = Application.builder().token("6755221703:AAFs7fZc7ATYUy-ZCLE9pJtToZQmitOqqc0").read_timeout(600).get_updates_read_timeout(600).write_timeout(600).get_updates_write_timeout(600).pool_timeout(600).get_updates_pool_timeout(600).connect_timeout(600).get_updates_connect_timeout(600).build()

      
      #  application.add_handler(CommandHandler("help", help_command))

      # Add conversation handler with the states STARTCHOICE, CHOOSE_DISTRO
      conv_handler = ConversationHandler(
         entry_points=[CommandHandler("start", start)],
         states={
               STARTCHOICE: [CallbackQueryHandler(distro_choice, pattern="^" + "electricity"),
                           CallbackQueryHandler(customer_support_choice, pattern="^" + "support")],
               CHOOSE_DISTRO: [CallbackQueryHandler(collect_meter_number, pattern=r'AEDC|EEDC|EKEDC|IBEDCO|IKEDC|JED|KAEDCO|KEDCO|PHED|BEDC')],
               COLLECT_METER_NUMBER:[MessageHandler(filters.TEXT & ~filters.COMMAND, validate_meter_number)],
               CHOOSE_METER_TYPE: [CallbackQueryHandler(choose_meter_type, pattern=r"prepaid|postpaid")]
         },
         fallbacks=[CommandHandler("cancel", cancel)],
      )

      application.add_handler(conv_handler)

      # Run the bot until the user presses Ctrl-C
      application.run_polling(allowed_updates=Update.ALL_TYPES)
   except Exception as e:
      return str(e)

if __name__ == "__main__":
    main()
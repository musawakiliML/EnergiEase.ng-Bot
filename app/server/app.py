import os
from dotenv import load_dotenv

import logging

from telegram.ext import Application, ContextTypes

from telegram import Update

from telegram.ext import (
   CommandHandler, ConversationHandler,
   MessageHandler, filters, CallbackQueryHandler
)

# Get Modules for chatbot messages
from app.server.bot.message import *

# Import Chatbot handlers
from app.server.bot.handlers import *

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# API Routes
from app.server.api.webhook import router as Fintava_router

# Enable Bot Token
load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_API"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Set the webhook path to the route you want to handle updates
WEBHOOK_PATH = "/telegram"

# URL of your FastAPI server
WEBHOOK_URL_STAGING = "https://living-optimal-seahorse.ngrok-free.app" + WEBHOOK_PATH
# WEBHOOK_URL_PRODUCTION = "https://energiease-ng-bot.onrender.com" + WEBHOOK_PATH

# WEBHOOK_URL_PRODUCTION_VERCEL = "https://energi-ease-ng-bot.vercel.app" + WEBHOOK_PATH



# Configuring the Main Bot Instance
application = Application.builder().token(TELEGRAM_BOT_TOKEN).read_timeout(600).get_updates_read_timeout(600).write_timeout(600).get_updates_write_timeout(600).pool_timeout(600).get_updates_pool_timeout(600).connect_timeout(600).get_updates_connect_timeout(600).build()

# Add conversation handler with the states STARTCHOICE, CHOOSE_DISTRO
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START_CHOICE: [
            # CallbackQueryHandler(distro_choice, pattern="^" + "electricity"),
            CallbackQueryHandler(distro_choice, pattern=str(BUY_ELECTRICITY)),
            CallbackQueryHandler(customer_support_choice, pattern=str(SUPPORT))],

        CHOOSE_DISTRO: [
            CallbackQueryHandler(choose_distro, pattern=r'AEDC|EEDC|EKEDC|IBEDCO|IKEDC|JED|KAEDCO|KEDCO|PHED|BEDC')],
        
        COLLECT_METER_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_meter_number)],
        
        CHOOSE_METER_TYPE:[CallbackQueryHandler(choose_meter_type, pattern=r"prepaid|postpaid")],

        ELECTRICTY_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_electricity_amount)],

        ORDER_CONFIRMATION: [CallbackQueryHandler(order_confirmation)]
    },
    fallbacks=[CommandHandler("help", help)]
)

# Configure Conversation Handlers
application.add_handler(conv_handler)
help_command = CommandHandler("help", help)
cancel_command = CommandHandler("cancel", cancel)
customer_support = CommandHandler("support", customer_support_command)

# Add Command handlers
application.add_handler(help_command)
application.add_handler(customer_support)
application.add_handler(cancel_command)

# Set up the webhook
@asynccontextmanager
async def lifespan(_: FastAPI):
    await application.bot.set_webhook(WEBHOOK_URL_STAGING, allowed_updates=Update.ALL_TYPES)
    async with application:
        await application.start()
        yield
        await application.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Fintava_router, tags=["Fintava Webhook"], prefix='/fintavawebhook')


# Configure telegram bot webhook
@app.post(WEBHOOK_PATH)
async def receive_update(request: Request):
    data = await request.json()
    logger.info(data)
    # print(data)
    try:
        update = Update.de_json(data, application.bot)
        await application.update_queue.put(update)
    except Exception as e:
        logger.info(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"status": "ok"})

@app.get("/api")
async def start_bot():
    return {"message":f"Welcome to EnergiEase: Your Journey to Smarter Energy Choices"}
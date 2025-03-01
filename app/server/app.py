import os
import logging
from dotenv import load_dotenv

import httpx
import asyncio
from datetime import datetime

from telegram.ext import Application, ContextTypes

from telegram import Update

from telegram.ext import (
   filters,
   CommandHandler,
   MessageHandler,
   ConversationHandler,
   CallbackQueryHandler
   )

# Get Modules for chatbot messages
from app.server.bot.message import *

# Import Chatbot handlers
from app.server.bot.handlers import *

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# API Routes
from app.server.api.webhook import router as Fintava_router
from app.server.api.dashboard import router as Dashboard_router
from app.server.api.user import router as User_router
from app.server.api.paystack import router as Paystack_router
from app.server.api.whatsapp import router as Whatsapp_router
from app.server.api.whatsappflows import router as Whatsapp_flow_router

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

# Webhook path to the route to handle updates
WEBHOOK_PATH = "/telegram"

# URL of FastAPI server
if os.environ['DEBUG'] == "True":
    WEBHOOK_URL_STAGING = "https://living-optimal-seahorse.ngrok-free.app" + WEBHOOK_PATH
elif os.environ['DEBUG'] == "False":
    WEBHOOK_URL_PRODUCTION = "https://energiease-ng-bot.onrender.com" + WEBHOOK_PATH
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
            CallbackQueryHandler(choose_distro,
                                 pattern=r'AEDC|EEDC|EKEDC|IBEDCO|IKEDC|JED|KAEDCO|KEDCO|PHED|BEDC')],
        
        COLLECT_METER_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_meter_number)],
        
        CHOOSE_METER_TYPE:[CallbackQueryHandler(choose_meter_type, pattern=r"prepaid|postpaid")],
        
        ELECTRICTY_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_electricity_amount)],
        
        ORDER_CONFIRMATION: [CallbackQueryHandler(order_confirmation)]
    },
    
    fallbacks=[CommandHandler("start", start), CommandHandler("cancel", cancel)]
)

# Configure Conversation Handlers
application.add_handler(conv_handler)
help_command = CommandHandler("help", help)
# cancel_command = CommandHandler("cancel", cancel)
customer_support = CommandHandler("support", customer_support_command)

# Add Command handlers
application.add_handler(help_command)
application.add_handler(customer_support)
# application.add_handler(cancel_command)


# Render Background Tasks
RENDER_URL = "https://energiease-ng-bot.onrender.com/"
RELOAD_INTERVAL = 600 # Interval in seconds (15 minutes)

async def reload_website():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(RENDER_URL)
            print(f"Reloaded at {datetime.utcnow().isoformat()}: Status Code {response.status_code}")
        except Exception as e:
            print(f"Error reloading at {datetime.utcnow().isoformat()}: {str(e)}")

async def keep_alive_task():
    while True:
        await reload_website()
        await asyncio.sleep(RELOAD_INTERVAL)

# Set up the webhook
# @asynccontextmanager
# async def lifespan(_: FastAPI):
    
#     await application.bot.set_webhook(WEBHOOK_URL_PRODUCTION, allowed_updates=Update.ALL_TYPES)
#     async with application:
#         await application.start()
        
#         # Start the background task to keep the Render app alive
#         keep_alive = asyncio.create_task(keep_alive_task())
        
#         yield
        
#         await application.stop()
        
#         # Clean up: Stop the Telegram bot and cancel the keep-alive task
#         keep_alive.cancel()
#         try:
#             await keep_alive
#         except asyncio.CancelledError:
#             print("Keep-alive task cancelled during shutdown.")

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Declare all routes
app.include_router(Whatsapp_router, tags=["WhatsApp Webhook"], prefix='/whatsapphook')
app.include_router(Whatsapp_flow_router, tags=['WhatsApp Flow Webhooks'], prefix='/whatsappflow')
app.include_router(Fintava_router, tags=["Fintava Webhook"], prefix='/fintavawebhook')
app.include_router(Paystack_router, tags=["Paystack Webhook"], prefix='/paystackwebhook')
app.include_router(Dashboard_router, tags=["Dashboard Views"], prefix='/dashboard')
app.include_router(User_router, tags=['User Authentication'], prefix='/user')


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
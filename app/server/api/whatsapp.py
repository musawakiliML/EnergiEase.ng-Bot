from fastapi import FastAPI, APIRouter, Query, status, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from app.server.bot.whatsapp_handlers import handle_whatsapp_chat


import random
from datetime import datetime

from app.server.bot.whatsapp_messages import *
from app.server.utils.whatsapp import send_whatsapp_message_normal, send_whatsapp_message_buttons

router = APIRouter()

@router.get("/verify/")
async def buy_electricity_webhook_verification(hub_mode: str = Query(..., alias='hub.mode'), verify_token: str = Query(..., alias='hub.verify_token'), challenge: int = Query(..., alias='hub.challenge')):
   
   VERIFY_TOKEN = "buyelectricitybot"

   if hub_mode == 'subscribe' and verify_token == VERIFY_TOKEN:
      #return {'hub.challenge': challenge}
      return JSONResponse(content=challenge, status_code=status.HTTP_200_OK)
   else:
      raise HTTPException(detail="Forbidden", status_code=status.HTTP_403_FORBIDDEN)

@router.post("/verify/", status_code=status.HTTP_200_OK)
async def buy_electricity_webhook(request: Request):
   response = await request.json()
   print(response)
   if ('object' in response) and ('entry' in response):
      if response['object'] == 'whatsapp_business_account':
         try:
            for entry in response['entry']:
               phone_number = entry['changes'][0]['value']['metadata']['display_phone_number']
               phone_id = entry['changes'][0]['value']['metadata']['phone_number_id']
               profile_name = entry['changes'][0]['value']['contacts'][0]['profile']['name']
               whatsapp_id = entry['changes'][0]['value']['contacts'][0]['wa_id']
               from_id = entry['changes'][0]['value']['messages'][0]['from']
               message_id = entry['changes'][0]['value']['messages'][0]['id']
               timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
               text = entry['changes'][0]['value']['messages'][0]['text']['body']
               
               opening = ['hi', 'Hi', 'Hello', 'Hello', 'Hey', 'hey']
               opening_msg = random.choice(opening).upper()
               print("here")
               if text in opening or text:
                    message = welcome_menu(opening_msg, profile_name)
                    send_whatsapp_message_buttons(from_id, message)
                    print("passed")
            #    await handle_whatsapp_chat(from_id, text, profile_name, phone_id)

            return JSONResponse(content={"message":"Success"}, status_code=status.HTTP_200_OK)   
         except Exception as e:
            # return JSONResponse(content={"message":"Success"}, status_code=status.HTTP_200_OK)
            # raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # raise str(e)
            pass
   return JSONResponse(content={"message":"Success"}, status_code=status.HTTP_200_OK)
         # except Exception as e:
         #    raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



# {'object': 'whatsapp_business_account', 'entry': [{'id': '101864066083784', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '15550881730', 'phone_number_id': '100753659532289'}, 'contacts': [{'profile': {'name': 'Mind Colony LTD'}, 'wa_id': '2348102778677'}], 'messages': [{'context': {'from': '15550881730', 'id': 'wamid.HBgNMjM0ODEwMjc3ODY3NxUCABEYEkE3RDc0NkE3Q0FBMTNCQTEyQQA='}, 'from': '2348102778677', 'id': 'wamid.HBgNMjM0ODEwMjc3ODY3NxUCABIYIDdBMTlGRTA2QzM4OTg5RERDODU3OUVBODk3NDJEQUUyAA==', 'timestamp': '1726141993', 'type': 'interactive', 'interactive': {'type': 'button_reply', 'button_reply': {'id': 'buy_electricity', 'title': 'Buy Electricity ⚡'}}}]}, 'field': 'messages'}]}]}
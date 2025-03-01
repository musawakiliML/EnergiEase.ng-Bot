import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def send_whatsapp_message(recipient_number: str, body: str):

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    phone_number = os.environ["TWILIO_PHONE_NUMBER"]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_="whatsapp:" + phone_number,
        to="whatsapp:" + recipient_number,
    )
    # print(message.body)
    return message.body







# def send_whatsapp_message_normal(phone_number, message):
#     headers = {"Authorization": os.environ['WHATSAPP_TOKEN']}
#     payload = {
#         "messaging_product": "whatsapp",
#         "reciepient_type": "individual",
#         "to": phone_number,
#         "type": "text",
#         "text": {
#             "body": message
#         }
#     }
#     response = requests.post(os.environ['WHATSAPP_URL'],
#                              headers=headers, json=payload)
#     response_json = response.json()
#     return response_json


# def send_whatsapp_message_buttons(phone_number, message):
#     headers = {"Authorization": os.environ['WHATSAPP_TOKEN']}
#     payload = {
#         "messaging_product": "whatsapp",
#         "reciepient_type": "individual",
#         "to": phone_number,
#         "type": "interactive",
#         "interactive": {
#             "type": "button",
#             "body": {
#                 "text": message
#             },
#             "action": {
#                 "buttons": [
#                     {"type": "reply",
#                      "reply": {"id": "buy_electricity", "title": "Buy Electricity ⚡"}
#                     }
#                 ]
#             }
#         }
#     }
#     response = requests.post(os.environ['WHATSAPP_URL'],
#                              headers=headers, json=payload)
#     response_json = response.json()
#     print(response_json)
#     return response_json


# # test = send_whatsapp_message_normal("2348102778677", "Hello, Welcome to EnergiEase!")

# # print(test)

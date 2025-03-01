import os

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio Message Handler

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


# Whatsapp Message Handlers


def send_whatsapp_message_normal(phone_number, message):
    headers = {"Authorization": os.environ["WHATSAPP_TOKEN"]}
    payload = {
        "messaging_product": "whatsapp",
        "reciepient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(os.environ["WHATSAPP_URL"], headers=headers, json=payload)
    response_json = response.json()
    return response_json


def send_whatsapp_message_opening_buttons(phone_number, name):
    headers = {"Authorization": os.environ["WHATSAPP_TOKEN"]}
    payload = {
        "messaging_product": "whatsapp",
        "reciepient_type": "individual",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {"type": "text", "text": "I'm EnergiEase Bot"},
            "body": {
                "text": f"Hi, {name}! Nice to meet you, What would you like to do today?"
            },
            "footer": {"text": "Powered By Mind Colony™"},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {"id": "buy_electricity", "title": "Buy Electricity"},
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "customer_support",
                            "title": "Customer Support",
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {"id": "ktc_meter", "title": "Meter KTC"},
                    },
                ]
            },
        },
    }
    response = requests.post(os.environ["WHATSAPP_URL"], headers=headers, json=payload)
    response_json = response.json()
    return response_json


# Send Disco List Plans

def send_disco_list_message(phone_number: str) -> dict:

    headers = {
        "Authorization": os.environ["WHATSAPP_TOKEN"],
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "Discos List"},
            "body": {"text": "That's perfect!! 👍 Choose from the Distribution Companies available below:"},
            "footer": {"text": "Powered By Mind Colony™"},
            "action": {
                "button": "Select Disco",
                "sections": [
                    {
                        "title": "Discos",
                        "rows": [
                            {
                                "id": "aedc",
                                "title": "AEDC",
                            },
                            {
                                "id": "eedc",
                                "title": "EEDC",
                            },
                            {
                               "id": "ekedc",
                                "title": "EKEDC",
                            },
                            {
                                "id": "ibedco",
                                "title": "IBEDCO",
                            },
                            {
                                "id": "ikedc",
                                "title": "IKEDC",
                            },
                            {
                                "id": "jed",
                                "title": "JED",
                            },
                            {
                                "id": "kaedco",
                                "title": "KAEDCO",
                            },
                            {
                                "id": "kedco",
                                "title": "KEDCO",
                            },
                            {
                                "id": "phed",
                                "title": "PHED",
                            },
                            {
                                "id": "bedc",
                                "title": "BEDC",
                            },
                        ],
                    },
                ],
            },
        },
    }

    response = requests.post(
        os.environ["WHATSAPP_URL"], headers=headers, json=payload)
    response_json = response.json()
    return response_json

# Send meter type buttons

def send_meter_type_buttons(phone_number):
    headers = {"Authorization": os.environ["WHATSAPP_TOKEN"]}
    payload = {
        "messaging_product": "whatsapp",
        "reciepient_type": "individual",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {"type": "text", "text": "Meter Type"},
            "body": {
                "text": "Please Select Your Meter Type:"
            },
            "footer": {"text": "Powered By Mind Colony™"},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {"id": "prepaid", "title": "Prepaid"},
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "postpaid",
                            "title": "Postpaid",
                        },
                    }
                ]
            },
        },
    }
    response = requests.post(os.environ["WHATSAPP_URL"], headers=headers, json=payload)
    response_json = response.json()
    return response_json
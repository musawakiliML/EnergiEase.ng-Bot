import logging

from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse

from app.server.bot.whatsapp_handlers import handle_whatsapp_chat

router = APIRouter()

logging.basicConfig(level=logging.INFO)

# Twilio Webhook


@router.post("/bot/", status_code=status.HTTP_200_OK)
async def twilio_webhook(request: Request):
    """Twilio Request Webhook

    Args:
        request (Request): twilio response
    """

    try:
        data = await request.form()

        body = data.get("Body", None)
        profile_name = data.get("ProfileName", None)
        whatsapp_id = data.get("WaId", None)
        phone_number = str(data.get("From", None)).split(":")[-1]

        #   print(data)

        # Chatbot Logic Handler
        await handle_whatsapp_chat(phone_number, body, profile_name, whatsapp_id)

        return JSONResponse(
            content={"message": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        print(str(e))
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# WhatsApp Based Webhooks


@router.get("/")
async def energieasebot_webhook_verification(
    hub_mode: str = Query(..., alias="hub.mode"),
    verify_token: str = Query(..., alias="hub.verify_token"),
    challenge: int = Query(..., alias="hub.challenge"),
):

    VERIFY_TOKEN = "energieasebot"

    if hub_mode == "subscribe" and verify_token == VERIFY_TOKEN:

        return JSONResponse(content=challenge, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(detail="Forbidden", status_code=status.HTTP_403_FORBIDDEN)


@router.post("/", status_code=status.HTTP_200_OK)
async def energieasebot_webhook(request: Request):
    response = await request.json()
    print(response)
    if ("object" in response) and ("entry" in response):
        if response["object"] == "whatsapp_business_account":
            try:
                if (
                    response["entry"][0]["changes"][0]["value"].get("messages")
                ) is not None:
                    profile_name = response["entry"][0]["changes"][0]["value"][
                        "contacts"
                    ][0]["profile"]["name"]
                    phone_id = response["entry"][0]["changes"][0]["value"]["metadata"][
                        "phone_number_id"
                    ]
                    from_id = response["entry"][0]["changes"][0]["value"]["messages"][
                        0
                    ]["from"]

                    # Get User Opening Message, Amount and Meter Number
                    if (
                        response["entry"][0]["changes"][0]["value"]["messages"][0].get(
                            "text"
                        )
                    ) is not None:
                        text = response["entry"][0]["changes"][0]["value"]["messages"][
                            0
                        ]["text"]["body"]

                        # Pass text to whatsapp handler for processing
                        await handle_whatsapp_chat(
                            phonenumber=from_id,
                            text=text,
                            profilename=profile_name,
                            phoneid=phone_id,
                        )

                    # Get User Selection Using Button
                    elif (
                        response["entry"][0]["changes"][0]["value"]["messages"][0][
                            "interactive"
                        ].get("type")
                    ) == "button_reply":
                        user_input = response["entry"][0]["changes"][0]["value"][
                            "messages"
                        ][0]["interactive"]["button_reply"]["title"]

                        # Pass user input to whatsapp handler for processing
                        await handle_whatsapp_chat(
                            phonenumber=from_id,
                            text=user_input,
                            profilename=profile_name,
                            phoneid=phone_id,
                        )

                    # Get User List Selection
                    elif (
                        response["entry"][0]["changes"][0]["value"]["messages"][0][
                            "interactive"
                        ].get("type")
                    ) == "list_reply":
                        user_input = response["entry"][0]["changes"][0]["value"][
                            "messages"
                        ][0]["interactive"]["list_reply"]["title"]

                        # Pass user input to whatsapp handler for processing
                        await handle_whatsapp_chat(
                            phonenumber=from_id,
                            text=user_input,
                            profilename=profile_name,
                            phoneid=phone_id,
                        )
                    return JSONResponse(
                        content={"message": "Success"}, status_code=status.HTTP_200_OK
                    )
            except Exception as e:
                logging.info(f"Error: {e}")
    return JSONResponse(content={"message": "Success"}, status_code=status.HTTP_200_OK)

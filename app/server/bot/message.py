from emoji import emojize


def welcome_menu(profile_name: str):
    message = f"Hi\\!, {profile_name}, Nice to Meet You, I'm EnergiEase Bot {emojize(':bulb:', language='alias')} from Mind Colony\\!\nWhat would you like to do today? \nPlease reply by choosing an option\\.\n\n Send /cancel to stop talking to me\\.\n\n"

    return message


def options_menu():
    message = f"That's perfect!! {emojize(':thumbsup:', language='alias')} Choose from the Distribution Companies available below:🔋\n\n Please choose an option."

    return message


def meter_number_menu():
    message = f"Please enter your meter number {emojize(':pager:', language='alias')}:"

    return message


def meter_type_menu():
    message = f"Please Select Your Meter Type:\n{emojize(':one:', language='alias')} Prepaid\n{emojize(':two:', language='alias')} Postpaid"
    return message


def bill_amount_menu():
    message = f"Great! how much {emojize(':battery:', language='alias')} electricity unit (in naira) do you want to buy {emojize(':dollar:', language='alias')}?\n\n{emojize(':heavy_exclamation_mark:', language='alias')}Note: The minimun order amount should be N1000.0\nA service fee of N100 will be added to the amount."

    return message


def order_summary(owner: str, amount: str, meter_number: str, package: str, address: str):
    message = f"Hurray!, Here is your order summary:\n\n\t👤 Meter Owner:{owner}\n\t🔢 Meter No:`{meter_number}`\n\t📍 Address: {address}\n\t📦 Package: {package}\n\n\t💵 Amount {emojize(':dollar:', language='alias')}: ₦ {amount}\n\tService Fee: ₦ 100\n\nChoose an option:"

    return message


def order_payment(amount: str, accountnumber: str, accountname: str, bankname: str):
    message = f"Fabulous!! Please send 💵 {int(amount) + 100} to:\n\n\tAccount number:`{accountnumber}`\n\tAccount name: {accountname}\n\tBank name: {bankname}\n\n\tAccount Number Expires In: 30mins\n\n ⌛ Your request would be processed automatically once we received your payment."

    return message


def order_confirmation_message(order_id: str):
    message = f"Fantastic!! Your order has been received.✅\n\n\tOrder Id: `{order_id}`\n⌛ We are processing it."

    return message


def order_successful(meter_unit: str, meter_number: str, meter_token: str):
    message = f"Your Order was successful!! 🎉\n You can get the details below:\n\n\tToken: {meter_token}\n\tUnits: {meter_unit}\n\tMeter Number: {meter_number}\n\nThank you for choosing EnergiEase!🤗"

    return message


def order_failed(order_id: str):
    message = f"OOPs ❌ Your order has failed!!\n Please Contact Support with your Order Id:`{order_id}`, or send email to support@energieasebot.ng.\nJust type '/start' 👋 To start a new conversation.. \nThank you for choosing EnergiEase!🤗"
    return message


def customer_support():
    message = f"Welcome to Customer Support. Please Whats your issue Today? Write to us.."
    return message


def quit_chat():
    message = "Thank You For using the Bot 🤗, See you next time 👋.\n Just type '/start' 👋 To start a conversation."
    return message

def cancel_order(order_id: str):
    message = f"Your Order with ID:`{order_id}` has been cancelled ❌.\n\nThank You For using the Bot 🤗, See you next time 👋.\n Just type '/start' 👋 To start a conversation."
    return message

def help_menu():
    message = "Welcome to Help Section of EnergiEase 🔋\nTo Buy Electricity Unit type /start\nTo End a chat session type /cancel\nTo Reach Customer type /support\nTo Get Help type /help"
    return message

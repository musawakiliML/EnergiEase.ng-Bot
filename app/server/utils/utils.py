from app.server.database.crud import create_meter_details, get_all_orders

# Create Meter Details Collection


async def create_meter_details_collection():
    """Create Meter Details Collection"""

    try:
        # Meter Details Data
        meter_details_data_list = []

        # Get all orders
        orders = await get_all_orders()

        for order in orders["data"]:

            if order["user_meter_number"] == "":
                continue
            else:
                meter_details_data = {
                    "meter_owner": order["meter_owner"],
                    "meter_number": order["user_meter_number"],
                    "meter_address": order["meter_address"],
                    "meter_package": order["meter_type"],
                    "meter_distributions": order["meter_distribution"],
                }

                meter_details_data_list.append(meter_details_data)

        # Create Meter Details
        await create_meter_details(meter_details_data_list)

    except Exception as e:
        return {"message": f"{str(e)}"}


# test = create_meter_details_collection()
# print(test)

from datetime import datetime, timedelta
from my_custom_data_handler import MyCustomDataHandler
from my_custom_flight_explorer import MyCustomFlightExplorer
from my_notification_service import MyCustomNotificationService

MY_CUSTOM_ORIGIN_CITY_IATA = "LON"

my_custom_data_handler = MyCustomDataHandler()
my_custom_flight_explorer = MyCustomFlightExplorer()
my_custom_notification_service = MyCustomNotificationService()

my_custom_sheet_data = my_custom_data_handler.fetch_custom_data()

if my_custom_sheet_data[0]["iataCode"] == "":
    my_custom_city_names = [row["city"] for row in my_custom_sheet_data]
    my_custom_data_handler.city_codes = my_custom_flight_explorer.get_custom_destination_codes(my_custom_city_names)
    my_custom_data_handler.update_custom_codes()
    my_custom_sheet_data = my_custom_data_handler.fetch_custom_data()

    if my_custom_sheet_data[0]["iataCode"] == "":
        my_custom_city_names = [row["city"] for row in my_custom_sheet_data]
        my_custom_data_handler.city_codes = my_custom_flight_explorer.get_custom_destination_codes(my_custom_city_names)
        my_custom_data_handler.update_custom_codes()
        my_custom_sheet_data = my_custom_data_handler.fetch_custom_data()

    my_custom_destinations = {
        data["iataCode"]: {
            "id": data["id"],
            "city": data["city"],
            "price": data["lowestPrice"]
        } for data in my_custom_sheet_data}

    my_custom_tomorrow = datetime.now() + timedelta(days=1)
    my_custom_six_month_from_today = datetime.now() + timedelta(days=6 * 30)

    for my_custom_destination_code in my_custom_destinations:
        my_custom_flight = my_custom_flight_explorer.explore_custom_flights(
            MY_CUSTOM_ORIGIN_CITY_IATA,
            my_custom_destination_code,
            from_time=my_custom_tomorrow,
            to_time=my_custom_six_month_from_today
        )
        print(my_custom_flight.price)
        if my_custom_flight is None:
            continue

        if my_custom_flight.price < my_custom_destinations[my_custom_destination_code]["price"]:
            my_custom_users = my_custom_data_handler.retrieve_custom_emails()
            my_custom_emails = [row["email"] for row in my_custom_users]
            my_custom_names = [row["firstName"] for row in my_custom_users]

            my_custom_message = f"Low price alert! Only £{my_custom_flight.price} to fly from {my_custom_flight.origin_city}-{my_custom_flight.origin_airport} to {my_custom_flight.destination_city}-{my_custom_flight.destination_airport}, from {my_custom_flight.out_date} to {my_custom_flight.return_date}."

            if my_custom_flight.stop_overs > 0:
                my_custom_message += f"\nFlight has {my_custom_flight.stop_overs} stop over, via {my_custom_flight.via_city}."

            my_custom_notification_service.send_emails(my_custom_emails, my_custom_message)
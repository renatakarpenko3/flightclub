import requests
MY_SHEET_USERS_ENDPOINT = "SHEET USERS ENDPOINT"
MY_SHEET_PRICES_ENDPOINT = "SHEET PRICES ENDPOINT"


class MyCustomDataHandler:

    def __init__(self):
        self.my_custom_data = {}

    def fetch_custom_data(self):
        response = requests.get(url=MY_SHEET_PRICES_ENDPOINT)
        data = response.json()
        self.my_custom_data = data["prices"]
        return self.my_custom_data

    def update_custom_codes(self):
        for city in self.my_custom_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{MY_SHEET_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def retrieve_custom_emails(self):
        users_endpoint = MY_SHEET_USERS_ENDPOINT
        response = requests.get(url=users_endpoint)
        data = response.json()
        self.custom_user_data = data["users"]
        return self.custom_user_data

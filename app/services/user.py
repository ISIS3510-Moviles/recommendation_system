import requests
from collections import namedtuple

# User Model
User = namedtuple("User", ["id", "tags", "subscribed_restaurants", "reservations", "saved_products", "comments"])

def get_user():
    url = "https://gist.githubusercontent.com/wareval0/56ae63f017985a748e84bd27ba8ba895/raw/4c8b15f112187324f909af72747cc91deac16de1/users_campus_bites.json"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        user = User(
            id=user_data["id"],
            tags=user_data["tags"],
            subscribed_restaurants=user_data["subscribed_restaurants"],
            reservations=user_data["reservations"],
            saved_products=user_data["saved_products"],
            comments=user_data["comments"]
        )
        return user
    else:
        print(f"Error fetching user data: {response.status_code}")
        return None
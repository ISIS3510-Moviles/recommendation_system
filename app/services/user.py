import requests
from collections import namedtuple

# User Model
User = namedtuple("User", ["id", "tags", "subscribed_restaurants", "reservations", "saved_products", "comments"])

def get_user(user_id):
    url = f"https://mobiledev.chickenkiller.com/user/tag/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        user = User(
            id=user_data["id"],
            tags=user_data.get("tags", []),
            subscribed_restaurants=user_data.get("subscribed_restaurants", []),
            reservations=user_data.get("reservations", []),
            saved_products=user_data.get("saved_products", []),
            comments=user_data.get("comments", [])
        )
        return user
    else:
        print(f"Error fetching user data: {response.status_code}")
        return None
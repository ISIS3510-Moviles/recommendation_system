import pandas as pd
import requests
from collections import namedtuple

# Restaurant Model
Restaurant = namedtuple("Restaurant", ["id", "name", "tags", "rating", "comments", "reservations", "subscribers"])
def get_restaurants():
    url = "https://mobiledev.chickenkiller.com/restaurant/full/"
    response = requests.get(url)
    if response.status_code == 200:
        restaurant_data = response.json()
        data = []
        for r in restaurant_data:
            restaurant = Restaurant(
                id=r["id"],
                name=r["name"],
                tags=r["tags"],
                rating=r.get("rating", 3.5),
                comments=r.get("comments", []),
                reservations=r.get("reservations", []),
                subscribers=r.get("subscribers", [])
            )
            restaurant_dict = restaurant._asdict()
            restaurant_dict["popularity"] = calculate_popularity(restaurant_dict)
            data.append(restaurant_dict)
    else:
        print(f"Error fetching restaurant data: {response.status_code}")
        return []

    return pd.DataFrame(data)

def calculate_popularity(r):
    return (
        len(r.get("comments", [])) * 1.0 +
        len(r.get("reservations", [])) * 1.2 +
        len(r.get("subscribers", [])) * 0.8 +
        len(r.get("visits", [])) * 1.0
    )

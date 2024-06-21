import requests
from geopy.distance import distance


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()[
        'response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(client_coordinates,
                 restaurant_lat,
                 restaurant_long):
    restaurant_coordinates = (
        float(restaurant_lat),
        float(restaurant_long))
    dist = distance(client_coordinates,
                    restaurant_coordinates).km
    return round(dist, 2)

import requests
from geopy.distance import distance

from django.conf import settings
from environs import Env


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(client_coordinates,apikey,rest_address):
    restaurant_coordinates = fetch_coordinates(
                apikey, rest_address)
    dist = distance(client_coordinates,
                    restaurant_coordinates).km
    return round(dist,2)

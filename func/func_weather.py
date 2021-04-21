# this module contains the functions necessary to receive weather on request from the user

from const.config import WEAHER_URL
import json
import requests


def parse_weather(data: json) -> str:
    'this function generates a message for the user with the results of a weather request for the city'
    for elem in data['weather']:
        weather_state = elem['description']
    city = data['name']
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    weather_in_city = f'''
    Погода в городе {city}:
    Температура: {temp} °С
    Условия: {weather_state}
    Скорость ветра: {wind_speed} м/с'''
    return weather_in_city


def get_weather(city: str) -> str:
    'this is a function for getting weather by city name'
    res = requests.get(WEAHER_URL.format(city=city))
    if res.status_code != 200:
        return 'город не найден'
    data = json.loads(res.content)
    return parse_weather(data)

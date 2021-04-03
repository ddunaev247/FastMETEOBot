import flask
from flask import Flask, request, Response
import requests
from config import TOKEN, WEAHER_URL
import message_bot
import telebot
import json


bot = telebot.TeleBot(TOKEN)


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    if request.method == 'POST':
        return Response('ok', status=200)
    else:
        return ''

@bot.message_handler(commands=['start', 'help'])
def start_messege(message):
    bot.send_message(message.chat.id, message_bot.start)

def parse_weather(data):
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
    print( f'{city}: Температура: {temp}, Описание:{weather_state}') #проверка для отладки
    return weather_in_city


def get_weather(city):
    res = requests.get(WEAHER_URL.format(city=city))
    if res.status_code != 200:
        return 'город не найден'
    data = json.loads(res.content)
    return parse_weather(data)


@bot.message_handler(content_types=['text'])
def send_text(message):
    query = get_weather(message.text)
    bot.send_message(message.chat.id, query)



if __name__ == '__main__':
    app.run()

import flask
from flask import Flask, request, Response
import requests
from config import TOKEN, WEAHER_URL
import message_bot
import telebot
from telebot import types
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


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button_weather_in_city = types.KeyboardButton('/Погода')
    button_shedule = types.KeyboardButton('/Расписание')
    keyboard.add(button_weather_in_city)
    keyboard.add(button_shedule)
    bot.send_message(message.chat.id, message_bot.start, reply_markup=keyboard)

    keyboard_inline = types.InlineKeyboardMarkup()
    button_replay = types.InlineKeyboardButton(text='Заново', callback_data='/Погода')
    keyboard_inline.add(button_replay)

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

@bot.message_handler(commands=['Погода'])
def command_weather(message):
    msg = bot.send_message(message.chat.id,'Введи название города')
    bot.register_next_step_handler(msg,command_weather_return )

def command_weather_return(message):
    button_replay = types.InlineKeyboardButton(text='Заново', callback_data='/Погода')
    keyboard_inline = types.InlineKeyboardMarkup().add(button_replay)
    result = get_weather(message.text)
    bot.send_message(message.chat.id, result, reply_markup=keyboard_inline)

@bot.callback_query_handler(lambda c: c.data == '/Погода')
def callback_weather(callback_query):
    msg = bot.send_message(callback_query.from_user.id,'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return)


#@bot.message_handler(content_types=['text'])
#def send_text(message):
    #query = get_weather(message.text)
    #bot.send_message(message.chat.id, query)






if __name__ == '__main__':
    app.run()

import flask
from flask import Flask, request, Response
import requests
from config import TOKEN, WEAHER_URL
import message_bot
import telebot
import json
from keyboards import keyboard_menu, keyboard_inline, keyboard_schedule, keyboard_schedule_delete
from bot_db import *
import bot_db


bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def run_bot():
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
    bot.send_message(message.chat.id, message_bot.start, reply_markup=keyboard_menu)


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
    print(f'{city}: Температура: {temp}, Описание:{weather_state}') #проверка для отладки
    return weather_in_city


def get_weather(city):
    res = requests.get(WEAHER_URL.format(city=city))
    if res.status_code != 200:
        return 'город не найден'
    data = json.loads(res.content)
    return parse_weather(data)

@bot.message_handler(commands=['Погода'])
def command_weather(message):

    msg = bot.send_message(message.chat.id, 'Введи название города')
    bot.register_next_step_handler(msg,command_weather_return )

def command_weather_return(message):
    result = get_weather(message.text)
    bot.send_message(message.chat.id, result, reply_markup=keyboard_inline)

@bot.callback_query_handler(lambda c: c.data == '/Погода')
def callback_weather(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return)


@bot.message_handler(commands=['Расписание'])
def command_schedule(message):
    bot.send_message(message.chat.id, message_bot.shedule, reply_markup=keyboard_schedule)

@bot.callback_query_handler(lambda c: c.data == 'set')
def set_schedule(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, '1-ое: Введи название города')
    bot.register_next_step_handler(msg, user_city)

def user_city(message):
    msg = bot.send_message(message.chat.id, '2-ое: Введи время')
    bot_db.info.append(message.from_user.id)
    bot_db.info.append(message.text)
    bot.register_next_step_handler(msg, user_time)

def user_time(message):
    bot_db.info.append(message.text)
    add_data_db(bot_db.info)
    bot.send_message(message.from_user.id, 'Расписание установлено\u2705')
    bot_db.info = []

@bot.callback_query_handler(lambda c: c.data == 'get')
def get_schedule(callback_query):
    bot.answer_callback_query(callback_query.id)
    string = get_user_schedule(callback_query.from_user.id)
    bot.send_message(callback_query.from_user.id, f'Ваши расписания:\n{string}', reply_markup=keyboard_schedule_delete)

@bot.callback_query_handler(lambda c: c.data == 'delete_one')
def delete_one(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введите номер расписания')
    bot.register_next_step_handler(msg, delete_record)

def delete_record(message):
    delete_one_schedule(message.text)
    bot.send_message(message.from_user.id, 'Запись удалена\u2705')


@bot.callback_query_handler(lambda c: c.data == 'delete_all')
def delete_all(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Записи удалены\u2705')
    delete_all_shedule(callback_query.from_user.id)

#@bot.message_handler(content_types=['text'])
#def send_text(message):
    #query = get_weather(message.text)
    #bot.send_message(message.chat.id, query)






if __name__ == '__main__':
    app.run()

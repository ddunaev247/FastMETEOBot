import flask
from flask import Flask, request, Response
import requests
from config import TOKEN
import message_bot
import telebot
from function_weather import get_weather
from keyboards import keyboard_menu, keyboard_repeat, keyboard_schedule, keyboard_schedule_delete
from telebot.types import ReplyKeyboardRemove
from bot_db import *
import bot_db
import logging
from auto_posting import process_autoposting

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
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


@bot.message_handler(commands=['Погода'])
def command_weather(message):
    msg = bot.send_message(message.chat.id, 'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return )


def command_weather_return(message):
    result = get_weather(message.text)
    bot.send_message(message.chat.id, result, reply_markup=keyboard_repeat)


@bot.callback_query_handler(lambda c: c.data == 'new_query')
def callback_weather(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return)


@bot.message_handler(commands=['Расписание'])
def command_schedule(message):
    bot.send_message(message.chat.id, message_bot.schedule, reply_markup=keyboard_schedule)


@bot.callback_query_handler(lambda c: c.data == 'set')
def set_schedule(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, '1-ое: Введи название города')
    bot.register_next_step_handler(msg, user_city)


def user_city(message):
    msg = bot.send_message(message.chat.id, '2-ое: Введи время в формате ЧЧ:ММ')
    if not bot_db.info.get(message.from_user.id) == None:
        del bot_db.info[message.from_user.id]
    bot_db.info.setdefault(message.from_user.id,[]).append(message.from_user.id)
    bot_db.info.setdefault(message.from_user.id,[]).append(message.text)
    bot.register_next_step_handler(msg, user_time)


def user_time(message):
    time = message.text
    time = time.split(':')
    if (time[0].isdigit() and -1 < int(time[0]) < 24) and (time[1].isdigit() and -1 < int(time[0]) < 59):
        bot_db.info.setdefault(message.from_user.id,[]).append(time[0])
        bot_db.info.setdefault(message.from_user.id,[]).append(time[1])
        add_data_db(bot_db.info, message.from_user.id)
        bot.send_message(message.from_user.id, 'Расписание установлено\u2705')
    else:
        msg = bot.send_message(message.from_user.id,message_bot.bad_input_time)
        bot.register_next_step_handler(msg, user_time)


@bot.callback_query_handler(lambda c: c.data == 'get')
def get_schedule(callback_query):
    bot.answer_callback_query(callback_query.id)
    string = get_user_schedule(callback_query.from_user.id)
    if not string:
        bot.send_message(callback_query.from_user.id, f'У Вас нет рассписаний')
    else:
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, f'Ваши расписания:\n{string}', reply_markup=keyboard_schedule_delete)


@bot.callback_query_handler(lambda c: c.data == 'delete_one')
def delete_one(callback_query):
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введите номер расписания')
    bot.register_next_step_handler(msg, delete_record)


def delete_record(message):
    list_id = all_id_record()
    if message.text == '/Погода':
        msg = bot.send_message(message.from_user.id, 'Введи название города')
        bot.register_next_step_handler(msg,command_weather_return)
    elif message.text == '/Расписание':
        bot.send_message(message.chat.id, message_bot.schedule, reply_markup=keyboard_schedule)
    elif message.text.isdigit() == False or not int(message.text) in list_id:
        msg = bot.send_message(message.from_user.id, message_bot.bad_input_id_schedule)
        bot.register_next_step_handler(msg, delete_record)
    else:
        delete_one_schedule(message.text)
        bot.send_message(message.from_user.id, 'Запись удалена\u2705')


@bot.callback_query_handler(lambda c: c.data == 'delete_all')
def delete_all(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Все записи удалены\u2705')
    delete_all_shedule(callback_query.from_user.id)



#@bot.message_handler(content_types=['text'])
#def return_cmd_weather(message):
#   if message.text == '/Погода':
#        msg = bot.send_message(message.chat.id, 'переключаю на погоду')
#        bot.register_next_step_handler(msg, command_weather)



if __name__ == '__main__':
    process_autoposting.start()
    app.run()


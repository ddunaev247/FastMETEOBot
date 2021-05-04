# the main bot module, it contains the main handlers and functions

from app import app
import flask
from flask import request, Response
from const import message_bot
from const.config import TOKEN
import telebot
import logging
import time
from multiprocessing import Process
from func.func_weather import get_weather
from keyboards.keyboards import *
from bot_db.bot_db import *
from func.func_time import *
from typing import Union
from statistics.static import create_statistic


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(TOKEN)


@app.route('/', methods=['POST', 'GET'])
def run_bot() -> Union[dict, str]:
    'view to receive and send responses from telegram servers'
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


def check_send_messages() ->None:
    '''this function checks the database for the presence of schedules equal to the current time,
     if available, it sends weather messages to the users who set the schedules'''
    while True:
        hour, min = check_hour(), check_minutes()
        list_schedule = check_schedule(hour, min)
        for item in list_schedule:
            result = get_weather(item.city)
            try:
                bot.send_message(item.user_id, result)
            except:
                delete_all_shedule(item.user_id)
        time.sleep(60)


process_autoposting = Process(target=check_send_messages, args=())    # creating a separate process for auto-posting
process_create_statistic = Process(target=create_statistic, args=())   # a separate process for creating statistics once an hour


@bot.message_handler(commands=['start'])
def start_message(message: types.Message) -> None:
    'start command handler'
    bot.send_message(message.chat.id, message_bot.start, reply_markup=keyboard_menu)


@bot.message_handler(commands=['Погода'])
def command_weather(message: types.Message) -> None:
    'weather command handler'
    msg = bot.send_message(message.chat.id, 'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return )


def command_weather_return(message: types.Message) -> None:
    'function of sending a message by a bot, with the results of a request for weather in the city'
    if message.text != '/Погода' and message.text != '/Расписание':
        result = get_weather(message.text)
        bot.send_message(message.from_user.id, result, reply_markup=keyboard_repeat)
        if not info_query.get(message.from_user.id) == None:
            del info_query[message.from_user.id]
        info_query.setdefault(message.from_user.id, []).extend([message.from_user.id,message.text, result.replace(r"\n","\t"),
                                                                check_year(), check_month(), check_day(), check_hour(),
                                                                check_minutes(),check_second()])
        add_data_queries(info_query, message.from_user.id)

    elif message.text == '/Погода':
        msg = bot.send_message(message.from_user.id, 'Введи название города')
        bot.register_next_step_handler(msg,command_weather_return)
    elif message.text == '/Расписание':
        bot.send_message(message.chat.id, message_bot.schedule, reply_markup=keyboard_schedule)


@bot.callback_query_handler(lambda c: c.data == 'new_query')
def callback_weather(callback_query: types.CallbackQuery) -> None:
    'new weather request handler'
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введи название города')
    bot.register_next_step_handler(msg, command_weather_return)


@bot.message_handler(commands=['Расписание'])
def command_schedule(message: types.Message) -> None:
    'schedules command handler'
    bot.send_message(message.chat.id, message_bot.schedule, reply_markup=keyboard_schedule)


@bot.callback_query_handler(lambda c: c.data == 'set')
def set_schedule(callback_query: types.CallbackQuery) -> None:
    'handler and scheduling function'
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, '1-ое: Введи название города')
    bot.register_next_step_handler(msg, user_city)


def user_city(message: types.Message) -> None:
    'function of requesting the city from the user, for the schedules'
    result = get_weather(message.text)
    if result == 'Город не найден':
        msg = bot.send_message(message.from_user.id, message_bot.bad_input_city)
        bot.register_next_step_handler(msg, user_city)
    else:
        msg = bot.send_message(message.chat.id, '2-ое: Введи время в формате ЧЧ:ММ')
        if not info.get(message.from_user.id) == None:
            del info[message.from_user.id]
        info.setdefault(message.from_user.id,[]).append(message.from_user.id)
        info.setdefault(message.from_user.id,[]).append(message.text)
        bot.register_next_step_handler(msg, user_time)


def user_time(message: types.Message) -> None:
    'function of requesting time from the user, for the schedules'
    time = message.text
    time = time.split(':')
    if (time[0].isdigit() and -1 < int(time[0]) < 24) and (time[1].isdigit() and -1 < int(time[0]) < 59):
        info.setdefault(message.from_user.id,[]).append(time[0])
        info.setdefault(message.from_user.id,[]).append(time[1])
        add_data_schedule(info, message.from_user.id)
        bot.send_message(message.from_user.id, 'Расписание установлено\u2705')
    else:
        msg = bot.send_message(message.from_user.id,message_bot.bad_input_time)
        bot.register_next_step_handler(msg, user_time)


@bot.callback_query_handler(lambda c: c.data == 'get')
def get_schedule(callback_query: types.CallbackQuery) -> None:
    'handler and function for displaying user schedules'
    bot.answer_callback_query(callback_query.id)
    string = get_user_schedule(callback_query.from_user.id)
    if not string:
        bot.send_message(callback_query.from_user.id, f'У Вас нет рассписаний')
    else:
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, f'Ваши расписания:\n{string}', reply_markup=keyboard_schedule_delete)


@bot.callback_query_handler(lambda c: c.data == 'delete_one')
def delete_one(callback_query: types.CallbackQuery) -> None:
    'handler for deleting one schedules entry'
    bot.answer_callback_query(callback_query.id)
    msg = bot.send_message(callback_query.from_user.id, 'Введите номер расписания')
    bot.register_next_step_handler(msg, delete_record)


def delete_record(message: types.Message) -> None:
    'the function of deleting the schedules by its number, with checks of the entered data from the user'
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
def delete_all(callback_query: types.CallbackQuery) -> None:
    'handler and function for deleting all user schedules'
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Все записи удалены\u2705')
    delete_all_shedule(callback_query.from_user.id)


if __name__ == '__main__':
    process_autoposting.start()
    process_create_statistic.start()
    app.run(debug=False)
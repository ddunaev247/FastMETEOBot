# this module contains the functions necessary to send weather to the user on a schedule

from datetime import datetime
import time
from multiprocessing import Process
from bot_db.bot_db import check_schedule
from func.function_weather import get_weather
import telebot
from const.config import TOKEN


bot = telebot.TeleBot(TOKEN)


def check_now_time() -> (int, int):
    'this function takes the current time and returns: the number of hours and minutes'
    return datetime.now().time().hour, datetime.now().time().minute


def check_send_messages() ->None:
    '''this function checks the database for the presence of schedules equal to the current time,
     if available, it sends weather messages to the users who set the schedule'''
    while True:
        hour, min = check_now_time()
        list_schedule = check_schedule(hour, min)
        for item in list_schedule:
            result = get_weather(item.city)
            bot.send_message(item.user_id, result)
        time.sleep(60)

process_autoposting = Process(target=check_send_messages, args=())
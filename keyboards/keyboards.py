# in the module, finding sets of keyboards that are used in the bot

from telebot import types

keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_weather_in_city = types.KeyboardButton('/Погода')
button_schedule = types.KeyboardButton('/Расписание')
keyboard_menu.add(button_weather_in_city)
keyboard_menu.add(button_schedule)

keyboard_repeat = types.InlineKeyboardMarkup()
button_repeat = types.InlineKeyboardButton(text='Новый запрос', callback_data='new_query')
keyboard_repeat.add(button_repeat)

keyboard_schedule = types.InlineKeyboardMarkup()
button_set_schedule = types.InlineKeyboardButton(text='Установить расписание\u23f0', callback_data='set')
button_get_my_schedule = types.InlineKeyboardButton(text='Мои расписания\ud83d\uddd3', callback_data='get')
keyboard_schedule.add(button_set_schedule)
keyboard_schedule.add(button_get_my_schedule)

keyboard_schedule_delete = types.InlineKeyboardMarkup()
button_schedule_delete_one = types.InlineKeyboardButton(text='Удалить одно 1\ufe0f\u20e3', callback_data='delete_one')
button_schedule_delete_all = types.InlineKeyboardButton(text='Удалить все \ud83d\udd22', callback_data='delete_all')
keyboard_schedule_delete.add(button_schedule_delete_one)
keyboard_schedule_delete.add(button_schedule_delete_all)
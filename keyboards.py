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
button_set_schedule = types.InlineKeyboardButton(text='Установить расписание', callback_data='set')
button_get_my_schedule = types.InlineKeyboardButton(text='Мои расписания', callback_data='get')
keyboard_schedule.add(button_set_schedule)
keyboard_schedule.add(button_get_my_schedule)

keyboard_schedule_delete = types.InlineKeyboardMarkup()
button_schedule_delete_one = types.InlineKeyboardButton(text='Удалить одно', callback_data='delete_one')
button_schedule_delete_all = types.InlineKeyboardButton(text='Удалить все', callback_data='delete_all')
keyboard_schedule_delete.add(button_schedule_delete_one)
keyboard_schedule_delete.add(button_schedule_delete_all)
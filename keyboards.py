from telebot import types

keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_weather_in_city = types.KeyboardButton('/Погода')
button_shedule = types.KeyboardButton('/Расписание')
keyboard_menu.add(button_weather_in_city)
keyboard_menu.add(button_shedule)

keyboard_inline = types.InlineKeyboardMarkup()
button_replay = types.InlineKeyboardButton(text='Заново \ud83d\udd04', callback_data='/Погода')
keyboard_inline.add(button_replay)

keyboard_shedule = types.InlineKeyboardMarkup()
button_set_shedule = types.InlineKeyboardButton(text='Установить расписание \u23f0', callback_data='set')
button_get_my_shedule = types.InlineKeyboardButton(text='Мои расписания \ud83d\uddd3', callback_data='get')
keyboard_shedule.add(button_set_shedule)
keyboard_shedule.add(button_get_my_shedule)

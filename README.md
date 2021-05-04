<p class="has-line-data" data-line-start="0" data-line-end="17">FastMETEOBot<br>
 <div>Телеграм бот погоды. Быстрое получение погоды по запросу, поддержка результатов погоды по расписанию</div>
 <div> </div>
Структура репозитория<br>
├── bot_db<br>
│ └── bot_db.py # функции работы с БД<br>
├── const<br>
│ ├── config.py # константы API<br>
│ └── message_bot.py # сообщения отправляемые ботом<br>
├── func<br>
│ ├── func_time.py # временные функции<br>
│ └── function_weather.py # функции получения погоды, формирования сообщения с погодой<br>
├── keyboards<br>
│ └── keyboards.py # клавиатуры которые используются в боте<br>
├── bot.py # основной файл бота<br>
├── app.py # файл админ панели, веб-приложения<br>
├── manager.py # менеджер для работы с бд<br>
├── testing.py # файл тестов<br>
└── README.md</p>
<p class="has-line-data" data-line-start="18" data-line-end="23">Задача<br>
Требовалось создать телеграм бота:<br>
1.Cпособного отправлять пользователю погоду по запросу названия города.<br>
2.Поддерживающего функцию отправки погоды по расписанию, которое задает пользователь<br>
3.Поддерживающего функции добавления/просмотра/удаления расписания</p>
<p class="has-line-data" data-line-start="24" data-line-end="29">Дополнительно:<br>
1.Реализовать веб-интерфейс администратора<br>
2.Поддержку управления расписаниями из админ панели<br>
3.Поддержку управления запросами из админ панели<br>
4.Просмотр статистики</p>

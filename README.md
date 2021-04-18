<h1 class="code-line" data-line-start=1 data-line-end=2 ><a id="FastMETEOBot_1"></a>FastMETEOBot</h1>
<h1 class="code-line" data-line-start=3 data-line-end=4 ><a id="__3"></a>Структура репозитория</h1>
<p class="has-line-data" data-line-start="5" data-line-end="17">├── bot_db<br>
│   └── bot_db.py                     # функции работы с БД<br>
├── const<br>
│   ├── <a href="http://config.py">config.py</a>                     # константы API<br>
│   └── message_bot.py                # сообщения отправляемые ботом<br>
├── func<br>
│   ├── auto_posting.py               # функции автопостинга погоды<br>
│   └── function_weather.py           # функции получения погоды, формирования сообщения с погодой<br>
├── keyboards<br>
│   └── <a href="http://keyboards.py">keyboards.py</a>                  # клавиатуры которые используются в боте<br>
├── <a href="http://bot.py">bot.py</a>                            # основной файл бота<br>
└── <a href="http://README.md">README.md</a></p>
<h1 class="code-line" data-line-start=20 data-line-end=21 ><a id="_20"></a>Задача</h1>
<p class="has-line-data" data-line-start="21" data-line-end="23">Требовалось создать телеграм бота:<br>
1.способного отправлять пользователю погоду по запросу названия города.</p>
<ol start="2">
<li class="has-line-data" data-line-start="23" data-line-end="24">Поддерживающего функцию отправки погоды по расписанию, которое задает пользователь</li>
<li class="has-line-data" data-line-start="24" data-line-end="25">Поддерживающего функции добавления/просмотра/удаления расписания</li>
</ol

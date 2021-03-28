import flask
from flask import Flask, request, Response
from config import TOKEN
import message_bot
import telebot


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

@bot.message_handler(commands=['start', 'help'])
def start_messege(message):
    bot.send_message(message.chat.id, message_bot.start)


#@bot.message_handler(content_types=['text'])
#def send_text(message):
#   if message.text.lower() == 'hi':
#       bot.send_message(message.chat.id, 'hi and you')



if __name__ == '__main__':
    app.run()

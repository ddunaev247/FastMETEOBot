import flask
from flask import Flask, request, Response,render_template
import telebot
from const.config import TOKEN,Configuration
from flask import Blueprint
bot = telebot.TeleBot(TOKEN)
schedules = Blueprint('schedules', __name__, template_folder='templates')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot_db/botDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

app.config.from_object(Configuration)
from bot_db.bot_db import Schedules









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

@app.route('/admin', methods=['POST', 'GET'])
def admin_panel():
    return render_template('admin_schedule.html')

@schedules.route('/')
def index():
    schedules = Schedules.query.all()
    return render_template('schedules/index.html', schedules=schedules)
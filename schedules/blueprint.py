from flask import Blueprint,render_template
from bot_db.bot_db import Schedules

schedules = Blueprint('schedules', __name__, template_folder='templates')

@schedules.route('/')
def index():
    schedules = Schedules.query.all()
    return render_template('schedules/index.html', schedules=schedules)
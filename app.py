from flask import Flask, render_template
from const.config import Configuration
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Configuration)
admin = Admin(app)
from bot_db.bot_db import Schedule,db

admin.add_view(ModelView(Schedule, db.session))

@app.route('/admin')
def admin_panel():
    return render_template('admin_page.html')


@app.route('/admin/schedules')
def admin_schedules():
    schedules = Schedule.query.all()
    return render_template('schedules.html', schedules=schedules)


@app.route('/admin/stat')
def admin_statistics():
    return render_template('stat.html')
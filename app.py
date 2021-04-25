from flask import Flask, render_template
from const.config import Configuration
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Configuration)
admin = Admin(app, base_template='admin/no-brand-layout.html', template_mode='bootstrap3')
from bot_db.bot_db import db,Schedule, Queries



class Statistics(BaseView):
    @expose('/')
    def statistics(self):
        return self.render('statnew.html')


admin.add_view(ModelView(Schedule, db.session))
admin.add_view(ModelView(Queries, db.session))
admin.add_view(Statistics(name='Statistics'))
@app.route('/admin')
def admin_panel():
    return render_template('admin/index.html')


@app.route('/admin/schedule')
def admin_schedules():
    return render_template('schedules.html')

@app.route('/admin/queries')
def admin_queries():
    return render_template('queries.html')

@app.route('/admin/statistics')
def admin_statistics():
    return render_template('statnew.html')





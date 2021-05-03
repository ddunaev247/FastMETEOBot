# application module and view for the admin page

from flask import Flask, render_template
from const.config import Configuration
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config.from_object(Configuration)
admin = Admin(app, base_template='admin/no-brand-layout.html', template_mode='bootstrap3')

from bot_db.bot_db import db, Schedule, Queries
from statistics.static import popular_hour_dgrm, popular_city_dgrm, statistics_queries

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Statistics(BaseView):
    'Class and view for the "Statistics" admin page'
    @expose('/', methods= ['GET'])
    def statistics(self):
        popular_city_dgrm()
        popular_hour_dgrm()
        statistics_queries()
        return self.render('statnew.html')


admin.add_view(ModelView(Schedule, db.session))
admin.add_view(ModelView(Queries, db.session))
admin.add_view(Statistics(name='Statistics'))


@app.route('/admin')
def admin_panel():
    'view for main admin page'
    return render_template('admin/index.html')


@app.route('/admin/schedule')
def admin_schedules():
    'view for the "Schedule" admin page'
    return render_template('schedules.html')


@app.route('/admin/queries')
def admin_queries():
    'view for the "Queries" admin page'
    return render_template('queries.html')






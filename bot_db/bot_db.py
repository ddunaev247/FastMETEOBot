from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)

info = {}


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    city = db.Column(db.String(140))
    time_hour = db.Column(db.Integer)
    time_minutes = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Schedule, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.id, self.user_id, self.city, self.time_hour, self.time_minutes


def add_data_db(data: dict, id:int) -> None:
    'function of adding data to the database'
    data_record = Schedule(user_id=data[id][0], city=data[id][1], time_hour=data[id][2], time_minutes=data[id][3])
    db.session.add(data_record)
    db.session.commit()


def get_user_schedule(user_id: int) -> str:
    'function for getting the schedules set by the user'
    list_schedule = db.session.query(Schedule).filter(Schedule.user_id==user_id).all()
    data_for_message = "\n\r".join([f"{item.id} - {item.city}, {item.time_hour}ч:{item.time_minutes}мин" for item in list_schedule])
    return data_for_message


def delete_one_schedule(record_id:int) -> None:
    'function of deleting one schedules from the database specified by the user'
    delete_record = db.session.query(Schedule).filter(Schedule.id==record_id).one()
    db.session.delete(delete_record)
    db.session.commit()


def delete_all_shedule(user_id:int) -> None:
    'function for deleting all user schedules from the database'
    delete_all_record = db.session.query(Schedule).filter(Schedule.user_id == user_id).all()
    for record in delete_all_record:
        db.session.delete(record)
    db.session.commit()


def check_schedule(hour: int, minutes: int) ->tuple:
    'function of checking the availability of schedules in the database, which correspond to the current time'
    data = db.session.query(Schedule).filter(Schedule.time_hour==hour).filter(Schedule.time_minutes==minutes).all()
    return data


def all_id_record() -> list:
    'the function returns all schedules numbers'
    list_record = db.session.query(Schedule).filter(Schedule.id).all()
    list_id = [item.id for item in list_record]
    return list_id
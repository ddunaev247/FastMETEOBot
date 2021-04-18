
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('sqlite:///botDBnew.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
info = {}

class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column('user_id',Integer, nullable=False)
    city = Column('city', String(250), nullable=False)
    time_hour = Column('time_hour', Integer, nullable=False)
    time_minutes = Column('time_minutes', Integer, nullable=False)
    def __repr__(self):
       return f'{self.id}, {self.user_id}, {self.city}, {self.time_hour}:{self.time_minutes}'


def add_data_db(data, id):
    data_record = Schedule(user_id=data[id][0], city=data[id][1], time_hour=data[id][2], time_minutes=data[id][3])
    session.add(data_record)
    session.commit()


def get_user_schedule(user_id):
    list_schedule = session.query(Schedule).filter(Schedule.user_id==user_id).all()
    data_for_message = "\n\r".join([f"{item.id} - {item.city}, {item.time_hour}ч:{item.time_minutes}мин" for item in list_schedule])
    return data_for_message

def delete_one_schedule(record_id):
    delete_record = session.query(Schedule).filter(Schedule.id==record_id).one()
    session.delete(delete_record)
    session.commit()

def delete_all_shedule(user_id):
    delete_all_record = session.query(Schedule).filter(Schedule.user_id == user_id).all()
    for record in delete_all_record:
        session.delete(record)
    session.commit()


def check_schedule(hour, minutes):
    data = session.query(Schedule).filter(Schedule.time_hour==hour).filter(Schedule.time_minutes==minutes).all()
    return data

def all_id_record():
    list_record = session.query(Schedule).filter(Schedule.id).all()
    list_id = [item.id for item in list_record]
    return list_id

list = all_id_record()
if not 50 in list:
    print('NOT OK')
else:
    print("OK")

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('sqlite:///botDB.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column('user_id',Integer, nullable=False)
    city = Column('city', String(250), nullable=False)
    time_hour = Column('time_hour', Integer, nullable=False)
    time_minutes = Column('time_minutes', Integer, nullable=False)
    def __repr__(self):
       return f'{self.id}, {self.user_id}, {self.city}, {self.time_hour}:{self.time_minutes}'


def add_data(data):
    data_record = Schedule(user_id=data[0], city=data[1], time_hour=data[2],time_minutes=data[3])
    session.add(data_record)
    session.commit()


def get_user_schedule(user_id):
    list_schedule = session.query(Schedule).filter(Schedule.user_id==user_id).all()
    my_string = "\n\r".join([f"{item.id} - {item.city}, {item.time_hour}:{item.minutes}" for item in list_schedule])
    print(list_schedule)
    print(my_string)

#get_user_schedule(440945969)
def delete_all_shedule(user_id):
    delete_all_record = session.query(Schedule).filter(Schedule.user_id==user_id).all()
    for record in delete_all_record:
        session.delete(record)
    session.commit()

def delete_one_schedule(record_id):
    delete_record = session.query(Schedule).filter(Schedule.id==record_id).one()
    session.delete(delete_record)
    session.commit()

#delete_all_shedule(440945969)
#delete_one_schedule(59)

def all_id_record():
    list_record = session.query(Schedule).filter(Schedule.id).all()
    list_id = [item.id for item in list_record]
    return list_id



from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('sqlite:///botDBnew.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column('user_id',Integer, nullable=False)
    city = Column('city', String(250), nullable=False)
    time_user = Column('time_user', String(250), nullable=False)
    def __repr__(self):
       return f'{self.id}, {self.user_id}, {self.city}, {self.time_user}'


def add_data(data):
    data_record = Schedule(user_id=data[0], city=data[1], time_user=data[2])
    session.add(data_record)
    session.commit()


def get_user_schedule(user_id):
    list_record = []
    list_shedule = []
    list_schedule =  session.query(Schedule).filter(Schedule.user_id==user_id).all()
    my_string = "\n\r".join([f"{item.id} - {item.city}, {item.time_user}" for item in list_schedule])
    print(list_schedule)
    print(my_string)

#get_user_schedule(440945969)
def delete_all_shedule(user_id):
    delete_all_record = session.query(Schedule).filter(Schedule.user_id==user_id).all()
    for record in delete_all_record:
        session.delete(record)
    session.commit()

delete_all_shedule(440945969)
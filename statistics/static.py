from matplotlib import pyplot as plt
import numpy as np
from app import db,Schedule,Queries
from func.func_time import check_year, check_month, check_day
from datetime import datetime,timedelta
import time

def popular_city_dgrm() -> None:
    list_city = []
    count_city = []
    country_counts = db.session.query(Schedule.city, db.func.count()).group_by(Schedule.city).all()
    for city, count in country_counts:
        list_city.append(city)
        count_city.append(count)

    positions = np.arange(len(count_city))  # положения столбцов по оси X
    width = 0.25                       # ширина столбцов
    figure = plt.figure()
    axes = figure.gca()
    axes.bar(positions, count_city, width, tick_label=list_city,
             align='center')
    axes.set_title('Пополурность городов в расписаниях')
    axes.set_xlabel('Города')                # заголовок оси X
    axes.set_ylabel('Количество в расписаниях')             # заголовок оси Y
    plt.savefig('static/pop_city.png')

def popular_hour_dgrm() -> None:
    list_hour = []
    count_hour = []
    hour_count = db.session.query(Schedule.time_hour, db.func.count()).group_by(Schedule.time_hour).all()
    for hour, count in hour_count:
        list_hour.append(hour)
        count_hour.append(count)

    positions = np.arange(len(count_hour))  # положения столбцов по оси X
    width = 0.25  # ширина столбцов
    figure = plt.figure()
    axes = figure.gca()
    axes.bar(positions, count_hour, width, tick_label=list_hour,
             align='center')
    axes.set_title('Пополурность часа в расписаниях')
    axes.set_xlabel('Час')  # заголовок оси X
    axes.set_ylabel('Количество в расписаниях')  # заголовок оси Y
    plt.savefig('static/pop_hour.png')

def statistics_queries() -> None:
    list_days = []
    list_count = []
    queries_count = db.session.query(Queries.year, Queries.month, Queries.day, db.func.count()).order_by(Queries.month).group_by(Queries.day).all()
    now = datetime(check_year(),check_month(),check_day())
    delta = now-timedelta(days=6)
    for year,month,day,count in queries_count:
        if datetime(year,month,day) >= delta:
            list_days.append(day)
            list_count.append(count)

    positions = np.arange(len(list_count))  # положения столбцов по оси X
    width = 0.25  # ширина столбцов
    figure = plt.figure()
    axes = figure.gca()
    axes.bar(positions, list_count, width, tick_label=list_days,
             align='center')
    axes.set_title('Количество запросов за последние 7 дней')
    axes.set_xlabel('День')  # заголовок оси X
    axes.set_ylabel('Количество запросов')  # заголовок оси Y
    plt.savefig('static/queries.png')

def create_statistics() -> None:
    while True:
        popular_city_dgrm()
        popular_hour_dgrm()
        statistics_queries()
        time.sleep(43200)
import sqlite3
from typing import Union
name_db = 'botDB.sqlite'
name_table = 'shedule'
info = []
def creat_query(query: str, data):
    conn = sqlite3.connect(name_db)
    cur = conn.cursor()
    if data:
        cur.execute(query, data)
    else:
        cur.execute(query)
    return conn, cur

def add_info_chat(info: tuple) -> None:
    conn, cur = creat_query(f"INSERT INTO {name_table}(chat_id) VALUES(?)", [info])
    conn.commit()

def add_info_city(info: tuple) -> None:
    conn, cur = creat_query(f"INSERT INTO {name_table}(city) VALUES(?)", [info])
    conn.commit()

def add_info_time(info: tuple) -> None:
    conn, cur = creat_query(f"INSERT INTO {name_table}(time_user) VALUES (?)", [info])
    conn.commit()

def add_info(info: tuple) -> None:
    conn, cur = creat_query(f"INSERT INTO {name_table}(chat_id, city, time_user) VALUES(?,?,?)", (info))
    conn.commit()




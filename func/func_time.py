from datetime import datetime

"the module contains functions for getting the current: year, month, day, hour, minute, second"

def check_year() -> int:
    return datetime.now().year

def check_month() -> int:
    return datetime.now().month

def check_day() -> int:
    return datetime.now().day

def check_hour() -> int:
    return datetime.now().time().hour

def check_minutes() -> int:
    return datetime.now().time().minute

def check_second() -> int:
    return datetime.now().time().second
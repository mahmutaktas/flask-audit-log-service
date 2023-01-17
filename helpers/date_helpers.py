from datetime import datetime


def get_current_date():
    current_date = datetime.now()
    current_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    current_date = datetime.strptime(
        current_date, "%Y-%m-%d %H:%M:%S")
    return current_date


def get_current_datetime_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

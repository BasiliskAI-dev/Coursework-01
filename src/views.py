import datetime

from main import path_to_data
import pandas as pd

def greetings(time: str):
    """В зависимотси от времени функция выдает приветсвие"""
    date_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    if 6 <= date_obj.hour < 12:
        word_of_greetings="Доброе утро"
    elif 12 <= date_obj.hour < 18:
        word_of_greetings="Добрый день"
    elif date_obj.hour >= 18:
        word_of_greetings="Добрый вечер"
    else:
        word_of_greetings="Доброй ночи"
    return word_of_greetings


def excel_reader(path: str) -> list:
    """Функция читает эксель как словарь"""
    reader = pd.read_excel(path)
    reader_to_dict = reader.to_dict("records")
    return reader_to_dict   


def filter_by_date(time)->list:
    """Создает список со словарями, с датами от начала месяца до текущей даты с помощью реплейс"""
    excel=excel_reader(path_to_data)
    date_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    list_of_need=[]
    for x in excel:
        if isinstance(x['Дата платежа'], str) and str(x['Дата платежа']).lower() != 'nan':
            if date_obj.replace(day=1)<=datetime.datetime.strptime(str(x['Дата платежа']), "%d.%m.%Y") <= date_obj:
                list_of_need.append(x)
    return list_of_need


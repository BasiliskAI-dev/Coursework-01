import datetime
import pandas as pd
import json
from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename:
                actual_filename = filename
            else:
                actual_filename = "report.txt"
            with open(actual_filename, "a", encoding="utf-8") as f:
                f.write(f"{result}\n")
            return result

        return wrapper

    return decorator


@log()
def spending_by_category(transactions: pd.DataFrame, category: str, date=None) -> str:
    """Функция для фильтрации входного датафрейма по категории и дате"""
    if date is None:
        date = datetime.datetime.now()
    elif isinstance(date, str):
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    new_time_obj = date + datetime.timedelta(days=-90)
    transactions["Дата платежа"] = pd.to_datetime(
        transactions["Дата платежа"], dayfirst=True
    )
    what_i_need = transactions.loc[
        (transactions["Категория"] == category)
        & (new_time_obj < transactions["Дата платежа"])
        & (transactions["Дата платежа"] <= date)
    ]
    what_i_need["Дата платежа"] = what_i_need["Дата платежа"].dt.strftime("%d.%m.%Y")

    # Теперь спокойно переводим в список словарей
    dict_result = what_i_need.to_dict(orient="records")

    # Теперь json.dumps сработает идеально
    resultes = json.dumps(dict_result, ensure_ascii=False, indent=4)
    return resultes

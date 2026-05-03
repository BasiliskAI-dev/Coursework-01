import datetime
from CONSTANCE import path_to_excel, path_to_user_settings
import pandas as pd
import json
import os
import requests
from dotenv import load_dotenv
import yfinance as yf


def greetings(time=None):
    """В зависимости от времени функция выдает приветствие"""
    if time:
        date_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    else:
        date_obj = datetime.datetime.now()
    if 6 <= date_obj.hour < 12:
        word_of_greetings = "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        word_of_greetings = "Добрый день"
    elif date_obj.hour >= 18:
        word_of_greetings = "Добрый вечер"
    else:
        word_of_greetings = "Доброй ночи"
    return word_of_greetings


def excel_reader(path: str) -> list:
    """Функция читает эксель как лист словарей"""
    reader = pd.read_excel(path)
    reader_to_dict = reader.to_dict("records")
    return reader_to_dict


def filter_by_date(time=None) -> list:
    """Создает список со словарями, с датами от начала месяца до текущей даты с помощью replace"""
    excel = excel_reader(path_to_excel)
    if time:
        date_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    else:
        date_obj = datetime.datetime.now()
    list_of_need = []
    for x in excel:
        if (
            isinstance(x["Дата платежа"], str)
            and str(x["Дата платежа"]).lower() != "nan"
        ):
            if (
                date_obj.replace(day=1)
                <= datetime.datetime.strptime(str(x["Дата платежа"]), "%d.%m.%Y")
                <= date_obj
            ):
                list_of_need.append(x)
    return list_of_need


def get_4_last_numbers_amount_cashback(list_of_need):
    """Функция отдает последние 4 цифры карты"""
    cards = []
    amount_dict = {}
    amount_cashback_dict = {}
    for x in list_of_need:
        card = x.get("Номер карты")
        # номер карты достал
        amount = x.get("Сумма платежа", 0)
        # сумму платежа достал
        cashback = amount / 100
        # создал переменные, чтобы сложить карта: кешбек, карта:общая сумма
        amount_dict[card] = amount_dict.get(card, 0) + amount
        amount_cashback_dict[card] = amount_cashback_dict.get(card, 0) + cashback
    for card, total in amount_dict.items():
        # проверяю нет ли пустых строк
        if isinstance(card, str):
            cashback = amount_cashback_dict.get(card, 0)
            item = {
                "last_digits": card,
                "total_spent": round(total, 2),
                "cashback": round(cashback, 2),
            }
            # складываю всё что у меня есть по одному ключу карте в один json ответ
            cards.append(item)
    return cards


def top_5_transactions(list_of_need):
    trans = sorted(list_of_need, key=lambda i: abs(i["Сумма платежа"]), reverse=True)
    top_transactions = []
    for x in trans[:5]:
        item = {
            "date": x.get("Дата платежа"),
            "amount": x.get("Сумма платежа"),
            "category": x.get("Категория"),
            "description": x.get("Описание"),
        }
        top_transactions.append(item)
    return top_transactions


def show_currency_and_stocks():
    """Функция перевода валюта с помощью АПИ"""
    load_dotenv()
    api_1 = os.getenv("API_KEY_1")
    with open(path_to_user_settings) as f:
        data = json.load(f)
        list_of_dates = data.get("user_currencies", 0)
        currency_rates = []
        for x in list_of_dates:
            headers = {"apikey": f"{api_1}"}
            to_param = "RUB"
            from_param = x
            summ = 1
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_param}&from={from_param}&amount={summ}"
            payload = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            result = (json.loads(response.text))["result"]
            item = {"currency": x, "rate": round(result, 2)}
            currency_rates.append(item)

    return currency_rates


def stocks_prices():
    with open(path_to_user_settings) as f:
        data = json.load(f)
        list_of_stacks = data.get("user_stocks", [])
        stock_prices = []
        for ticker in list_of_stacks:
            stock = yf.Ticker(ticker)
            # эти данные взяты из нейронки, была использована документация api с сайта
            # https://ranaroussi.github.io/yfinance/reference/api/yfinance.Tickers.html#yfinance.Tickers
            price = stock.history(period="1d")["Close"].iloc[-1]
            stock_prices.append({"stock": ticker, "price": float(round(price, 0))})
        return stock_prices

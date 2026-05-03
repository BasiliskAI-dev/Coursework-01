import json
from CONSTANCE import path_to_excel
from src.reports import spending_by_category
from src.services import search
from src.views import (greetings, filter_by_date, get_4_last_numbers_amount_cashback,
                       top_5_transactions, show_currency_and_stocks, stocks_prices)
import pandas as pd


def main_function_views():
    time = input("Введите необходимое число в противном случае будет использоваться текущее время: ")
    final_report = {}
    if not time:
        list_of_need = filter_by_date()
        final_report = {
            "greeting": greetings(),
            "cards": get_4_last_numbers_amount_cashback(list_of_need),
            "top_transactions": top_5_transactions(list_of_need),
            "currency_rates": show_currency_and_stocks(),
            "stock_prices": stocks_prices()
        }
    if time:
        list_of_need = filter_by_date(time)
        final_report = {
            "greeting": greetings(time),
            "cards": get_4_last_numbers_amount_cashback(list_of_need),
            "top_transactions": top_5_transactions(list_of_need),
            "currency_rates": show_currency_and_stocks(),
            "stock_prices": stocks_prices()
        }
    json_result = json.dumps(final_report, ensure_ascii=False)
    return json_result


def main_services(path):
    return search(path)


def main_reports(path):
    reader = pd.read_excel(path)
    category = input("Введите категория для поиска: ")
    date = input("Введите дату для поиска, если не введете будет использована текущая: ")
    return spending_by_category(reader, category, date)


if __name__ == "__main__":
    main_function_views()
    main_services(path_to_excel)
    main_reports(path_to_excel)

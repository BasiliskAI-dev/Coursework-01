import pytest
from unittest.mock import patch
from src.views import (greetings, show_currency_and_stocks, stocks_prices, top_5_transactions,
                       get_4_last_numbers_amount_cashback)


@pytest.mark.parametrize(
    "time, result",
    [
        ("2000-03-09 12:42:39", "Добрый день"),
        ("2000-03-09 01:42:39", "Доброй ночи"),
        ("2000-03-09 07:42:39", "Доброе утро"),
        ("2000-03-09 16:42:39", "Добрый день")
    ],
)
def test_greetings(time, result):
    assert greetings(time) == result


@patch('src.views.requests.request')
def test_show_currency_and_stocks(mock_get):
    mock_get.return_value.text = '{"result": 75.0}'
    result = show_currency_and_stocks()
    assert result[0]['rate'] == 75.0
    assert result[0]['currency'] == 'USD'


@patch('src.views.yf.Ticker')
def test_stocks_prices(mock_ticker):
    mock_stock = mock_ticker.return_value
    import pandas as pd
    mock_stock.history.return_value = pd.DataFrame({'Close': [150.0]})
    result = stocks_prices()
    assert result[0]['price'] == 150.0


def test_get_4_last_numbers_amount_cashback():
    test_data = [
        {'Номер карты': '*1111', 'Сумма платежа': 1000},
        {'Номер карты': '*1111', 'Сумма платежа': 2000},
        {'Номер карты': '*2222', 'Сумма платежа': 500}
    ]

    result = get_4_last_numbers_amount_cashback(test_data)
    assert len(result) == 2
    card_1 = next(item for item in result if item["last_digits"] == "*1111")
    assert card_1["total_spent"] == 3000
    assert card_1["cashback"] == 30.0


def test_top_5_transactions():
    test_data = [
        {'Сумма платежа': 100, 'Описание': 'Мало'},
        {'Сумма платежа': -5000, 'Описание': 'Много минус'},
        {'Сумма платежа': 3000, 'Описание': 'Средне'},
        {'Сумма платежа': 10000, 'Описание': 'Босс'},
        {'Сумма платежа': -50, 'Описание': 'Копейки'},
        {'Сумма платежа': 7000, 'Описание': 'Почти босс'}
    ]

    result = top_5_transactions(test_data)
    assert len(result) == 5
    assert result[0]['amount'] == 10000
    amounts = [item['amount'] for item in result]
    assert -5000 in amounts

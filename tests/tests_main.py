import json
from unittest.mock import patch
from main import main_function_views


def test_main_function_views_success():
    """Тестируем полную сборку итогового отчета"""

    mock_list_of_need = [{'Сумма платежа': 100}]
    mock_cards = [{'last_digits': '*1111', 'total_spent': 100}]
    mock_top = [{'amount': 100}]
    mock_currencies = [{'currency': 'USD', 'rate': 75.0}]
    mock_stocks = [{'stock': 'AAPL', 'price': 150.0}]
    with patch('main.input', return_value=''), \
            patch('main.filter_by_date', return_value=mock_list_of_need), \
            patch('main.greetings', return_value='Добрый день'), \
            patch('main.get_4_last_numbers_amount_cashback', return_value=mock_cards), \
            patch('main.top_5_transactions', return_value=mock_top), \
            patch('main.show_currency_and_stocks', return_value=mock_currencies), \
            patch('main.stocks_prices', return_value=mock_stocks):
        result_json = main_function_views()
        result_dict = json.loads(result_json)
        assert result_dict["greeting"] == "Добрый день"
        assert result_dict["cards"][0]["last_digits"] == "*1111"
        assert result_dict["currency_rates"][0]["currency"] == "USD"
        assert "stock_prices" in result_dict

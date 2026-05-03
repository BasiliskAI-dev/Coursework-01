import pandas as pd
import json
from unittest.mock import patch
from src.services import search


def test_search_success():
    mock_df = pd.DataFrame({
        'Категория': ['Супермаркеты', 'Транспорт'],
        'Описание': ['Ozon.ru', 'Метро']
    })
    with patch('builtins.input', return_value='Ozon'):
        with patch('pandas.read_excel', return_value=mock_df):
            # Вызываем функцию
            result_json = search('fake_path.xlsx')
            result_list = json.loads(result_json)
            assert len(result_list) == 1
            assert result_list[0]['Описание'] == 'Ozon.ru'
            assert result_list[0]['Категория'] == 'Супермаркеты'


def test_search_not_found():
    mock_df = pd.DataFrame({
        'Категория': ['Еда'],
        'Описание': ['Пятерочка']
    })
    with patch('builtins.input', return_value='Авиабилеты'):
        with patch('pandas.read_excel', return_value=mock_df):
            result_json = search('fake_path.xlsx')
            result_list = json.loads(result_json)
            assert len(result_list) == 0
            assert result_json == "[]"

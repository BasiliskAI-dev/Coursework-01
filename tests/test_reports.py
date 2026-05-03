import os
import pandas as pd
from src.reports import spending_by_category


def test_spending_by_category_logic():
    df = pd.DataFrame({
        'Дата платежа': ['01.01.2020', '01.02.2020'],
        'Категория': ['Еда', 'Транспорт'],
        'Сумма операции': [-100, -200]
    })
    result = spending_by_category(df, 'Еда', date='05.02.2020')
    assert 'Еда' in result
    assert '-100' in result
    result_empty = spending_by_category(df, 'Космос', date='05.02.2020')
    assert result_empty == "[]"


def test_log_decorator_creates_file():
    test_filename = "test_log.txt"
    if os.path.exists(test_filename):
        os.remove(test_filename)
    df = pd.DataFrame({'Дата платежа': ['01.01.2020'], 'Категория': ['Еда'], 'Сумма операции': [-100]})
    spending_by_category(df, 'Еда', '02.01.2020')
    assert os.path.exists("report.txt") or os.path.exists(test_filename)
    if os.path.exists(test_filename):
        os.remove(test_filename)

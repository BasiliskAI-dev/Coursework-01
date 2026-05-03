import re
import pandas as pd
import json


def search(path: str):
    """функция реализует поисковой запрос"""
    user_input = input("Поисковой запрос. Введите: ")
    safe_pattern = re.escape(user_input)
    df = pd.read_excel(path)
    category = df["Категория"].str.contains(safe_pattern, case=False, na=False)
    description = df["Описание"].str.contains(safe_pattern, case=False, na=False)
    result = df[category | description]
    json_result = json.dumps(result.to_dict(orient="records"), ensure_ascii=False)
    return json_result

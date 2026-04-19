import pytest
from src.views import greetings
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


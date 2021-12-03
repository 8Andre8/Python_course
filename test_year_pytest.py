import pytest
from unittest.mock import patch
import io
import urllib.request

from what_is_year_now import what_is_year_now  # импорт тестируемой функции


def test_YMD_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объекта.
    Дату подаем в формате YMD - YYYY-MM-DD (2021-11-30)
    """
    date_for_test = io.StringIO('{"currentDateTime": "2021-11-30T10:33Z"}')
    with patch.object(urllib.request, 'urlopen', return_value=date_for_test):
        year = what_is_year_now()
    assert year == 2021


def test_DMY_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объекта.
    Дату подаем в формате DMY - DD.MM.YYYY (30.11.2021)
    """
    date_for_test = io.StringIO('{"currentDateTime": "30.11.2021T10:33Z"}')
    with patch.object(urllib.request, 'urlopen', return_value=date_for_test):
        year = what_is_year_now()
    assert year == 2021


def test_exception_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объекта.
    Дату подаем в неправильном формате (перехватываем исключение)
    """
    date_for_test = io.StringIO('"currentDateTime": "НЕПРАВИЛЬНЫЙ ТИП"')
    with patch.object(urllib.request, 'urlopen', return_value=date_for_test):
        with pytest.raises(ValueError):
            what_is_year_now()

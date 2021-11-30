import pytest
from what_is_year_now import what_is_year_now
from unittest.mock import patch
import json


def test_YMD_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объектов.
    Дату подаем в формате YMD - YYYY-MM-DD (2021-11-30)
    """
    res = {"$id": "1",
           "currentDateTime": "2021-11-30T10:33Z",
           "utcOffset": "00:00:00",
           "isDayLightSavingsTime": "false",
           "dayOfTheWeek": "Tuesday",
           "timeZoneName": "UTC",
           "currentFileTime": 132827420017924361,
           "ordinalDate": "2021-334",
           "serviceResponse": "null"}

    with patch('urllib.request.urlopen') as mock:
        mock.return_value.ok = True
        with patch.object(json, 'load', return_value=res):
            year = what_is_year_now()

    assert year == 2021


def test_DMY_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объектов.
    Дату подаем в формате DMY - DD.MM.YYYY (30.11.2021)
    """
    res = {"$id": "1",
           "currentDateTime": "30.11.2021T10:33Z",
           "utcOffset": "00:00:00",
           "isDayLightSavingsTime": "false",
           "dayOfTheWeek": "Tuesday",
           "timeZoneName": "UTC",
           "currentFileTime": 132827420017924361,
           "ordinalDate": "2021-334",
           "serviceResponse": "null"}

    with patch('urllib.request.urlopen') as mock:
        mock.return_value.ok = True
        with patch.object(json, 'load', return_value=res):
            year = what_is_year_now()

    assert year == 2021


def test_exception_with_mock():
    """
    Проверяем работу функции what_is_year_now
    с заменой обращения в сеть с помощью mock-объектов.
    Дату подаем в неправильном формате (перехватываем исключение)
    """
    res = {"$id": "1",
           "currentDateTime": "НЕПРАВИЛЬНЫЙ ТИП",
           "utcOffset": "00:00:00",
           "isDayLightSavingsTime": "false",
           "dayOfTheWeek": "Tuesday",
           "timeZoneName": "UTC",
           "currentFileTime": 132827420017924361,
           "ordinalDate": "2021-334",
           "serviceResponse": "null"}

    with patch('urllib.request.urlopen') as mock:
        mock.return_value.ok = True
        with patch.object(json, 'load', return_value=res):
            with pytest.raises(ValueError):
                what_is_year_now()

import pytest
from one_hot_encoder import fit_transform


def test_standard():
    """
    Тест с примером без повторяющихся слов
    """
    assert fit_transform(['red', 'green', 'blue']) == [
        ('red', [0, 0, 1]),
        ('green', [0, 1, 0]),
        ('blue', [1, 0, 0])
    ]


def test_from_example():
    """
    Тест с примером с повторябщимися словами (из one_hot_encoder.py)
    """
    assert fit_transform(['Moscow', 'New York', 'Moscow', 'London']) == [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]


def test_eq():
    """
    Тест с повторяющимися словами
    """
    assert fit_transform(['red', 'blue', 'red']) == [
        ('red', [0, 1]),
        ('blue', [1, 0]),
        ('red', [0, 1])
    ]


def test_not_eq():
    """
    Тест с повторяющимися словами,
    проверяющий конкретное неправильное поведение (assertNotEqual)
    """
    assert fit_transform(['red', 'blue', 'red']) != [
        ('red', [0, 0, 1]),
        ('blue', [0, 1, 0]),
        ('red', [1, 0, 0])
    ]


def test_empty_input():
    """
    Тест с 0 числом аргументов (перехват исключения - assertRaises)
    """
    with pytest.raises(TypeError):
        fit_transform()


def test_not_iterable():
    """
    Тест с вводом неитерабельного типа (перехват исключения - assertRaises)
    """
    with pytest.raises(TypeError):
        fit_transform(42)

import unittest
from one_hot_encoder import fit_transform


class TestOneHot(unittest.TestCase):
    """
    Класс с тестами для проверки корректности работы функции fit_transform,
    реализующую one hot кодирование
    """
    def test_standard(self):
        """
        Тест с примером без повторяющихся слов
        """
        actual = fit_transform(['red', 'green', 'blue'])
        expected = [
            ('red', [0, 0, 1]),
            ('green', [0, 1, 0]),
            ('blue', [1, 0, 0])
        ]
        self.assertEqual(actual, expected)

    def test_from_example(self):
        """
        Тест с примером с повторябщимися словами (из one_hot_encoder.py)
        """
        actual = fit_transform(['Moscow', 'New York', 'Moscow', 'London'])
        expected = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        self.assertEqual(actual, expected)

    def test_eq(self):
        """
        Тест с повторяющимися словами
        """
        actual = fit_transform(['red', 'blue', 'red'])
        expected = [
            ('red', [0, 1]),
            ('blue', [1, 0]),
            ('red', [0, 1])
        ]
        self.assertEqual(actual, expected)

    def test_not_eq(self):
        """
        Тест с повторяющимися словами,
        проверяющий конкретное неправильное поведение (assertNotEqual)
        """
        actual = fit_transform(['red', 'blue', 'red'])
        not_expected = [
            ('red', [0, 0, 1]),
            ('blue', [0, 1, 0]),
            ('red', [1, 0, 0])
        ]
        self.assertNotEqual(actual, not_expected)

    def test_empty_input(self):
        """
        Тест с 0 числом аргументов (перехват исключения - assertRaises)
        """
        with self.assertRaises(Exception):
            fit_transform()

    def test_not_iterable(self):
        """
        Тест с вводом неитерабельного типа (перехват исключения - assertRaises)
        """
        with self.assertRaises(TypeError):
            fit_transform(42)

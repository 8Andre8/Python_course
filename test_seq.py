from seq import Seq


def test_from_example():
    """
    Тест с примером из лекции.
    """
    s = Seq([1, 2, 3, 4, 5])
    res = s.filter(lambda n: n % 2 == 0). \
        map(lambda n: n + 10). \
        take(3)
    assert res == [12, 14]


def test_1filter_1map_and_take():
    """
    Тест с применением 1 filter, 1 map и take.
    """
    s = Seq(['1', '2', '3'])
    res = s.filter(lambda n: type(n) == str). \
        map(int). \
        take(3)
    assert res == [1, 2, 3]


def test_1map_1filter_and_take():
    """
    Тест с применением 1 map, 1 filter и take.
    """
    s = Seq(['1', '2', '3'])
    res = s.map(int). \
        filter(lambda n: type(n) == int). \
        take(3)
    assert res == [1, 2, 3]


def test_many_filter_and_take():
    """
    Тест с большим числом последовательных фильтров.
    """
    s = Seq(['1', '2', '3'])
    res = s.filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        filter(lambda n: type(n) == str). \
        take(3)
    assert res == ['1', '2', '3']


def test_many_map_and_take():
    """
    Тест с большим числом последовательных map.
    """
    s = Seq(['1', '2', '3'])
    res = s.map(int). \
        map(float). \
        map(int). \
        map(float). \
        map(float). \
        map(int). \
        map(int). \
        map(str). \
        take(3)
    assert res == ['1', '2', '3']


def test_empty_after_filter():
    """
    Тест с пустым после фильтрации результатом.
    """
    s = Seq(['1', '2', '3'])
    res = s.filter(lambda n: type(n) == float).take(3)
    assert res == []


def test_without_take():
    """
    Тест ленивости - без применения take выводится лишь название класса (Seq)
    """
    s = Seq(['1', '2', '3'])
    res = s.map(int)
    assert str(res) == s.__class__.__name__


def test_with_different_types():
    """
    Тест с различными типами внутри Seq.
    """
    s = Seq([1, 2.2, 3.3, 'four', 5.5])
    res = s.filter(lambda n: type(n) == float). \
        map(int). \
        filter(lambda n: type(n) == int). \
        take(5)
    assert res == [2, 3, 5]

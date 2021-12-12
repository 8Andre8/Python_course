from __future__ import annotations
from typing import Sequence, TypeVar, Callable, Union
from itertools import islice


T = TypeVar('T')


class Seq:
    """
    Принимает в метод __init__ любую последовательность Sequence[T],
    где T - некоторый тип (generic).
    Реализованы методы map, filter и take.
    """
    def __init__(self, seq: Union[Sequence[T], map, filter]):
        self.seq = seq

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def map(self, func_to_change_type: Callable) -> Seq:
        """
        Применяет некоторую функцию ко всем элементам Sequence,
        полученный map-объект помещает в новый экземпляр класса Seq.
        Данный метод - ленивый
        (без вызова метода take результатом будет лишь название класса (Seq))
            Параметр:
                func_to_change_type: функция, которая трансформирует nип Т
                (тип элементов Sequence) в любой тип.
                Но может принимать и другие функции.
            Выходное значение:
                Seq: новый экземпляр класса, содержащий map-объект.
        """
        return Seq(map(func_to_change_type, self.seq))

    def filter(self, func_for_filtering_by_type: Callable) -> Seq:
        """
        Осуществляет фильтрацию элементов Sequence
        Данный метод - ленивый
        (без вызова метода take результатом будет лишь название класса (Seq))
            Параметр:
                func_for_filtering_by_type: функция,
                которая входным параметром принимает тип T и возвращает bool.
                Но может принимать и другие функции.
            Выходное значение:
                Seq: новый экземпляр класса, содержащий filter-объект.
        """
        return Seq(filter(func_for_filtering_by_type, self.seq))

    def take(self, n: int):
        """
        Принимает число и возвращает список из того количества элементов,
        которое передали в take.
            Параметр:
                n: количество элементов в списке для вывода.
        """
        return list(islice(self.seq, 0, n))


if __name__ == '__main__':
    s = Seq([1, 2.2, 3.3, 'four', 5.5])
    res = s.filter(lambda n: type(n) == float).\
        map(int).\
        filter(lambda n: type(n) == int).\
        take(5)
    print(res)

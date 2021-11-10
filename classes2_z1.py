import random
from abc import abstractmethod


class AnimeMon:
    """
        Абстрактный класс для аниме-монстров, имеющий:
            1. Абстрактное свойство exp, хранящее опыт монстра.
            2. Абстрактный метод inc_exp, увеличивающий опыт монстра.
    """
    @property
    @abstractmethod
    def exp(self):
        pass

    @abstractmethod
    def inc_exp(self, step_size: int):
        pass


class Pokemon(AnimeMon):
    """
        Класс для покемонов, наследующийся от абстрактного класса AnimeMon:
            Атрибуты:
                1. name - имя покемона,
                2. pokitype - тип покемона,
                3. experience - опыт покемона.
            Методы:
                1. exp - возвращает опыт покемона как атрибут класса,
                2. inc_exp - увеличивает опыт покемона по некоторой формуле.
    """
    def __init__(self, name: str, poketype: str, experience=0):
        self.name = name
        self.poketype = poketype
        self.experience = experience

    @property
    def exp(self):
        return self.experience

    def inc_exp(self, step_size: int):
        self.experience += step_size


class Digimon(AnimeMon):
    """
        Класс для дигимонов, наследующийся от абстрактного класса AnimeMon:
            Атрибуты:
                1. name - имя дигимона,
                2. experience - опыт дигимона.
            Методы:
                1. exp - возвращает опыт дигимона как атрибут класса,
                2. inc_exp - увеличивает опыт дигимона по некоторой формуле.
    """
    def __init__(self, name: str, experience=0):
        self.name = name
        self.experience = experience

    @property
    def exp(self):
        return self.experience

    def inc_exp(self, value: int):
        self.experience += value * 8


def train(mon: AnimeMon):
    """
        Проводит однократную тренировку аниме-монстра
            Параметр:
                mon: экземпляр класса некоторого аниме-монстра.
    """
    step_size, level_size = 10, 100
    sparring_qty = (level_size - mon.exp % level_size) // step_size
    for i in range(sparring_qty):
        win = random.choice([True, False])
    if win:
        mon.inc_exp(step_size)


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    train(bulbasaur)
    print(f'Опыт покемона {bulbasaur.name}: {bulbasaur.exp}')
    agumon = Digimon(name='Agumon')
    train(agumon)
    print(f'Опыт покемона {agumon.name}: {agumon.exp}')
    print(bulbasaur.__dict__)
    print(agumon.__dict__)

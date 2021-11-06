import json


class BaseAdvert():
    """
    Базовый класс необходимый для изменения вывода Advert.__repr__
        Атрибут:
            repr_color_code: задает цвет с помощью кода (33 - желтый)
    """
    repr_color_code = 33

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


class ColorMixin:
    """
    Миĸсин для изменения цвета вывода Advert.__repr__
    """

    def __repr__(self):
        color = super().repr_color_code
        string_to_print = super().__repr__()
        return f'\033[1;{color};20m{string_to_print}\033[0m'


class Advert(ColorMixin, BaseAdvert):
    """
    Динамичесĸи создает атрибуты эĸземпляра ĸласса из атрибутов JSON-объеĸта.
    Содержит обязательные артибуты:
        1. title - заголовок объявления,
        2. price - стоимость товара или услуги в обявлении.
    В случае отсутствия поля price в JSON-объеĸте возвращает 0.
    Осуществляет проверку неотрицательности атрибута price.
    """

    def __init__(self, json_dict: dict):
        for key, item in json_dict.items():
            if isinstance(item, dict):
                self.__setattr__(key, Advert(item))
            else:
                if key == 'price' and item < 0:
                    raise ValueError('price must be >= 0')
                else:
                    self.__setattr__(key, item)
        if 'price' not in self.__dict__:
            self.__setattr__('price', 0)


if __name__ == '__main__':
    phone_str = """
        {
            "title": "iPhone X",
            "price": 100,
            "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
            }
        }
        """
    phone = json.loads(phone_str)
    a = Advert(phone)
    assert a.title == "iPhone X", a.title
    assert a.price == 100, a.price
    assert a.location.address == "город Самара, улица Мориса Тореза, 50", a.location.address
    assert a.location.metro_stations == ["Спортивная", "Гагаринская"], a.location.metro_stations
    print("Заголовок:", a.title)
    print("Стоимость:", a.price)
    print("Адрес:", a.location.address)
    print("Станции метро:", a.location.metro_stations)
    print("REPR:", a)
    print()
    corgi_str = """
        {
            "title": "Вельш-корги",
            "price": 1000,
            "class": "dogs",
            "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
            }
        }
        """
    corgi = json.loads(corgi_str)
    a2 = Advert(corgi)
    assert a2.title == "Вельш-корги", a2.title
    assert a2.price == 1000, a2.price
    assert a2.location.address == "" \
                                  "сельское поселение Ельдигинское, " \
                                  "поселок санатория Тишково, 25", a2.location.address
    print("Заголовок:", a2.title)
    print("Цена:", a2.price)
    print("Адрес:", a2.location.address)
    print("REPR:", a2)
    a2.title = 'Вельш-Пельш-корги'
    a2.price *= 10
    print("REPR после изменений:", a2)

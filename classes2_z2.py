import json


class BaseAdvert:
    """
    Базовый класс необходимый для изменения вывода Advert.__repr__
        Атрибут:
            title: заголовок объявления,
            price: стоимость товара или услуги в объявлении.
    """
    title = None
    price = 0

    def __repr__(self):
        if self.title is not None:
            return f'{self.title} | {self.price} ₽'
        else:
            return self.__class__


class ColorMixin:
    """
    Миĸсин для изменения цвета вывода Advert.__repr__
    Атрибут:
        repr_color_code: задает цвет с помощью кода (33 - желтый).
    Методы:
        change_color: задает цвет для вывода,
        __repr__: выводит Advert.__repr__ с измененным цветом
    """
    repr_color_code = 33

    def change_color(self, color):
        self.repr_color_code = color

    def __repr__(self):
        color = self.repr_color_code
        string_to_print = super().__repr__()
        return f'\033[1;{color};20m{string_to_print}\033[0m'


class Advert(ColorMixin, BaseAdvert):
    """
    Динамичесĸи создает атрибуты эĸземпляра ĸласса из атрибутов JSON-объеĸта.
    Содержит обязательные артибуты:
        1. title: заголовок объявления,
        2. price: стоимость товара или услуги в объявлении.
    В случае отсутствия поля price в JSON-объеĸте возвращает 0.
    Осуществляет проверку неотрицательности атрибута price.
    Методы __getattr__, __setattr__ предотвращают зацикливание при
    обращении к несуществующим атрибутам
    """

    def __getattr__(self, item):
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __init__(self, json_dict: dict):
        for key, item in json_dict.items():
            if isinstance(item, dict):
                self.__setattr__(key, Advert(item))
            else:
                if key == 'price' and item < 0:
                    raise ValueError('price must be >= 0')
                else:
                    self.__setattr__(key, item)
        if 'title' not in self.__dict__:
            self.__setattr__('title', None)
        if 'price' not in self.__dict__:
            self.__setattr__('price', 0)


if __name__ == '__main__':
    # пример 1
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
    # пример 2
    corgi_str = """
        {
            "title": "Вельш-корги",
            "price": 1000,
            "category": "собаки",
            "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
            }
        }
        """
    corgi = json.loads(corgi_str)
    a2 = Advert(corgi)
    assert a2.title == "Вельш-корги", a2.title
    assert a2.price == 1000, a2.price
    assert a2.category == "собаки", a2.category
    assert a2.location.address == "" \
                                  "сельское поселение Ельдигинское, " \
                                  "поселок санатория Тишково, 25", a2.location.address
    print("Заголовок:", a2.title)
    print("Цена:", a2.price)
    print("Категория:", a2.category)
    print("Адрес:", a2.location.address)
    print("REPR:", a2)
    a2.title = 'Вельш-Пельш-корги'
    a2.price *= 10
    print("REPR после изменений:", a2)
    print()
    # пример 3
    pipe_str = """
            {
                "title": "Труба",
                "category": "Железки",
                "location": {
                "address": { 
                    "country": "Россия",
                    "town": "Железноводск",
                    "street": "Железная",
                    "house": 26
                    }
                }
            }
            """
    pipe = json.loads(pipe_str)
    a3 = Advert(pipe)
    assert a3.title == "Труба", a3.title
    assert a3.price == 0, a3.price
    assert a3.category == "Железки", a3.category
    assert a3.location.address.country == "Россия", a3.location.address.country
    assert a3.location.address.town == "Железноводск", a3.location.address.town
    assert a3.location.address.street == "Железная", a3.location.address.street
    assert a3.location.address.house == 26, a3.location.address.house
    print("Заголовок:", a3.title)
    print("Цена:", a3.price)
    print("Категория:", a3.category)
    print("Страна:", a3.location.address.country)
    print("Город:", a3.location.address.town)
    print("Улица:", a3.location.address.street)
    print("Дом:", a3.location.address.house)
    #print("Обращение к адресу целиком:", a3.location.address)
    a3.change_color(32)
    print("REPR:", a3)

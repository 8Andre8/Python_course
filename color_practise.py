from abc import ABC, abstractmethod


class ComputerColor(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __mul__(self, c):
        pass

    @abstractmethod
    def __rmul__(self, c):
        pass


class RGBColor(ComputerColor):
    """
    Реализует взаимодествие цветов на базе модели RGB.
    """
    END = '\033[0'
    START = '\033[1;38;2'
    MOD = 'm'

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self) -> str:
        """
        Выводит цветную точку.
        """
        return f'{self.START};{self.red};{self.green};{self.blue}{self.MOD}●{self.END}{self.MOD}'

    def __eq__(self, other) -> bool:
        """
        Сравнивает объекты (self и other) по цвету.
        """
        return self.__str__() == other.__str__()

    def __add__(self, other):
        """
        Смешивает цвета объектов КПМ().
        Установлен потолок для любого цвета: 255.
        """
        return RGBColor(min(self.red + other.red, 255),
                        min(self.green + other.green, 255),
                        min(self.blue + other.blue, 255))

    def __hash__(self):
        """
        Реализует проверку на уникальность.
        """
        return hash((self.red, self.green, self.blue))

    def __repr__(self):
        """
        Выводит точку (●) соответствующего цвета.
        """
        return f'{self.START};{self.red};{self.green};{self.blue}{self.MOD}●{self.END}{self.MOD}'

    def _change_contrast(self, current_contrast: float, c: float):
        """
        Реализует уменьшение контраста для 1 составляющей цвета.
            Параметры:
                current_contrast: текущее значение цвета,
                c: коэффициент изменения контраста.
        """
        contrast_level = -256 * (1 - c)
        f = (259 * (contrast_level + 255)) / (255 * (259 - contrast_level))
        return int(f * (current_contrast - 128) + 128)

    def __mul__(self, c: float):
        """
        Реализует уменьшение контраста.
            Параметр:
                с: коэффициент изменения контраста (при вызове стоит справа).
        """
        return RGBColor(self._change_contrast(self.red, c),
                        self._change_contrast(self.green, c),
                        self._change_contrast(self.blue, c))

    def __rmul__(self, c: float):
        """
        Реализует уменьшение контраста.
            Параметр:
                с: коэффициент изменения контраста (при вызове стоит слева).
        """
        return self.__mul__(c)


class HSLColor(ComputerColor):
    """
    Реализует взаимодествие цветов на базе модели HSL
    (упрощенно - работаем всегда с черным цветом).
    """
    END = '\033[0'
    START = '\033[1;38;2'
    MOD = 'm'

    def __init__(self, red, green, blue):
        self.red = 0
        self.green = 0
        self.blue = 0

    def __repr__(self) -> str:
        """
        Выводит точку (●) черного цвета.
        """
        return f'{self.START};{self.red};{self.green};{self.blue}{self.MOD}●{self.END}{self.MOD}'

    def _change_contrast(self, current_contrast: float, c: float) -> int:
        """
        Реализует уменьшение контраста для 1 составляющей цвета.
            Параметры:
                current_contrast: текущее значение цвета,
                c: коэффициент изменения контраста.
        """
        contrast_level = -256 * (1 - c)
        f = (259 * (contrast_level + 255)) / (255 * (259 - contrast_level))
        return int(f * (current_contrast - 128) + 128)

    def __mul__(self, c: float):
        """
        Реализует уменьшение контраста.
            Параметр:
                с: коэффициент изменения контраста (при вызове стоит справа).
        """
        return RGBColor(self._change_contrast(self.red, c),
                        self._change_contrast(self.green, c),
                        self._change_contrast(self.blue, c))

    def __rmul__(self, c: float):
        """
        Реализует уменьшение контраста.
            Параметр:
                с: коэффициент изменения контраста (при вызове стоит слева).
        """
        return self.__mul__(c)


def print_a(color: ComputerColor):
    """
    Выводит букву А, состоящую из цветных ●.
    """
    bg_color = 0.1 * color
    a_matrix = [
        [bg_color] * 19,
        [bg_color] * 9 + [color] + [bg_color] * 9,
        [bg_color] * 8 + [color] * 3 + [bg_color] * 8,
        [bg_color] * 7 + [color] * 2 + [bg_color] +
        [color] * 2 + [bg_color] * 7,
        [bg_color] * 6 + [color] * 2 + [bg_color] * 3 +
        [color] * 2 + [bg_color] * 6,
        [bg_color] * 5 + [color] * 9 + [bg_color] * 5,
        [bg_color] * 4 + [color] * 2 + [bg_color] * 7 +
        [color] * 2 + [bg_color] * 4,
        [bg_color] * 3 + [color] * 2 + [bg_color] * 9 +
        [color] * 2 + [bg_color] * 3,
        [bg_color] * 19,
    ]
    for row in a_matrix:
        print(''.join(str(ptr) for ptr in row))


if __name__ == '__main__':
    # Задание 1 - Вывод цвета
    print('Задание 1 - Вывод цвета')
    print('Red point:', RGBColor(255, 0, 0))
    print('Green point:', RGBColor(0, 255, 0))
    print('Blue point:', RGBColor(0, 0, 255))
    print('Black point:', RGBColor(0, 0, 0))
    print()

    # Задание 2 - Сравнение цветов
    red = RGBColor(255, 0, 0)
    other_red = RGBColor(255, 0, 0)
    green = RGBColor(0, 255, 0)
    string = 'not Color object'
    digit = 42
    print('Задание 2 - Сравнение цветов')
    print('red == red? ->', red == other_red)
    print('red == green? ->', red == green)
    print('red == string? ->', red == string)
    print('red == digit? ->', red == digit)
    print()

    # Задание 3 - Смешивание цветов
    red = RGBColor(255, 0, 0)
    green = RGBColor(0, 255, 0)
    blue = RGBColor(0, 0, 255)
    print('Задание 3 - Смешивание цветов')
    print('red + green =', red + green)
    print('red + blue =', red + blue)
    print('green + blue =', green + blue)
    print('red + green + blue =', red + green + blue)
    print()

    # Задание 4 - Уникальные цвета
    orange1 = RGBColor(255, 165, 0)
    red = RGBColor(255, 0, 0)
    green = RGBColor(0, 255, 0)
    blue1 = RGBColor(0, 0, 255)
    blue2 = RGBColor(0, 0, 255)
    blue3 = RGBColor(0, 0, 255)
    orange2 = RGBColor(255, 165, 0)
    color_list = [orange1, red, blue1, blue2, green, orange2, blue3]
    print('Задание 4 - Уникальные цвета')
    print(f'Все цвета: {color_list}')
    print('Уникальные цвета:', set(color_list))
    print()

    # Задание 5 - уменьшение контраста
    red = RGBColor(255, 0, 0)
    print('Задание 5 - уменьшение контраста')
    print('red * 0.9:', red * 0.9)
    print('red * 0.6:', red * 0.6)
    print('0.3 * red:', 0.3 * red)
    print('0.1 * red:', 0.1 * red)
    print()

    # Задание 6 - Вывод буквы А
    print('Задание 6 - Вывод буквы А')
    print('A in RGB:')
    print_a(red)
    print()
    hsl = HSLColor(0, 0, 0)
    print('A in HSL:')
    print_a(hsl)

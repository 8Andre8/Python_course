import sys
import datetime
from typing import Callable

original_write = sys.stdout.write


def my_write(string_text: str) -> int:
    """
    Подменяет метод write у объекта sys.stdout на такую функцию,
    которая перед каждым вызовом оригинальной функции записи данных в stdout
    допечатывает к тексту текущую метку времени.
        Параметр:
            string_text: строка для вывода.
    """
    now = datetime.datetime.now()
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    if string_text != '\n':
        string_to_write = f'[{date}]: {string_text}'
        original_write(string_to_write)
        return len(string_to_write)
    else:
        original_write(string_text)
        return len(string_text)


def timed_output(print_func: Callable) -> Callable:
    """
    Декоратор, который перед каждым вызовом
    оригинальной функции записи данных в stdout
    допечатывает к тексту текущую метку времени.
    """

    def wrapper(*args, **kwargs):
        now = datetime.datetime.now()
        date = now.strftime('%d-%m-%Y %H:%M:%S')
        print(f'[{date}]: ', end='')
        print_func(*args, **kwargs)

    return wrapper


@timed_output
def print_greeting(name: str):
    """
    Вывод приветствия в stdout.
    """
    print(f'Hello, {name}!')


def redirect_output(filepath: str) -> Callable:
    """
    Декоратор, осуществляющий перенапрвление вывода из stdout в файл.
    Если он не пуст, то содержимое будет перезаписано.
        Параметр:
            filepath: путь к файлу.
    """

    def out_wrapper(function: Callable) -> Callable:
        def inner_wrapper(*args, **kwargs):
            orig_stdout = sys.stdout
            f = open(filepath, 'w')
            sys.stdout = f
            text = function(*args, **kwargs)
            f.close()
            sys.stdout = orig_stdout
            return text

        return inner_wrapper

    return out_wrapper


@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


if __name__ == '__main__':
    # Задание 1 - подмена write
    print('Задание 1 - подмена write')
    sys.stdout.write = my_write
    print('Сообщение с текущей меткой времени')
    print('Еще одно')
    sys.stdout.write = original_write
    print()

    # Задание 2 - подмена write c декоратором
    print('Задание 2 - подмена write с декоратором')
    print_greeting('World')
    print_greeting('Gustav')
    print()

    # Задание 3 - перенаправление вывода в файл
    print('Задание 3 - перенаправление вывода в файл function_output.txt')
    calculate()
    print('Содержимое файла:')
    with open('./function_output.txt') as f:
        print(f.read())

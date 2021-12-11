import sys
import datetime
from Decorators import my_write
from Decorators import print_greeting
from Decorators import calculate


def test_changed_write(capfd):
    """
    Тест для функции my_write.
    Проверяет вывод временной метки в stdout.
    """
    now = datetime.datetime.now()
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    sys.stdout.write = my_write
    print('Тест')
    out, err = capfd.readouterr()
    assert out == f'[{date}]: Тест'


def test_changed_write_with_decorator(capfd):
    """
    Тест для функции print_greeting.
    Проверяет вывод временной метки вместе с приветствием.
    """
    now = datetime.datetime.now()
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    print_greeting('World')
    out, err = capfd.readouterr()
    assert out == f'[{date}]: Hello, World!\n'


def test_calculate():
    """
    Тест для функции calculate.
    Проверяет содержимое файла с результатами.
    """
    calculate()
    file = open('./function_output.txt', 'r')
    string = file.read()
    print(string)
    assert string == '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 \n' \
                     '1 4 9 16 25 36 49 64 81 100 121 144 169 196 225 ' \
                     '256 289 324 361 \n' \
                     '1 8 27 64 125 216 343 512 729 1000 1331 1728 2197 ' \
                     '2744 3375 4096 4913 ' \
                     '5832 6859 \n' \
                     '1 16 81 256 625 1296 2401 4096 6561 10000 14641 ' \
                     '20736 28561 38416 50625 ' \
                     '65536 83521 104976 130321 \n'

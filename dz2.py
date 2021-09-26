import csv
import sys


def get_option(stop_option_: str) -> str:
    """
    Получает 1 из возможных вариантов поведения от пользователя.
    Если пользователь вводит вариант, которого нет в options - просит его повторить попытку.

        Параметр:
            stop_option_: значение, которое приводит к выходу из программы.

        Возвращаемое значение:
            option_: 1 из вариантов поведения программы.

    """
    option_ = 'start'
    options_ = ['1', '2', '3', stop_option_]
    while option_ not in options_:
        print('Выберите:\n'
              '{} - распечатать иерархию команд\n'
              '{} - распечатать сводный отчет\n'
              '{} - записать сводный отчет в csv-файл\n'
              '{} - выйти из программы'.format(*options_))
        option_ = input()
    return option_


def execute_option(option_: str, data_: list):
    """
    Выполняет 1 из возможных вариантов поведения программы.
    Если поступает значение, для которого нет варианта поведения - ничего не делает.

        Параметр:
            option_: 1 из вариантов поведения программы;
            data_: двумерный список с данными.

        Возвращаемое значение:
            Нет (None).
    """
    if option_ == '1':
        teams_hierarchy_dict = create_teams_hierarchy_dict(data_)
        print_teams_hierarchy(teams_hierarchy_dict)
    if option_ == '2':
        departments_with_salaries = create_summary_report_list(data_)
        print_summary_report(departments_with_salaries)
    if option_ == '3':
        departments_with_salaries = create_summary_report_list(data_)
        write_summary_report_to_csv(departments_with_salaries, 'Summary_report.csv')


def read_csv_to_list(file_name_: str, data_list_=None) -> list:
    """
    Считывает данные из csv-файла в двумерный список.

        Параметры:
            file_name_: имя csv-файла с данными;
            data_list_: двумерный список, в который будут считываться данные. Может быть не пустым.

        Возвращаемое значение:
            data_list_: двумерный список со считанными из данными.

    """
    if data_list_ is None:
        data_list_ = []
    with open(file_name_, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            data_list_.append([row['Департамент'], row['Отдел'], row['Оклад']])
    return data_list_


def create_teams_hierarchy_dict(data_list_: list, teams_hierarchy_dict_=None) -> dict:
    """
    Составляет словарь, хранящий иерархию команд.
    Ключ - название департамента.
    Значение - множество команд, соответствующих департаменту.

        Параметры:
            data_list_: список с данными;
            teams_hierarchy_dict_: словарь, хранящий иерархию команд. Может быть не пустым.

        Возвращаемое значение:
            teams_hierarchy_dict_: словарь, хранящий иерархию команд.
    """
    if teams_hierarchy_dict_ is None:
        teams_hierarchy_dict_ = {}
    departments_set = set()
    teams_set = set()
    for row in data_list_:
        if row[0] not in departments_set:
            for row_ in data_list_:
                if row_[0] == row[0] and row_[1] not in teams_set:
                    teams_set.add(row_[1])
            teams_hierarchy_dict_[row[0]] = teams_set
            teams_set = set()
            departments_set.add(row[0])
    return teams_hierarchy_dict_


def print_teams_hierarchy(teams_hierarchy_dict_: dict):
    """
    Печатает иерархию команд в консоль.

        Параметры:
            teams_hierarchy_dict_: словарь, хранящий иерархию команд. Может быть не пустым.

        Возвращаемое значение:
            Нет (None).
    """
    for key in teams_hierarchy_dict_:
        print(f'{key}:')
        teams_string = ', '.join(teams_hierarchy_dict_[key])
        print(f'\t{teams_string}')


def create_summary_report_list(data_list_: list, summary_report_list_=None) -> list:
    """
    Составляет двумерный список summary_report_list_, хранящий сводный отчет по департаментам:
    Столбцы списка:
        0 - название департамента;
        1 - максимальная зарплата;
        2 - минимальная зарплата;
        3 - средняя зарплата.

        Параметры:
            data_list_: список с данными;
            summary_report_list_: двумерный список, хранящий сводный отчет по департаментам.
            Может быть не пустым.

        Возвращаемое значение:
            summary_report_list_: двумерный список, хранящий сводный отчет по департаментам.
    """
    if summary_report_list_ is None:
        summary_report_list_ = []
    departments_set = set()
    min_salary = None
    max_salary = None
    total_salary = 0
    employees_number = 0
    for row in data_list_:
        if row[0] not in departments_set:
            for row_ in data_list_:
                if row_[0] == row[0]:
                    if employees_number == 0:
                        min_salary = int(row_[2])
                        max_salary = int(row_[2])
                        total_salary = int(row_[2])
                    if int(row_[2]) > max_salary:
                        max_salary = int(row_[2])
                    if int(row_[2]) < min_salary:
                        min_salary = int(row_[2])
                    employees_number += 1
                    total_salary += int(row_[2])
            average_salary = round(float(total_salary / employees_number))
            summary_report_list_.append([row[0], max_salary, min_salary, average_salary])
            min_salary = None
            total_salary = 0
            employees_number = 0
            departments_set.add(row[0])
    return summary_report_list_


def print_summary_report(summary_report_list_: list):
    """
    Печатает сводный отчет в консоль.

        Параметры:
            summary_report_list_: двумерный список, хранящий сводный отчет по департаментам.

        Возвращаемое значение:
            Нет (None).
    """
    for row in summary_report_list_:
        print(f'{row[0]}:')
        print(f'\tМаксимальная зарплата: {row[1]}\n'
              f'\tМинимальная зарплата: {row[2]}\n'
              f'\tСредняя зарплата: {row[3]}')


def write_summary_report_to_csv(summary_report_list_: list, file_name_: str):
    """
    Записывает сводный отчет в csv-файл.

        Параметры:
            summary_report_list_: двумерный список, хранящий сводный отчет по департаментам;
            file_name_: название csv-файла для записи сводного отчета.

        Возвращаемое значение:
            Нет (None).
    """
    with open(file_name_, 'w', newline='') as csvfile:
        fieldnames = [
            'Департамент',
            'Максимальная зарплата',
            'Минимальная зарплата',
            'Средняя зарплата'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for el in summary_report_list_:
                writer.writerow({
                    'Департамент': el[0],
                    'Максимальная зарплата': el[1],
                    'Минимальная зарплата': el[2],
                    'Средняя зарплата': el[3]
                })
        except csv.Error as e:
            sys.exit('file {}: {}'.format(csvfile, e))
        else:
            print(f'Сводный отчет успешно записан в файл {file_name_}')


if __name__ == '__main__':
    option = 'start'
    stop_option = '0'
    data = read_csv_to_list('Corp Summary.csv')
    while option != stop_option:
        option = get_option(stop_option)
        print()
        execute_option(option, data)
        print()

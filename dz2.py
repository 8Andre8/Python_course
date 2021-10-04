import csv
import sys
from collections import namedtuple
from statistics import mean


def main() -> None:
    """
    Запускает программный цикл.

        Возвращаемое значение:
            Нет (None).
    """
    option = 'start'
    stop_option = '0'
    data = read_csv_to_list('Corp Summary.csv')
    while option != stop_option:
        option = get_option(stop_option)
        print()
        execute_option(option, data)
        print()


def get_option(stop_option: str) -> str:
    """
    Получает 1 из возможных вариантов поведения от пользователя.
    Если пользователь вводит вариант, которого нет в options - просит его повторить попытку.

        Параметр:
            stop_option: значение, которое приводит к выходу из программы.

        Возвращаемое значение:
            option: 1 из вариантов поведения программы.
    """
    option = 'start'
    options = ['1', '2', '3', stop_option]
    while option not in options:
        print('Выберите:\n'
              '{} - распечатать иерархию команд\n'
              '{} - распечатать сводный отчет\n'
              '{} - записать сводный отчет в csv-файл\n'
              '{} - выйти из программы'.format(*options))
        option = input()
    return option


def execute_option(option: str, data_list: list) -> None:
    """
    Выполняет 1 из возможных вариантов поведения программы.
    Если поступает значение, для которого нет варианта поведения - ничего не делает.

        Параметр:
            option: 1 из вариантов поведения программы;
            data_list: список с данными в виде namedtuple.

        Возвращаемое значение:
            Нет (None).
    """
    if option == '1':
        teams_hierarchy_dict = create_teams_hierarchy_dict(data_list)
        print_teams_hierarchy(teams_hierarchy_dict)
    if option == '2':
        departments_with_salaries = create_summary_report_dict(data_list)
        print_summary_report(departments_with_salaries)
    if option == '3':
        departments_with_salaries = create_summary_report_dict(data_list)
        write_summary_report_to_csv(departments_with_salaries, 'Summary_report.csv')


def read_csv_to_list(file_name: str, data_list=None) -> list:
    """
    Считывает данные из csv-файла в список.

        Параметры:
            file_name: имя csv-файла с данными;
            data_list: список, в который будут считываться данные в виде namedtuple.
            Может быть не пустым.

        Возвращаемое значение:
            data_list: список со считанными из csv-файла данными.

    """
    field_names = [
        'name',
        'department',
        'team',
        'position',
        'mark',
        'salary'
    ]
    if data_list is None:
        data_list = []
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        Row = namedtuple('Row', field_names)
        for row in reader:
            worker_info = Row(*row.values())
            data_list.append(worker_info)
    return data_list


def create_teams_hierarchy_dict(data_list: list, teams_hierarchy_dict=None) -> dict:
    """
    Составляет словарь, хранящий иерархию команд.
    Ключ - название департамента.
    Значение - множество отделов, соответствующих департаменту.

        Параметры:
            data_list: список с данными;
            teams_hierarchy_dict: словарь, хранящий иерархию команд. Может быть не пустым.

        Возвращаемое значение:
            teams_hierarchy_dict: словарь, хранящий иерархию команд.
    """
    if teams_hierarchy_dict is None:
        teams_hierarchy_dict = {}
    for row in data_list:
        teams_hierarchy_dict.setdefault(row.department, set())
        teams_hierarchy_dict[row.department].add(row.team)
    return teams_hierarchy_dict


def print_teams_hierarchy(teams_hierarchy_dict: dict) -> None:
    """
    Печатает иерархию команд в консоль.

        Параметры:
            teams_hierarchy_dict: словарь, хранящий иерархию команд. Может быть не пустым.

        Возвращаемое значение:
            Нет (None).
    """
    for department in teams_hierarchy_dict:
        print(f'{department}:')
        teams_string = ', '.join(teams_hierarchy_dict[department])
        print(f'\t{teams_string}')


def create_summary_report_dict(data_list: list, summary_report_dict=None) -> dict:
    """
    Составляет словарь summary_report_dict, хранящий сводный отчет по департаментам:
    Ключ словаря - название департамента.
    Значение словаря - кортеж namedtuple, состоящий из:
        - количества сотрудников в команде;
        - максимальной зарплаты в команде;
        - минимальной зарплаты в команде;
        - средней зарплаты в команде.

        Параметры:
            data_list: список с данными в виде namedtuple;
            summary_report_dict: двумерный список, хранящий сводный отчет по департаментам.
            Может быть не пустым.

        Возвращаемое значение:
            summary_report_dict: словарь, хранящий сводный отчет по департаментам.
    """
    field_names = [
        'quantity',
        'max_salary',
        'min_salary',
        'average_salary',
    ]
    if summary_report_dict is None:
        summary_report_dict = {}
    for row in data_list:
        summary_report_dict.setdefault(row.department, list())
        summary_report_dict[row.department].append(row.salary)
    Summary = namedtuple('Summary', field_names)
    for department in summary_report_dict:
        department_salary_list = list(map(float, summary_report_dict[department]))
        summary_report_dict[department] = Summary(len(department_salary_list),
                                                  round(max(department_salary_list)),
                                                  round(min(department_salary_list)),
                                                  round(mean(department_salary_list)))
    return summary_report_dict


def print_summary_report(summary_report_dict: dict) -> None:
    """
    Печатает сводный отчет в консоль.

        Параметры:
            summary_report_dict: словарь, хранящий сводный отчет по департаментам.

        Возвращаемое значение:
            Нет (None).
    """
    for department in summary_report_dict:
        print(f'{department}:')
        print(f'\tКоличество работников: {summary_report_dict[department].quantity}\n'
              f'\tМаксимальная зарплата: {summary_report_dict[department].max_salary}\n'
              f'\tМинимальная зарплата: {summary_report_dict[department].min_salary}\n'
              f'\tСредняя зарплата: {summary_report_dict[department].average_salary}\n')


def write_summary_report_to_csv(summary_report_dict: dict, file_name_: str) -> None:
    """
    Записывает сводный отчет в csv-файл.

        Параметры:
            summary_report_dict: словарь, хранящий сводный отчет по департаментам;
            file_name: название csv-файла для записи сводного отчета.

        Возвращаемое значение:
            Нет (None).
    """
    with open(file_name_, 'w', newline='') as csv_file:
        fieldnames = [
            'Департамент',
            'Количество работников',
            'Максимальная зарплата',
            'Минимальная зарплата',
            'Средняя зарплата'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for department in summary_report_dict:
                writer.writerow({
                    'Департамент': department,
                    'Количество работников': summary_report_dict[department].quantity,
                    'Максимальная зарплата': summary_report_dict[department].max_salary,
                    'Минимальная зарплата': summary_report_dict[department].min_salary,
                    'Средняя зарплата': summary_report_dict[department].average_salary
                })
        except csv.Error as e:
            sys.exit('file {}: {}'.format(csv_file, e))
        else:
            print(f'Сводный отчет успешно записан в файл {file_name_}')


if __name__ == '__main__':
    main()

def is_yes():
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()
    return options[option]


def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    if is_yes():
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print('\nУтка-маляр решила взять зонтик. Стоит ли взять с собой ведро?')
    if is_yes():
        return step3_bucket()
    return step3_no_bucket()


def step2_no_umbrella():
    print(
        '\nНееее, ей лень! Она лучше наденет на голову авоську и станет красить асфальт в '
        'серо-коричневый цвет. 🎨')


def step3_bucket():
    print(
        '\nС собой можно взять, а вот куда потом это ведро девать? '
        'И что, утка-маляр станет красить зонтиком? 🤔')


def step3_no_bucket():
    print('\nХватит и бутылки (сидра, конечно) 🍎 😜')


if __name__ == '__main__':
    step1()

from collections import OrderedDict
from collections.abc import Iterable


class CountVectorizer:
    """
    Позволяет конвертировать Iterable объект, состоящий из строк в терм-документную матрицу,
    а также вернуть список уникальных слов этого объекта.
    """

    def __init__(self, lowercase=True):
        self.lowercase = lowercase
        self.vocabulary = OrderedDict()

    def _create_vocabulary(self, corpus: Iterable) -> None:
        """
        Создает/обновляет словарь слов с помощью Iterable объекта coprus, состоящего из строк.
        Запоминает его в виде атрибута vocabulary.
            Параметры:
                corpus: Iterable объект, состоящий из строк.
            Возвращаемое значение:
                None.
        """
        self.vocabulary = OrderedDict()
        words_in_string_dict = OrderedDict()
        for string in corpus:
            if self.lowercase:
                split_string_list = string.lower().split()
            else:
                split_string_list = string.split()
            words_in_string_dict = words_in_string_dict.fromkeys(split_string_list, 0)
            self.vocabulary.update(words_in_string_dict)

    def _create_document_matrix(self, corpus: Iterable) -> list:
        """
        Создает терм-документную матрицу.
            Параметры:
                corpus: Iterable объект, состоящий из строк.
            Возвращаемое значение:
                document_matrix: терм-документная матрица в виде списка.
        """
        document_matrix = list()
        for string in corpus:
            if self.lowercase:
                split_string_list = string.lower().split()
            else:
                split_string_list = string.split()
            words_in_string_counter = self.vocabulary.copy()
            for word in split_string_list:
                words_in_string_counter[word] += 1
            document_matrix.append(list(words_in_string_counter.values()))
        return document_matrix

    def fit_transform(self, corpus: Iterable) -> list:
        """
        Конвертирует Iterable объект coprus, состоящий из строк в терм-документную матрицу,
        а также сохраняет словарь слов в виде атрибута vocabulary.
            Параметры:
                corpus: Iterable объект, состоящий из строк.
            Возвращаемое значение:
                document_matrix: терм-документная матрица в виде списка.
        """
        if isinstance(corpus, Iterable) and not isinstance(corpus, str):
            self._create_vocabulary(corpus)
        else:
            raise TypeError('Требуется Iterable объект, состоящий из строк!')
        document_matrix = self._create_document_matrix(corpus)
        return document_matrix

    def get_feature_names(self) -> list:
        """
        Возвращает список слов словаря (атрибут vocabulary).
            Возвращаемое значение:
                список слов словаря (атрибут vocabulary)
        """
        return list(self.vocabulary.keys())


if __name__ == '__main__':
    # тест 1 - пример из задания
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    c = CountVectorizer()
    count_matrix = c.fit_transform(corpus)
    assert count_matrix == [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]], count_matrix
    assert c.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil',
                                     'again', 'pomodoro', 'fresh', 'ingredients',
                                     'parmesan', 'to', 'taste'], c.get_feature_names()
    # тест 2 - пример из задания + False lowercase
    c.lowercase = False
    count_matrix = c.fit_transform(corpus)
    assert count_matrix == [[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]], count_matrix
    assert c.get_feature_names() == ['Crock', 'Pot', 'Pasta', 'Never', 'boil', 'pasta',
                                     'again', 'Pomodoro', 'Fresh', 'ingredients',
                                     'Parmesan', 'to', 'taste'], c.get_feature_names()
    # тест 3 - пример из задания + tuple вместо list
    c3 = CountVectorizer()
    count_matrix = c3.fit_transform(tuple(corpus))
    assert count_matrix == [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]], count_matrix
    assert c3.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil',
                                      'again', 'pomodoro', 'fresh', 'ingredients',
                                      'parmesan', 'to', 'taste'], c.get_feature_names()
    # тест 4 - пустой ввод
    c4 = CountVectorizer()
    count_matrix = c4.fit_transform([])
    assert count_matrix == [], count_matrix
    assert c4.get_feature_names() == [], c4.get_feature_names()
    # тест 5 - одинаковые слова
    c5 = CountVectorizer()
    count_matrix = c5.fit_transform(['word', 'word', 'word',
                                     'word', 'word']) == [[1], [1]], count_matrix
    assert c5.get_feature_names() == ['word'], c5.get_feature_names()
    # тест 6 - все разные слова
    c6 = CountVectorizer()
    count_matrix = c6.fit_transform(['word1', 'word2', 'word3',
                                     'word4', 'word5']) == [[1, 1, 1, 0, 0],
                                                            [0, 0, 0, 1, 1]], count_matrix
    assert c6.get_feature_names() == ['word1', 'word2', 'word3',
                                      'word4', 'word5'], c6.get_feature_names()
    # тест 7.1 - одинаковые слова с разным регистром
    c7 = CountVectorizer()
    count_matrix = c7.fit_transform(['word', 'WORD', 'WOrd',
                                     'worD', 'Word']) == [[1], [1]], count_matrix
    assert c7.get_feature_names() == ['word'], c7.get_feature_names()
    # тест 7.2 - одинаковые слова с разным регистром + False lowercase
    c7.lowercase = False
    count_matrix = c7.fit_transform(['word', 'WORD', 'WOrd',
                                     'worD', 'Word']) == [[1, 1, 1, 0, 0],
                                                          [0, 0, 0, 1, 1]], count_matrix
    assert c7.get_feature_names() == ['word', 'WORD', 'WOrd',
                                      'worD', 'Word'], c7.get_feature_names()
    # тесты на ошибки
    # c8 = CountVectorizer()
    # c8.fit_transform(124234)
    # c8.fit_transform('124234')

from collections import OrderedDict
from collections.abc import Iterable
from typing import List
import math
from operator import mul


class CountVectorizer:
    """
    Позволяет конвертировать Iterable объект,
    состоящий из строк в терм-документную матрицу,
    а также вернуть список уникальных слов этого объекта.
    """

    def __init__(self, lowercase=True):
        self.lowercase = lowercase
        self.vocabulary = OrderedDict()

    def _create_vocabulary(self, corpus: Iterable):
        """
        Создает/обновляет словарь слов с помощью Iterable объекта coprus,
        состоящего из строк.
        Запоминает его в виде атрибута vocabulary.
            Параметры:
                corpus: Iterable объект, состоящий из строк.
        """
        self.vocabulary = OrderedDict()
        words_in_string_dict = OrderedDict()
        for string in corpus:
            if self.lowercase:
                split_string_list = string.lower().split()
            else:
                split_string_list = string.split()
            words_in_string_dict = \
                words_in_string_dict.fromkeys(split_string_list, 0)
            self.vocabulary.update(words_in_string_dict)

    def _create_document_matrix(self, corpus: Iterable) -> List[List[int]]:
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

    def fit_transform(self, corpus: Iterable) -> List[List[int]]:
        """
        Конвертирует Iterable объект coprus,
        состоящий из строк в терм-документную матрицу,
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

    def get_feature_names(self) -> List[str]:
        """
        Возвращает список слов словаря (атрибут vocabulary)
            Возвращаемое значение:
                список слов словаря (атрибут vocabulary).
        """
        return list(self.vocabulary.keys())


def tf_transform(count_matrix: List[List[int]]) -> List[List[float]]:
    """
    Принимает на вход терм-документную матрицу
    и возвращает матрицу частот (tf).
        Параметр:
            count_matrix: терм-документная матрица.
        Возвращаемое значение:
        tf-matrix: матрица частот той же размерности, что и count_matrix.
    """
    tf_matrix = []
    for row in count_matrix:
        words_number_in_row = sum(row)
        tf_matrix.append([round(val / words_number_in_row, 3) for val in row])
    return tf_matrix


def idf_transform(count_matrix: List[List[int]]) -> List[float]:
    """
    Принимает на вход терм-документную матрицу
    и возвращает матрицу обратных частот (idf).
        Параметр:
            count_matrix: терм-документная матрица.
        Возвращаемое значение:
            idf_vector: вектор обратных частот,
            который совпадает по размерности с количеством слов (документов).
            В count-matrix - это число равняется длине строк.
    """
    documents_number = len(count_matrix)
    idf_vector = []
    for i, _ in enumerate(count_matrix[0]):
        documents_with_word_number = 0
        for row in count_matrix:
            if row[i] > 0:
                documents_with_word_number += 1
        idf_vector.append(
            round(math.log((documents_number + 1) /
                           (documents_with_word_number + 1)) + 1, 3))
    return idf_vector


class TfidfTransformer:
    """
    Позволяет конвертировать терм-документную матрицу в tf-idf-матрицу при
    помощи метода fit-transform.
    """

    @staticmethod
    def _tf_transform(count_matrix: List[List[int]]) -> List[List[float]]:
        """
        Принимает на вход терм-документную матрицу
        и возвращает матрицу частот (tf).
            Параметр:
                count_matrix: терм-документная матрица.
            Возвращаемое значение:
            tf-matrix: матрица частот той же размерности, что и count_matrix.
        """
        tf_matrix = []
        for row in count_matrix:
            words_number_in_row = sum(row)
            tf_matrix.append([round(val /
                                    words_number_in_row, 3) for val in row])
        return tf_matrix

    @staticmethod
    def _idf_transform(count_matrix: List[List[int]]) -> List[float]:
        """
        Принимает на вход терм-документную матрицу
        и возвращает матрицу обратных частот (idf).
            Параметр:
                count_matrix: терм-документная матрица.
            Возвращаемое значение:
                idf_vector: вектор обратных частот,
                который совпадает по размерности с количеством слов
                (документов). В count-matrix - это число равняется длине строк.
        """
        documents_number = len(count_matrix)
        idf_vector = []
        for i, _ in enumerate(count_matrix[0]):
            documents_with_word_number = 0
            for row in count_matrix:
                if row[i] > 0:
                    documents_with_word_number += 1
            idf_vector.append(
                round(math.log((documents_number + 1) / (
                        documents_with_word_number + 1)) + 1, 3))
        return idf_vector

    def fit_transform(self, count_matrix: List[List[int]]) \
            -> List[List[float]]:
        """
        Принимает на вход терм-документную матрицу (count-matrix)
        и возвращает tf-idf-матрицу, совпадающую по размерности с count-matrix.
            Параметр:
                count_matrix: терм-документная матрица.
            Возвращаемое значение:
                tfidf_matrix: tf-idf-матрица, которая совпадает
                по размерности терм-документной матрицей (count-matrix).
        """
        tf_matrix = self._tf_transform(count_matrix)
        idf_vector = self._idf_transform(count_matrix)
        tfidf_matrix = []
        for row_tf in tf_matrix:
            tfidf_matrix.append(list(map(mul, row_tf, idf_vector)))
        return tfidf_matrix


class TfidfVectorizer(CountVectorizer):
    """
    Класс, который наследуется от класса CountVectorizer
    и является композицией с классом TfidfTransformer.
    Позволяет конвертировать Iterable объект,
    состоящий из строк в tf-idf-матрицу,
    а также вернуть список уникальных слов этого объекта.
    """

    def __init__(self):
        super().__init__()
        self.tfidf_transformer = TfidfTransformer()

    def fit_transform(self, corpus: Iterable) -> List[List[float]]:
        """
        Принимает на вход Iterable объект, состоящий из строк,
        и возвращает tf-idf-матрицу.
            Параметр:
                corpus: Iterable объект, состоящий из строк.
            Возвращаемое значение:
                tfidf_matrix: tf-idf-матрица, которая совпадает
                по размерности терм-документной матрицей (count-matrix).
        """
        document_matrix = super().fit_transform(corpus)
        tfidf_matrix = self.tfidf_transformer.fit_transform(document_matrix)
        return tfidf_matrix


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
    assert c.get_feature_names() == \
           ['crock', 'pot', 'pasta', 'never', 'boil',
            'again', 'pomodoro', 'fresh', 'ingredients',
            'parmesan', 'to', 'taste'], c.get_feature_names()
    print('CountVectorizer.get_feature_names::', c.get_feature_names())
    print('CountVectorizer.fit_transform:', count_matrix)
    print()
    assert tf_transform(count_matrix) == [
        [0.143, 0.143, 0.286, 0.143, 0.143, 0.143, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.143, 0.143, 0.143, 0.143, 0.143,
         0.143]
    ], tf_transform(count_matrix)
    tf = tf_transform(count_matrix)
    print('tf:', tf)
    assert idf_transform(count_matrix) == [
        1.405, 1.405, 1.0, 1.405, 1.405, 1.405,
        1.405, 1.405, 1.405, 1.405, 1.405, 1.405
    ], idf_transform(count_matrix)
    print('idf:', idf_transform(count_matrix))

    t = TfidfTransformer()
    assert t.fit_transform(count_matrix) == [
        [0.20091499999999998, 0.20091499999999998, 0.286,
         0.20091499999999998, 0.20091499999999998, 0.20091499999999998,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.20091499999999998,
         0.20091499999999998, 0.20091499999999998, 0.20091499999999998,
         0.20091499999999998, 0.20091499999999998]
    ], t.fit_transform(count_matrix)
    print('tf-idf:', t.fit_transform(count_matrix))
    print()
    v = TfidfVectorizer()
    assert v.fit_transform(corpus) == [
        [0.20091499999999998, 0.20091499999999998, 0.286,
         0.20091499999999998, 0.20091499999999998, 0.20091499999999998,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.20091499999999998,
         0.20091499999999998, 0.20091499999999998, 0.20091499999999998,
         0.20091499999999998, 0.20091499999999998]
    ], v.fit_transform(corpus)
    print('TfidfVectorizer.fit_transform:', v.fit_transform(corpus))
    assert v.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again',
        'pomodoro', 'fresh', 'ingredients', 'parmesan', 'to', 'taste'
    ], v.get_feature_names()
    print('TfidfVectorizer.get_feature_names:', v.get_feature_names())

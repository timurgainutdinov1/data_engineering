import numpy as np
import json
import collections


def calc_stats(values):

    '''
    Принимает список значений, возвращает словарь с результатами вычислений суммы значений,
    минимального и максимального значений, среднего арифметического значения и стандартного отклонения
    '''

    stats = {
        'total': round(sum(values), 1),
        'min_value': min(values),
        'max_value': max(values),
        'average_value': round(np.mean(values), 2),
        'std_value': round(np.std(values), 2)
    }
    return stats


def save(items, task_num):

    '''
    Принимает список параметров объектов и номер задания,
    выполняет сохранение данных в формате json
    с указанием номера задания
    '''

    with open(f'task_{task_num}_multiple_result.json', 'w', encoding='utf-8') as output_file:
        json.dump(items, output_file, indent=4, ensure_ascii=False)


def properties_count_calc(props, prop):
    """
    Подсчитывает частоту встречаемости значений необходимого поля
    """

    properties_count = dict(collections.Counter(props))
    items = []
    for p in set(props):
        item = dict()
        item[prop] = p
        item['count'] = properties_count[p]
        items.append(item)

    return items

import numpy as np
import json
import zipfile

with zipfile.ZipFile('data.zip', 'r') as zip_ref:
    zip_ref.extractall()


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

    with open(f'task_{task_num}_result.json', 'w') as output_file:
        json.dump(items, output_file, indent=4, ensure_ascii=False)

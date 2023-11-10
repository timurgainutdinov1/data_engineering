import urllib.request
import csv
import json
import msgpack
import pickle
import numpy as np
import collections
import os.path

# Загружаем файл с исходными данными
destination = 'import_data.csv'
url = 'https://data.transportation.gov/api/views/keg4-3bc2/rows.csv?accessType=DOWNLOAD'
urllib.request.urlretrieve(url, destination)

items = list()
values = list()

# Анализируем статистику по въездным пересечениям границ США-Канады и США-Мексики на уровне порта
with open('import_data.csv', newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file, delimiter=',')

    # Пропускаем шапку таблицы
    reader.__next__()

    for row in reader:

        # Год и месяц будем рассматривать отдельно
        date = row[4].split()

        item = {
            'port_name': row[0],
            'state': row[1],
            'port_code': row[2],
            'border': row[3],
            'year': date[1],
            'month': date[0],
            'mode_of_transportation': row[5],
            'value': int(row[6])
        }
        # Отдельно сохраняем данные по объемам пересечений границ
        # для дальнейшей обработки
        values.append(item['value'])

        items.append(item)

# Обрабатываем данные по объемам пересечений границ
sum_value = sum(values)
average_value = sum_value / len(values)
max_value = max(values)
min_value = min(values)
std_value = np.std(values)

# Для поиска наиболее встречаемых штатов, границ и транспортов
# создаем отдельные списки
states = list()
borders = list()
modes_of_transportation = list()

# Заполняем списки по штатам, границам и транспорту
for item in items:
    for param, value in item.items():
        if param == 'state':
            states.append(value)
        elif param == 'border':
            borders.append(value)
        elif param == 'mode_of_transportation':
            modes_of_transportation.append(value)

# Создаем и заполняем словарь с результатами анализа
result = {
    'sum_value': sum_value,
    'average_value': average_value,
    'max_value': max_value,
    'min_value': min_value,
    'std_value': std_value,
    'most_common_state': collections.Counter(states).most_common(1),
    'most_common_border': collections.Counter(borders).most_common(1),
    'mode_of_transportation': collections.Counter(modes_of_transportation).most_common(1),
}

with open('task_5_result.json', 'w') as output_file:
    json.dump(result, output_file, indent=4)

with open('task_5_data.csv', 'w', encoding='utf-8', newline='') as output_file_csv:
    writer = csv.writer(output_file_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Записываем шапку таблицы
    writer.writerow(items[0].keys())

    for item in items:
        writer.writerow(item.values())

with open('task_5_data.json', 'w') as output_file_json:
    json.dump(items, output_file_json)

with open('task_5_data.msgpack', 'wb') as output_file_msgpack:
    msgpack.dump(items, output_file_msgpack)

with open('task_5_data.pkl', 'wb') as output_file_pkl:
    pickle.dump(items, output_file_pkl)

data_size = {
    'csv': os.path.getsize('task_5_data.csv'),
    'json': os.path.getsize('task_5_data.json'),
    'msgpack': os.path.getsize('task_5_data.msgpack'),
    'pkl': os.path.getsize('task_5_data.pkl')
}

print(data_size)

print(f'{max(data_size, key=data_size.get)} has the max size of file')
print(f'{min(data_size, key=data_size.get)} has the min size of file')

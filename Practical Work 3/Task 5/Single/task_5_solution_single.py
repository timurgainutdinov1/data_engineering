from bs4 import BeautifulSoup
import collections
import json
import MyModule


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        props = site.find(attrs={"class": "place-char"}).find_all('div')
        props = [prop.contents for prop in props]
        for prop in props:
            item[prop[0].string.replace('\xa0', ' ')] = prop[1].strip()

        item['Цена'] = int(site.find_all('span', attrs={"class": "price"})[0].string.replace(' ', ''))

        item['Длина, м'] = int(item['Длина, м'])
        item['Ширина, м'] = float(item['Ширина, м'].replace(',', '.'))
        item['Количество в упаковке, рул'] = int(item['Количество в упаковке, рул'])
        item['Вес упаковки, кг'] = int(item['Вес упаковки, кг'])

    return item


items = list()

for i in range(1, 37):
    file_name = f'{i}.html'
    result = handle_file(file_name)
    items.append(result)

# Запись данных в json
with open(f'task_5_result_single.json', 'w') as output_file:
    json.dump(items, output_file, indent=4, ensure_ascii=False)

# Сортировка списка по полю 'Цена' в порядке возрастания
items = sorted(items, key=lambda x: x['Цена'])
# print(items)

# Фильтрация списка по критерию: цвет - серый
filtered_items = list(filter(lambda x: x['Цвет'] == 'серый', items))
# print(filtered_items)
# print(len(items))
# print(len(filtered_items))

# Формирование списка из значений всех цен
prices = list(map(lambda x: x['Цена'], items))
# print(prices)

# Расчет статистических характеристик
prices_stats = MyModule.calc_stats(prices)
# print(prices_stats)

# Формирование списка из значений поля 'Цвет'
colors = list(map(lambda x: x['Цвет'], items))
# print(colors)

# Расчет частоты меток в поле 'Цвет'
colors_count = dict(collections.Counter(colors))
# print(colors_count)

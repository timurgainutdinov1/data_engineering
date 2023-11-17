from bs4 import BeautifulSoup
import collections
import MyModule


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'xml').star

        item = dict()

        props = star.find_all()
        for prop in props:
            item[prop.name.strip()] = prop.string.strip()

    item["radius"] = int(item["radius"])

    return item


items = list()

for i in range(1, 501):
    file_name = f'{i}.xml'
    result = handle_file(file_name)
    items.append(result)


# Запись данных в json
MyModule.save(items, 3)

# Сортировка по радиусу в порядке возрастания
items = sorted(items, key=lambda x: x["radius"])
# print(items)

# Фильтрация по полю 'constellation' -> Овен
filtered_items = list(filter(lambda x: x['constellation'] == 'Овен', items))
# print(filtered_items)
# print(len(items))
# print(len(filtered_items))

# Формирование списка из полей 'age'
ages = list(map(lambda x: float(x['age'].replace(' billion years', '')), items))
# print(ages)

# Расчет статистических характеристик
ages_stats = MyModule.calc_stats(ages)
# print(ages_stats)

# Формирование списка из значений поля "constellation"
constellations = list(map(lambda x: x['constellation'], items))
# print(constellations)

# Расчет частоты меток в поле "constellation"
constellations_count = dict(collections.Counter(constellations))
# print(constellations_count)

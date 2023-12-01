from bs4 import BeautifulSoup
import MyModule


def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        clothings = BeautifulSoup(text, 'xml').find_all('clothing')

        for clothing in clothings:
            item = dict()
            props = clothing.find_all()

            for prop in props:
                item[prop.name.strip()] = prop.string.strip()

            item['price'] = int(item['price'])
            item['reviews'] = int(item['reviews'])

            items.append(item)

    return items


items = list()
for i in range(1, 101):
    file_name = f'{i}.xml'
    items += handle_file(file_name)

# Запись данных в json
MyModule.save(items, 4)

# Сортировка списка по цене в порядке возрастания
items = sorted(items, key=lambda x: x["price"])
MyModule.save(items, 4.1)

# Фильтрация списка по полю 'material' -> 'Хлопок'
filtered_items = list(filter(lambda x: x['material'] == 'Хлопок', items))
MyModule.save(filtered_items, 4.2)

# Формирование списка из значений поля 'reviews'
reviews_values = list(map(lambda x: x['reviews'], items))

# Расчет статистических характеристик
reviews_values_stats = MyModule.calc_stats(reviews_values)
MyModule.save(reviews_values_stats, 4.3)

# Формирование списка из значений поля 'size'
sizes = list(map(lambda x: x['size'], items))

# Расчет частоты меток в поле 'size'
sizes_counts = MyModule.properties_count_calc(sizes, 'size')
MyModule.save(sizes_counts, 4.4)

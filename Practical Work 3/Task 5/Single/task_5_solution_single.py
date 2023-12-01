from bs4 import BeautifulSoup
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
            match prop[0].string.replace('\xa0', ' '):
                case "Страна производитель":
                    item['manufacturer_country'] = prop[1].strip()
                case "Бренд":
                    item['brand'] = prop[1].strip()
                case "Фабрика":
                    item['factory'] = prop[1].strip()
                case "Торговая марка":
                    item['trademark'] = prop[1].strip()
                case "Коллекция":
                    item['collection'] = prop[1].strip()
                case "Тип обоев":
                    item['type'] = prop[1].strip()
                case "Основа":
                    item['backing'] = prop[1].strip()
                case "Ширина, м":
                    item['width_m'] = float(prop[1].strip().replace(',', '.'))
                case "Длина, м":
                    item['length_m'] = int(prop[1].strip())
                case "Цвет":
                    item['color'] = prop[1].strip()
                case "Раппорт, см":
                    item['spread_cm'] = prop[1].strip()
                case "Дизайн":
                    item['design'] = prop[1].strip()
                case "Вес упаковки, кг":
                    item['package_weight_kg'] = int(prop[1].strip())
                case "Количество в упаковке, рул":
                    item['number_in_package_roll'] = int(prop[1].strip())

        item['price'] = int(site.find_all('span', attrs={"class": "price"})[0].string.replace(' ', ''))

    return item


items = list()

for i in range(1, 37):
    file_name = f'{i}.html'
    result = handle_file(file_name)
    items.append(result)

# Запись данных в json
MyModule.save(items, 5)

# Сортировка списка по полю 'price' в порядке возрастания
items = sorted(items, key=lambda x: x['price'])
MyModule.save(items, 5.1)

# Фильтрация списка по критерию: color - серый
filtered_items = list(filter(lambda x: x['color'] == 'серый', items))
MyModule.save(filtered_items, 5.2)

# Формирование списка из значений всех цен
prices = list(map(lambda x: x['price'], items))

# Расчет статистических характеристик
prices_stats = MyModule.calc_stats(prices)
MyModule.save(prices_stats, 5.3)

# Формирование списка из значений поля 'color'
colors = list(map(lambda x: x['color'], items))

# Расчет частоты меток в поле 'color'
color_counts = MyModule.properties_count_calc(colors, 'color')
MyModule.save(color_counts, 5.4)

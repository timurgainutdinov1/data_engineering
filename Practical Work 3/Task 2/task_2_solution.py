from bs4 import BeautifulSoup
import MyModule


def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all('div', attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['model'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
            item['bonus'] = int(product.strong.get_text().split()[2])

            props = product.ul.find_all('li')
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

    return items


items = list()
for i in range(1, 61):
    file_name = f'{i}.html'
    items += handle_file(file_name)

# Запись данных в json
MyModule.save(items, 2)

# Сортировка списка по цене в порядке возрастания
items = sorted(items, key=lambda x: x["price"])
MyModule.save(items, 2.1)

# Фильтрация списка по критерию: производитель Lenovo
filtered_items = list(filter(lambda x: x['model'].split()[1] == 'Lenovo', items))
MyModule.save(filtered_items, 2.2)

# Формирование списка из значений цен
prices = list(map(lambda x: x['price'], items))

# Расчет статистических характеристик
prices_stats = MyModule.calc_stats(prices)
MyModule.save(prices_stats, 2.3)

# Формирование списка из всех производителей
creators = list(map(lambda x: x['model'].split()[1], items))

# Расчет частоты производителей
creators_counts = MyModule.properties_count_calc(creators, 'model')
MyModule.save(creators_counts, 2.4)

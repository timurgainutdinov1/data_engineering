from bs4 import BeautifulSoup
import MyModule


def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser').find('div', attrs={'class': 'place-listing'})

        products_data = site.find_all('a')
        for product_data in products_data[:12]:
            item = dict()
            item["link"] = 'https://www.domdekora66.ru' + product_data.get('href')
            item["img"] = product_data.find('span').get('data-img')
            item["code"] = product_data.find('span', attrs={'class': 'name pl'}).contents[0].strip()
            item["brand"] = product_data.find('span', attrs={'class': 'name pl'}).contents[2].strip()
            item["price"] = int(product_data.find('span', attrs={'class': 'pr'}).string.replace(' ', ''))

            items.append(item)

    return items


items = list()
for i in range(1, 4):
    file_name = f'{i}.html'
    items += handle_file(file_name)

links = [item["link"] for item in items]

# Запись ссылок на страницы с конкретным продуктом для дальнейшей обработки
with open(f'../Single/links', 'w', encoding="utf-8") as links_file:
    links_file.writelines([string + '\n' for string in links])

# Запись данных в json
MyModule.save(items, 5)

# Сортировка списка по цене в порядке возрастания
items = sorted(items, key=lambda x: x["price"])
MyModule.save(items, 5.1)

# Фильтрация списка по производителю: BELVINIL
filtered_items = list(filter(lambda x: x["brand"] == "BELVINIL", items))
MyModule.save(filtered_items, 5.2)

# Формирование списка из значений цен
prices = list(map(lambda x: x['price'], items))

# Расчет статистических характеристик
prices_stats = MyModule.calc_stats(prices)
MyModule.save(prices_stats, 5.3)

# Формирование списка из всех производителей
brands = list(map(lambda x: x['brand'], items))

# Расчет частоты производителей
brand_counts = MyModule.properties_count_calc(brands, 'brand')
MyModule.save(brand_counts, 5.4)

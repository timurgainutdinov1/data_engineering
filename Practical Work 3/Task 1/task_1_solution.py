from bs4 import BeautifulSoup
import re
import collections
import MyModule


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        item['type'] = site.find_all('span', string=re.compile('Тип:'))[0].get_text().replace('Тип:', '').strip()
        item['title'] = site.find_all('h1')[0].get_text().replace('Турнир:', '').strip()

        # Обработка ошибок, вызванных некорректными данными по городу и дате подобно файлу №2
        try:
            city_and_date = site.find_all('p')[0].get_text().split()
            item['city'] = city_and_date[1]
            item['date'] = city_and_date[3]
        except IndexError:
            city_and_date = (site.find_all('p')[0].get_text()
                             .replace('Город:', '').replace('Начало:', '').split())
            item['city'] = city_and_date[0]
            item['date'] = city_and_date[1]

        item['tours_count'] = int(site.find_all('span', attrs={'class': 'count'})[0]
                                  .get_text().replace('Количество туров:', '').strip())
        item['time_limit'] = int(site.find_all('span', attrs={'class': 'year'})[0].get_text().split()[2])
        item['rating_limit'] = int(site.find_all('span', string=re.compile('Минимальный рейтинг для участия:'))[0]
                                   .get_text().split(':')[1].strip())

        item['img'] = site.find_all('img')[0]['src']

        item['rating'] = float(site.find_all('span', string=re.compile('Рейтинг:'))[0]
                               .get_text().replace('Рейтинг:', '').strip())
        item['views'] = int(site.find_all('span', string=re.compile('Просмотры:'))[0]
                            .get_text().replace('Просмотры:', '').strip())
        return item


items = list()

for i in range(1, 1000):
    file_name = f'{i}.html'
    result = handle_file(file_name)
    items.append(result)

# Запись данных в json
MyModule.save(items, 1)

# Сортировка списка турниров по рейтингу в порядке возрастания
items = sorted(items, key=lambda x: x["rating"])
# print(items)

# Фильтрация списка турниров по критерию: количество туров не менее 15
filtered_items = list(filter(lambda x: x['tours_count'] >= 15, items))
# print(filtered_items)
# print(len(items))
# print(len(filtered_items))

# Формирование списка из значений рейтингов всех турниров
rating_values = list(map(lambda x: x['rating'], items))
# print(rating_values)

# Расчет статистических характеристик
rating_values_stats = MyModule.calc_stats(rating_values)
# print(rating_values_stats)

# Формирование списка из типов турниров
type_values = list(map(lambda x: x['type'], items))
# print(type_values)

# Расчет частоты меток в поле 'type'
type_count = dict(collections.Counter(type_values))
# print(type_count)

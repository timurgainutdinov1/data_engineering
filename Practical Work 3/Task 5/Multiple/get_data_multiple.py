import requests

for i in range(1, 4):

    r = requests.get(f'https://www.domdekora66.ru/katalog/oboi/page/{i}/').text

    with open(f'{i}.html', 'w', encoding="utf-8") as file:
        file.write(r)
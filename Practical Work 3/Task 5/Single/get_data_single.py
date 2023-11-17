import requests

links = list()

with open('links', 'r') as file:
    links = file.readlines()
    print(links)

i = 1
for link in links:
    r = requests.get(link.strip()).text
    with open(f'{i}.html', 'w', encoding="utf-8") as file:
        file.write(r)
    i += 1

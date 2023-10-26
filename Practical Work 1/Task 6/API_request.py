import requests
import json

url = 'https://api.openweathermap.org/data/2.5/weather?lat=56.839104&lon=60.60825&appid=bd5e378503939ddaee76f12ad7a97608'

response = requests.get(url)
response.raise_for_status()
data = response.json()

with open('text_6.json', 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, indent=4, ensure_ascii=False)

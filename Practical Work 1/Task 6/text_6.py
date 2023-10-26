import json
from bs4 import BeautifulSoup

str_json = ''

with open('text_6.json', encoding='utf-8') as input_file:
    lines = input_file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)

soup = BeautifulSoup(f"""<table>
        <tr>
            <th>Coordination</th>
            <th>Weather</th>
            <th>Temperature, °C</th>
            <th>Pressure, hPa</th>
            <th>Humidity, %</th>
            <th>Wind speed, meter/sec</th>
            <th>Cloudiness, %</th>
        </tr>
        <tr>
            <td align="center">Longitude: {data['coord']['lon']}, Latitude: {data['coord']['lat']}</td>
            <td align="center">{data['weather'][0]['main']}</td>
            <td align="center">{round(float(data['main']['temp'])-273.15)}</td>
            <td align="center">{data['main']['pressure']}</td>
            <td align="center">{data['main']['humidity']}</td>
            <td align="center">{data['wind']['speed']}</td>
            <td align="center">{data['clouds']['all']}</td>
        </tr>
</table>""", "html.parser")

with open('text_6_result.html', 'w', encoding='utf-8') as output_file:
    output_file.write(soup.prettify())

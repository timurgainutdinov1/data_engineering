import json
import msgpack
import os.path

with open('products_31.json') as input_file:
    data = json.load(input_file)

products = dict()

for item in data:
    if item['name'] in products:
        products[item['name']].append(item['price'])
    else:
        products[item['name']] = list()
        products[item['name']].append(item['price'])

result = list()

for key, value in products.items():

    avr_price = sum(value)
    max_price = max(value)
    min_price = min(value)

    result.append({
        'name': key,
        'avr_price': avr_price,
        'max_price': max_price,
        'min_price': min_price
    })

with open('products_31_result.json', 'w') as output_file_json:
    json.dump(result, output_file_json)

with open('products_31_result.msgpack', 'wb') as output_file_msgpack:
    msgpack.dump(result, output_file_msgpack)

print(f"Size of json   : {os.path.getsize('products_31_result.json')}")
print(f"Size of msgpack: {os.path.getsize('products_31_result.msgpack')}")

import json
import pickle


def update_price(price_info, products):
    method = price_info['method']
    if method == "sum":
        products[price_info['name']] += product_info["param"]
    elif method == "sub":
        products[price_info['name']] -= product_info["param"]
    elif method == "percent+":
        products[price_info['name']] *= (1 + product_info["param"])
    elif method == "percent-":
        products[price_info['name']] *= (1 - product_info["param"])


with open("products_31.pkl", "rb") as input_file:
    products = pickle.load(input_file)

with open("price_info_31.json") as input_file:
    price_info = json.load(input_file)

# Создание словаря по типу: продукт -> цена
products_dict = dict()
for items in products:
    products_dict[items['name']] = items['price']

# Обновление цен
for product_info in price_info:
    update_price(product_info, products_dict)

# Формирование списка из словарей по типу входного файла pkl
result = list()
for product, price in products_dict.items():
    result.append({
        'name': product,
        'price': round(price, 2)
    })

with open("products_31_result.pkl", "wb") as output_file:
    pickle.dump(result, output_file)

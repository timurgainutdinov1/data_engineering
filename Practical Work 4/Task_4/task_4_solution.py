import csv
import msgpack
import MyModuleCS


def load_product_data(file_name):
    with open(file_name, 'rb') as f:
        products = msgpack.load(f)
    unique_products_names = set(map(lambda item: item['name'], products))
    unique_products = []
    for product in products:
        if product["name"] in unique_products_names:
            product["quantity"] = int(product["quantity"])
            product["views"] = int(product["views"])
            product["price"] = float(product["price"])
            product["isAvailable"] = product["isAvailable"] == "True"
            product.setdefault("category", "no")
            unique_products.append(product)
            unique_products_names.remove(product["name"])
        else:
            continue
    return unique_products


def load_update_data(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        reader.__next__()

        for row in reader:
            if len(row) == 0:
                continue
            item = dict()
            item["name"] = row[0]
            item["method"] = row[1]
            if item["method"] == "available":
                item["param"] = row[2] == "True"
            elif item["method"] != "remove":
                item["param"] = float(row[2])
            items.append(item)

    return items


# Добавление данных в таблицу в базе данных
def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES(
            :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
        )
        """, data)

    db.commit()


def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE name = ?", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)",
                         [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET isAvailable = ? WHERE name = ?", [param, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = quantity + ? WHERE name = ? AND (quantity + ?) > 0",
                         [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case "remove":
                print(f"deleting {item['name']}")
                delete_by_name(db, item['name'])
            case "price_percent":
                print(f"update price {item['name']} {item['param']} %")
                update_price_by_percent(db, item['name'], item['param'])
            case "price_abs":
                print(f"update price {item['name']} {item['param']}")
                update_price(db, item['name'], item['param'])
            case "available":
                print(f"update available {item['name']} {item['param']}")
                update_available(db, item['name'], item['param'])
            case "quantity_add":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case "quantity_sub":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case _:
                print(f"unknown method {item['method']}")


# Определение топ-10 самых обновляемых товаров
def get_top_by_version(db):
    cursor = db.cursor()
    res = cursor.execute("SELECT name, version FROM product ORDER BY version DESC LIMIT 10")
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Расчет данных (сумма, мин, макс, среднее) по полю 'price' для групп,
# а также кол-ва товаров в группе
def get_stat_by_price_and_count_for_group(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category,
            SUM(price) as sum, 
            ROUND(AVG(price), 2) as avg, 
            MIN(price) as min,
            MAX(price) as max,
            COUNT (*) as count
        FROM product
        GROUP BY category
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Расчет остатков для каждой группы
def get_stat_by_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category,
        SUM(quantity) as quantity
        FROM product
        GROUP BY category
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Поиск самого дешевого и доступного товара из категории
def get_cheapest_and_available_fruit(db, category):
    cursor = db.cursor()
    res = cursor.execute("""SELECT name, price
                            FROM product
                            WHERE category = ? AND isAvailable = 1
                            ORDER BY price
                            """, [category])
    result = dict(res.fetchone())
    cursor.close()

    return result

items = load_product_data("task_4_var_31_product_data.msgpack")
db = MyModuleCS.db_connection("../third")
# insert_data(db, items)
# updates = load_update_data("task_4_var_31_update_data.csv")
# handle_update(db, updates)
MyModuleCS.saving(get_top_by_version(db), "task_3_res_first")
MyModuleCS.saving(get_stat_by_price_and_count_for_group(db), "task_3_res_second")
MyModuleCS.saving(get_stat_by_quantity(db), "task_3_res_third")
MyModuleCS.saving(get_cheapest_and_available_fruit(db, "fruit"), "task_3_res_fourth")

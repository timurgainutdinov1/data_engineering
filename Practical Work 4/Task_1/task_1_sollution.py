import pickle
import MyModuleCS


# Загрузка данных, приведение типов некоторых полей, удаление поля 'id'
def load_data(file_name):
    with open(file_name, "rb") as input_file:
        items = pickle.load(input_file)

    for item in items:
        item["zipcode"] = int(item["zipcode"])
        item["floors"] = int(item["floors"])
        item["year"] = int(item["year"])
        item["prob_price"] = int(item["prob_price"])
        item["views"] = int(item["views"])
        del item["id"]

    return items


# Добавление данных в таблицу в базе данных
def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO building (name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES(
            :name, :street, :city, :zipcode,
            :floors, :year, :parking, :prob_price, :views
        )
    """, data)

    db.commit()


# Сортировка объектов по этажам, отбор необходимого кол-ва объектов
def get_top_by_floors(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM building ORDER BY floors DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Расчет данных (сумма, мин, макс, среднее) по полю 'views'
def get_stat_by_views(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(views) as sum, 
            ROUND(AVG(views), 2) as avg, 
            MIN(views) as min, 
            MAX(views) as max 
        FROM building
        """)
    result = dict(res.fetchone())
    cursor.close()

    return result


# Расчет частоты встречаемости по полю 'floors'
def get_freq_by_floors(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT floors,
        COUNT(floors) as count
        FROM building
        GROUP BY floors
    """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Фильтрация объектов по условию кол-во этажей больше некоторого значения, сортировка по году,
# Отбор необходимого кол-ва объектов
def filter_by_floors(db, min_floor, limit):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM building
        WHERE floors > ?
        ORDER BY year DESC
        LIMIT ?
        """, [min_floor, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


items = load_data("task_1_var_31_item.pkl")

var = 31
limit = var + 10

db = MyModuleCS.db_connection("../first")
# insert_data(db, items)
MyModuleCS.saving(get_top_by_floors(db, limit), "task_1_sorting")
MyModuleCS.saving(get_stat_by_views(db), "task_1_stat_by_views")
MyModuleCS.saving(get_freq_by_floors(db), "task_1_freq_by_floors")
MyModuleCS.saving(filter_by_floors(db, 4, limit), "task_1_filter")

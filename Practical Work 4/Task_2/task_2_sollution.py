import csv
import MyModuleCS


def load_data(file_name):

    items = []

    with open(file_name, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file, delimiter=";")
        reader.__next__()

        for row in reader:
            if len(row) == 0:
                continue
            item = dict()
            item["name"] = row[0]
            item["rating"] = float(row[1])
            item["convenience"] = int(row[2])
            item["security"] = int(row[3])
            item["functionality"] = int(row[4])
            item["comment"] = row[5]

            items.append(item)

    return items


def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO comment (building_id, rating, convenience, security, functionality, comment_text)
        VALUES(
            (SELECT id FROM building WHERE name = :name),
            :rating, :convenience, :security, :functionality,
            :comment
        )
    """, data)

    db.commit()


# Запрос, который возвращает значения поля 'comment_text' по интересующему объекту
def first_query(db, name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT comment_text FROM comment
        WHERE building_id = (SELECT id FROM building WHERE name = ?)    
        """, [name])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    result = dict()
    result[name] = items
    return result


# Запрос, который возвращает среднее значение поля 'rating' для объектов,
# построенных позже определенного года
def second_query(db, year):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            AVG(rating) as avg_rating
        FROM comment
        WHERE building_id = (SELECT id FROM building WHERE year > ?)
        """, [year])
    result = dict(res.fetchone())
    result['after_year'] = year
    cursor.close()

    return result


# Запрос, который возвращает количество комментариев по каждому объекту
def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT building.name,
        COUNT(comment.building_id) as count
        FROM comment JOIN building
        ON comment.building_id = building.id
        GROUP BY comment.building_id
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


items = load_data("task_2_var_31_subitem.csv")

db = MyModuleCS.db_connection("../first")
# insert_data(db, items)
MyModuleCS.saving(first_query(db, 'Цирк 24'),'first_query_result')
MyModuleCS.saving(second_query(db, 2000),'second_query_result')
MyModuleCS.saving(third_query(db), 'third_query_result')

import MyModule


# Вывод первых 10 записей,
# отсортированных по убыванию по полю "salary"
def sort_by_salary(collection):

    data = (collection
            .find(limit=10)
            .sort({"salary": -1}))

    return data


# Вывод первых 15 записей,
# фильтрация по предикату "age" < 30,
# сортировка по убыванию по полю "salary"
def filter_by_age(collection):

    data = (collection
            .find({"age": {"$lt": 30}}, limit=15)
            .sort({"salary": -1}))

    return data


# Вывод первых 10 записей,
# фильтрация по сложному предикату:
# записи только из произвольного города,
# записи только из трех произвольно взятых профессий,
# сортировка по возрастанию по полю "age"
def complex_filter_by_city_and_job(collection):

    data = (collection
            .find({"city": "Варшава",
                   "job": {"$in": ["Психолог", "Учитель", "Инженер"]}}, limit=10)
            .sort({"age": 1}))

    return data


# Вывод количества записей,
# получаемых в результате фильтрации:
# "age" в произвольном диапазоне,
# "year" в [2019,2022],
# 50 000 < "salary" <= 75 000 || 125 000 < "salary" < 150 000)
def count_obj(collection):

    result = collection.count_documents({
        "age": {"$gt": 30, "$lt": 50},
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    })

    return {"count": result}


data = MyModule.get_from_file("Task_1/task_1_item.json")
MyModule.insert_many(MyModule.connect(), data)
MyModule.save_to_json("Task_1/sort_by_salary_result.json",
                      sort_by_salary(MyModule.connect()))
MyModule.save_to_json("Task_1/filter_by_age_result.json",
                      filter_by_age(MyModule.connect()))
MyModule.save_to_json("Task_1/complex_filter_by_city_and_job_result.json",
                      complex_filter_by_city_and_job(MyModule.connect()))
MyModule.save_to_json("Task_1/count_obj_result.json",
                      count_obj(MyModule.connect()))

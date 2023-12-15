import MyModule


# Удаление документов по предикату:
# "salary" < 25000 || "salary" > 175000
def delete_by_salary(collection):

    result = collection.delete_many(
        {
            "$or": [
                {"salary": {"$lt": 25000}},
                {"salary": {"$gt": 175000}},
            ]
        })

    result_dict = {
        "deleted_count": result.deleted_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "age" всех документов на 1
def update_age(collection):

    result = collection.update_many({}, {"$inc": {"age": 1}})

    result_dict = {
        "modified_count": result.modified_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "salary" на необходимый процент для произвольно выбранного поля
def increase_salary_by_column(collection, percent, column, values):

    filter = {
        f"{column}": {"$in": values}
    }

    update = {
        "$mul": {
            "salary": 1 + percent / 100
        }
    }

    result = collection.update_many(filter, update)

    result_dict = {
        "modified_count": result.modified_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "salary" на 10 % для выборки по сложного предикату
# все кроме произвольных "city", "job", произвольный диапазон "age"
def increase_salary_by_columns(collection, cities, jobs, age_gt, age_lt):
    filter = {
        "city": {"$nin": cities},
        "job": {"$nin": jobs},
        "age": {"$gt": age_gt, "$lt": age_lt}
    }

    update = {
        "$mul": {
            "salary": 1.1
        }
    }

    result = collection.update_many(filter, update)

    result_dict = {
        "modified_count": result.modified_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Удаление записей по произвольном предикату
# (по зарплате и возрасту)
def delete_by_salary_and_age(collection):
    result = collection.delete_many(
        {
            "$or": [
                {"salary": {"$lt": 25000}},
                {"salary": {"$gt": 175000}},
            ],
            "age": {"$gt": 30, "$lt": 50}
        }
    )

    result_dict = {
        "deleted_count": result.deleted_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


data = MyModule.get_from_file("Task_3/task_3_item.text")
MyModule.insert_many(MyModule.connect(), data)

MyModule.save_to_json("Task_3/delete_by_salary_result.json",
                      delete_by_salary(MyModule.connect()))

MyModule.save_to_json("Task_3/update_age_result.json",
                      update_age(MyModule.connect()))

MyModule.save_to_json("Task_3/increase_salary_by_column_1_result.json",
                      increase_salary_by_column(MyModule.connect(),
                                                5, "job",
                                                ["Психолог", "Учитель", "Инженер"]))

MyModule.save_to_json("Task_3/increase_salary_by_column_2_result.json",
                      increase_salary_by_column(MyModule.connect(),
                                                7, "city",
                                                ["Вильнюс", "Астана", "Барселона", "Москва"]))

MyModule.save_to_json("Task_3/increase_salary_by_columns_result.json",
                      increase_salary_by_columns(MyModule.connect(),
                                                 ["Вильнюс", "Астана", "Барселона", "Москва"],
                                                 ["Психолог", "Учитель", "Инженер"],
                                                 18, 25))

MyModule.save_to_json("Task_3/delete_by_salary_and_age_result.json",
                      delete_by_salary_and_age(MyModule.connect()))

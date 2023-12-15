import MyModule


# Вывод минимального, среднего, максимального значения поля "salary"
def get_stat_by_salary(collection):

    q = [
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
            }
        }
    ]

    result = collection.aggregate(q)

    return result


# Вывод количества данных по полю "job"
def get_freq_by_job(collection):
    q = [
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального, среднего, максимального значений необходимого поля
# по полю необходимому полю
def get_column_stat_by_other_column(collection, column_for_stat, column_for_grouping):

    q = [
        {
            "$group": {
                "_id": f"${column_for_grouping}",
                "max": {"$max": f"${column_for_stat}"},
                "min": {"$min": f"${column_for_stat}"},
                "avg": {"$avg": f"${column_for_stat}"}
            }
        }
    ]

    if column_for_stat == "age":
        q.append(
            {
                "$project": {
                    "_id": "$_id",
                    "max": "$max",
                    "min": "$min",
                    "avg": {"$toInt": "$avg"}
                }
            }
        )
    else:
        q.append(
            {
                "$project": {
                    "_id": "$_id",
                    "max": "$max",
                    "min": "$min",
                    "avg": {"$round": ["$avg", 2]}
                }
            }
        )

    data = collection.aggregate(q)

    return data


# Вывод максимального значения поля "salary" при минимальном "age"
def max_salary_by_min_age_match(collection):

    q = [
        {
            "$sort": {
                "age": 1,
                "salary": -1
            }
        },
        {
            "$limit": 1
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального значения поля "salary" при максимальном "age"
def min_salary_by_max_age_match(collection):

    q = [
        {
            "$sort": {
                "age": -1,
                "salary": 1
            }
        },
        {
            "$limit": 1
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального, среднего, максимального "age" по "city", где "salary" > 50000,
# сортировка по максимальному "age" в порядке убывания
def big_query_1(collection):

    q = [
        {
            "$match": {
                "salary": {"$gt": 50000}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$age"},
                "max": {"$max": "$age"},
                "avg": {"$avg": "$age"}
            }
        },
        {
            "$project": {
                "_id": "$_id",
                "max": "$max",
                "min": "$min",
                "avg": {"$toInt": "$avg"}
            }
        },
        {
            "$sort": {
                "max": -1
            }
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального, среднего, максимального "salary" по диапазонам "city", "job"
# и 18<"age"<25 || 50<"age"<65
def big_query_2(collection):

    q = [
        {
            "$match": {
                "city": {"$in": ["Вильнюс", "Астана", "Барселона", "Москва"]},
                "job": {"$in": ["Косметолог", "Врач", "Продавец", "Менеджер"]},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            }
        },
        {
            "$group": {
                "_id": "result",
                "min": {"$min": "$salary"},
                "max": {"$max": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального, среднего, максимального "salary", среднего "age",
# для "job" -> "Учитель"
# по "city",
# сортировка по "salary" в порядке убывания
def big_query_3(collection):

    q = [
        {
            "$match": {
                "job": {"$eq": "Учитель"}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "min_salary": {"$min": "$salary"},
                "max_salary": {"$max": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "avg_age": {"$avg": "$age"}
            }
        },
        {
            "$project": {
                "_id": "$_id",
                "min_salary": "$min_salary",
                "max_salary": "$max_salary",
                "avg_salary": "$avg_salary",
                "avg_age": {"$toInt": "$avg_age"}
            }
        },
        {
            "$sort": {
                "salary": -1
            }
        }
    ]

    data = collection.aggregate(q)

    return data


data = MyModule.get_from_file("Task_2/task_2_item.csv")
MyModule.insert_many(MyModule.connect(), data)
MyModule.save_to_json("Task_2/get_stat_by_salary_result.json",
                      get_stat_by_salary(MyModule.connect()))
MyModule.save_to_json("Task_2/get_freq_by_job_result.json",
                      get_freq_by_job(MyModule.connect()))
MyModule.save_to_json("Task_2/get_salary_stat_by_city_result.json",
                      get_column_stat_by_other_column(MyModule.connect(), "salary", "city"))
MyModule.save_to_json("Task_2/get_salary_stat_by_job_result.json",
                      get_column_stat_by_other_column(MyModule.connect(), "salary", "job"))
MyModule.save_to_json("Task_2/get_age_stat_by_city_result.json",
                      get_column_stat_by_other_column(MyModule.connect(), "age", "city"))
MyModule.save_to_json("Task_2/get_age_stat_by_job_result.json",
                      get_column_stat_by_other_column(MyModule.connect(), "age", "job"))
MyModule.save_to_json("Task_2/max_salary_by_min_age_match_result.json",
                      max_salary_by_min_age_match(MyModule.connect()))
MyModule.save_to_json("Task_2/min_salary_by_max_age_match_result.json",
                      min_salary_by_max_age_match(MyModule.connect()))
MyModule.save_to_json("Task_2/big_query_1_result.json",
                      big_query_1(MyModule.connect()))
MyModule.save_to_json("Task_2/big_query_2_result.json",
                      big_query_2(MyModule.connect()))
MyModule.save_to_json("Task_2/big_query_3_result.json",
                      big_query_3(MyModule.connect()))

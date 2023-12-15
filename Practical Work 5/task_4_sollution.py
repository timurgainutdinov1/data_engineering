import MyModule


# Вывод первых 5 записей,
# отсортированных по убыванию по полю "rating"
def sort_by_rating(collection):
    data = (collection
            .find(limit=5)
            .sort({"rating": -1}))

    return data


# Вывод первых 10 записей,
# фильтрация по предикату "price" <= 5,
# сортировка по убыванию по полю "year"
def filter_by_price(collection):
    data = (collection
            .find({"price": {"$lte": 5}}, limit=10)
            .sort({"year": -1}))

    return data


# Вывод первых 10 записей,
# фильтрация по сложному предикату:
# записи только c 'genre' -> 'fiction',
# записи только из 'year' -> 2008,2011,2015,
# сортировка по убыванию по полю "price"
def complex_filter_by_genre_and_year(collection):
    data = (collection
            .find({"genre": "fiction",
                   "year": {"$in": [2008, 2011, 2015]}}, limit=10)
            .sort({"price": -1}))

    return data


# Вывод количества записей,
# получаемых в результате фильтрации:
# "year" в (2000, 2010),
# "price" в [5, 10],
# 1 < "rating" <= 2 || 4 < "rating" < 5)
def count_obj(collection):
    result = collection.count_documents({
        "year": {"$gt": 2000, "$lt": 2010},
        "price": {"$gte": 5, "$lte": 10},
        "$or": [
            {"rating": {"$gt": 1, "$lte": 2}},
            {"rating": {"$gt": 4, "$lt": 5}}
        ]
    })

    return {"count": result}


# Вывод первых 3 записей,
# фильтрация по сложному предикату:
# записи только c 'author' -> "Stephen King",
# записи только c 'year' из диапазона [1980, 1990],
# сортировка по убыванию по полю "rating"
def complex_filter_by_author_and_year(collection):
    data = (collection
            .find({"author": "Stephen King",
                   "year": {"$gte": 1980, "$lte": 1990}}, limit=3)
            .sort({"rating": -1}))

    return data


MyModule.csv_to_json_pkl("Task_4/Books_Data_Clean.csv")
data = (MyModule.get_from_file("Task_4/task_4_item_part_1.json")
        + MyModule.get_from_file("Task_4/task_4_item_part_1.pkl"))

MyModule.insert_many(MyModule.connect(book=True), data)

MyModule.save_to_json("Task_4/results_1/sort_by_rating_result.json",
                      sort_by_rating(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_1/filter_by_price_result.json",
                      filter_by_price(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_1/complex_filter_by_genre_and_year_result.json",
                      complex_filter_by_genre_and_year(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_1/count_obj_result.json",
                      count_obj(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_1/complex_filter_by_author_and_year.json",
                      complex_filter_by_author_and_year(MyModule.connect(book=True)))


# Вывод минимального, среднего, максимального значения поля "rating"
def get_stat_by_rating(collection):
    q = [
        {
            "$group": {
                "_id": "rating",
                "max": {"$max": "$rating"},
                "min": {"$min": "$rating"},
                "avg": {"$avg": "$rating"},
            }
        },
        {
            "$project": {
                "_id": "$_id",
                "max": "$max",
                "min": "$min",
                "avg": {"$round": ["$avg", 2]}
            }
        }
    ]

    result = collection.aggregate(q)

    return result


# Вывод количества данных по полю "author"
def get_freq_by_author(collection):
    q = [
        {
            "$group": {
                "_id": "$author",
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
        },
        {
            "$project": {
                "_id": "$_id",
                "max": "$max",
                "min": "$min",
                "avg": {"$round": ["$avg", 2]}
            }
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод максимального значения поля "price" при минимальном "rating"
def max_price_by_min_rating_match(collection):
    q = [
        {
            "$sort": {
                "rating": 1,
                "price": -1
            }
        },
        {
            "$limit": 1
        }
    ]

    data = collection.aggregate(q)

    return data


# Вывод минимального значения поля "price" при максимальном "rating"
def min_price_by_max_rating_match(collection):
    q = [
        {
            "$sort": {
                "rating": -1,
                "price": 1
            }
        },
        {
            "$limit": 1
        }
    ]

    data = collection.aggregate(q)

    return data


MyModule.save_to_json("Task_4/results_2/get_stat_by_rating_result.json",
                      get_stat_by_rating(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_2/get_freq_by_author_result.json",
                      get_freq_by_author(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_2/get_rating_stat_by_genre.json",
                      get_column_stat_by_other_column(MyModule.connect(book=True), "rating", "genre"))
MyModule.save_to_json("Task_4/results_2/max_price_by_min_rating_match_result.json",
                      max_price_by_min_rating_match(MyModule.connect(book=True)))
MyModule.save_to_json("Task_4/results_2/min_price_by_max_rating_match_result.json",
                      min_price_by_max_rating_match(MyModule.connect(book=True)))


# Удаление документов по предикату:
# "rating" < 2.5 || "rating" > 4.5
def delete_by_rating(collection):
    result = collection.delete_many(
        {
            "$or": [
                {"rating": {"$lt": 2.5}},
                {"rating": {"$gt": 4.5}},
            ]
        })

    result_dict = {
        "deleted_count": result.deleted_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "price" всех документов на 1
def update_price(collection):
    result = collection.update_many({}, {"$inc": {"price": 1}})

    result_dict = {
        "modified_count": result.modified_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "price" на необходимый процент для произвольно выбранного поля
def increase_price_by_column(collection, percent, column, values):
    filter = {
        f"{column}": {"$in": values}
    }

    update = {
        "$mul": {
            "price": 1 + percent / 100
        }
    }

    result = collection.update_many(filter, update)

    result_dict = {
        "modified_count": result.modified_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


# Увеличение поля "price" на 10 % для выборки по сложного предикату
# не произвольные "year", производльные "genre", произвольный диапазон "rating"
def increase_price_by_columns(collection, years, genres, rating_gt, rating_lt):
    filter = {
        "year": {"$nin": years},
        "genre": {"$in": genres},
        "rating": {"$gt": rating_gt, "$lt": rating_lt}
    }

    update = {
        "$mul": {
            "price": 1.1
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
# (по рейтингу и году)
def delete_by_rating_and_year(collection):
    result = collection.delete_many(
        {
            "$or": [
                {"rating": {"$lt": 3}},
                {"rating": {"$gt": 4}},
            ],
            "year": {"$gt": 2000, "$lt": 2005}
        }
    )

    result_dict = {
        "deleted_count": result.deleted_count,
        "raw_result": result.raw_result
    }

    print(result)
    return result_dict


MyModule.save_to_json("Task_4/results_3/delete_by_rating_result.json",
                      delete_by_rating(MyModule.connect(book=True)))

MyModule.save_to_json("Task_4/results_3/update_price_result.json",
                      update_price(MyModule.connect(book=True)))

MyModule.save_to_json("Task_4/results_3/increase_price_by_column_result.json",
                      increase_price_by_column(MyModule.connect(book=True),
                                               5, "genre",
                                               ["fiction", "nonfiction"]))

MyModule.save_to_json("Task_4/results_3/increase_price_by_columns_result.json",
                      increase_price_by_columns(MyModule.connect(book=True),
                                                ["1980", "1990", "2000", "2010"],
                                                ["fiction", "genre fiction", "nonfiction"],
                                                3, 4))

MyModule.save_to_json("Task_4/results_3/delete_by_rating_and_year_result.json",
                      delete_by_rating_and_year(MyModule.connect(book=True)))

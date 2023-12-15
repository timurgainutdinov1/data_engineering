import json
import pickle
import csv
import os
import bson.json_util
from pymongo import MongoClient


def connect(book=False):
    '''
    Установка соединения с MongoDB, подключение к БД, получение коллекции
    '''
    client = MongoClient()
    db = client["test-database"]
    if not book:
        return db["person"]
    else:
        return db["book"]


def get_from_file(filename):
    '''
    Загрузка исходных данных
    '''
    basename, extension = os.path.splitext(filename)

    if extension == '.json':
        with open(filename, "r", encoding="utf-8") as f:
            items = json.load(f)
    elif extension == '.csv':
        items = []
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            reader.__next__()
            for row in reader:
                item = dict()
                item["job"] = row[0]
                item["salary"] = float(row[1])
                item["id"] = int(row[2])
                item["city"] = row[3]
                item["year"] = int(row[4])
                item["age"] = int(row[5])
                items.append(item)
    elif extension == '.pkl':
        with open(filename, "rb") as f:
            items = pickle.load(f)
    else:
        items = []
        with open(filename, "r", encoding="utf-8") as f:
            item = dict()
            while True:
                line = f.readline().strip()
                if line == '=====':
                    items.append(item)
                    item = dict()
                elif not line:
                    break
                else:
                    item[line.split('::')[0]] = line.split('::')[1]
        for item in items:
            item["salary"] = float(item["salary"])
            item["id"] = int(item["id"])
            item["year"] = int(item["year"])
            item["age"] = int(item["age"])

    return items


def insert_many(collection, data):
    '''
    Добавление записей в коллекцию
    '''
    collection.insert_many(data)


def save_to_json(filename, result):
    '''
    Сохранение данных в формат json
    '''
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(bson.json_util.dumps(result, ensure_ascii=False))


def csv_to_json_pkl(filename):
    '''
    Чтение исходных данных из csv-файла, запись в json-файл и pkl-файл
    '''
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        reader.__next__()
        for row in reader:
            item = dict()
            if row[1] != '':
                item["year"] = int(row[1].replace(".0", ""))
            else:
                continue
            item["name"] = row[2]
            item["author"] = row[3]
            item["lang"] = row[4]
            item["rating"] = float(row[6])
            item["genre"] = row[8]
            item["price"] = float(row[11])
            items.append(item)

    with open("Task_4/task_4_item_part_1.json", 'w', encoding='utf-8') as f:
        json.dump(items[:round(len(items)/2)], f, ensure_ascii=False)

    with open("Task_4/task_4_item_part_1.pkl", "wb") as f:
        pickle.dump(items[round(len(items)/2):], f)

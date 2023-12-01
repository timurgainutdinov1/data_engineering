import MyModuleCS
import pickle
import json


def load_data_pkl(file_name):
    with open(file_name, "rb") as input_file:
        items = pickle.load(input_file)

    return items


def load_data_json(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        items = json.load(f)

    return items


def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
            INSERT INTO movies_part_1 (ranking, name, year, certificate)
            VALUES(
                :ranking, :name, :year, :certificate)
            """, data)

    cursor.executemany("""
            INSERT INTO movies_part_2 (runtime_min, genre, rating, metascore)
            VALUES(
                :runtime_min, :genre, :rating, :metascore)
            """, data)

    cursor.executemany("""
            INSERT INTO movies_part_3 (info, director, actors, votes, gross_collection_mln_USD)
            VALUES(
                :info, :director, :actors, :votes, :gross_collection_mln_USD)
            """, data)

    db.commit()


movies = load_data_json("data_first.json") + load_data_pkl("data_second.pkl")
db = MyModuleCS.db_connection("../fourth")
insert_data(db, movies)

import msgpack
import MyModuleCS
import json


def load_msgpack(file_name):
    with open(file_name, 'rb') as f:
        songs_msgpack = msgpack.load(f)

    for song in songs_msgpack:
        del song['mode'], song['speechiness'], song['acousticness'], song['instrumentalness']

    return songs_msgpack


def load_json(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        songs_json = json.load(f)

    for song in songs_json:
        del song['explicit'], song['popularity'], song['danceability']

    return songs_json


# Добавление данных в таблицу в базе данных
def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre)
        VALUES(
            :artist, :song, :duration_ms,
            :year, :tempo, :genre
        )
        """, data)

    db.commit()


# Сортировка песен по полю 'duration_ms', отбор необходимого кол-ва песен
def get_top_by_duration_ms(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM music ORDER BY duration_ms DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Расчет данных (сумма, мин, макс, среднее) по полю 'duration_ms'
def get_stat_by_duration(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(duration_ms) as sum, 
            ROUND(AVG(duration_ms), 2) as avg, 
            MIN(duration_ms) as min, 
            MAX(duration_ms) as max 
        FROM music
        """)
    result = dict(res.fetchone())
    cursor.close()

    return result


# Расчет частоты встречаемости по полю 'artist'
def get_freq_by_artist(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT artist,
        COUNT(artist) as count
        FROM music
        GROUP BY artist
    """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


# Фильтрация песен полю "genre", сортировка по году,
# отбор необходимого кол-ва песен
def filter_by_genre(db, genre, limit):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM music
        WHERE genre = ?
        ORDER BY year DESC
        LIMIT ?
        """, [genre, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()

    return items


songs = load_msgpack("task_3_var_31_part_1.msgpack") + load_json("task_3_var_31_part_2.json")
db = MyModuleCS.db_connection("../second")
# insert_data(db, songs)

var = 31
first_limit = var + 10
second_limit = var + 15

MyModuleCS.saving(get_top_by_duration_ms(db, first_limit), "task_3_sorting")
MyModuleCS.saving(get_stat_by_duration(db), "task_3_stat_by_duration")
MyModuleCS.saving(get_freq_by_artist(db), "task_3_freq_by_artist")
MyModuleCS.saving(filter_by_genre(db, 'rock', second_limit), "task_3_filter")

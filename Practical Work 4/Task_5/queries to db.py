# -*- coding: utf-8 -*-
import MyModuleCS


# Отбор фильмов c рейтингом 'metascore' = 100, сортировка по году,
# вывод первых десяти фильмов
def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT movies_part_1.name, movies_part_1.year, movies_part_2.metascore
            FROM movies_part_1 JOIN movies_part_2
            ON movies_part_1.id = movies_part_2.id
            WHERE movies_part_2.metascore = 100
            ORDER BY movies_part_1.year DESC
            LIMIT 10
            """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# Вывод количества фильмов для каждого года
def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT year,
            COUNT(year) as count
            FROM movies_part_1
            GROUP BY year
            ORDER BY count
            DESC
            """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# Вывод фильмов по режисеру
def third_query(db, director):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT movies_part_1.name
            FROM movies_part_1 JOIN movies_part_3
            ON movies_part_1.id = movies_part_3.id
            WHERE movies_part_3.director = ? 
            """, [director])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    result = dict()
    result[director] = items
    return result


# Изменение числа голосов для фильма на требуемое число
def fourth_query(db, name, votes):
    cursor = db.cursor()
    res = cursor.execute("""
            UPDATE movies_part_3 SET votes = votes + ?
            WHERE id = (SELECT id FROM movies_part_1 WHERE name = ?) AND (votes + ?) > 0
            """, [votes, name, votes])
    if res.rowcount > 0:
        result = cursor.execute("""
            SELECT movies_part_1.name, 
            (movies_part_3.votes - ?) as old_votes,
            movies_part_3.votes as new_votes
            FROM movies_part_1 JOIN movies_part_3
            ON movies_part_1.id = movies_part_3.id
            WHERE movies_part_1.name = ?
            """, [votes, name])
        db.commit()
        return dict(result.fetchone())


# Расчет среднего, минимального и максимального рейтингов
def fifth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT 
            ROUND(AVG(rating), 2) as avg_rating, 
            MIN(rating) as min_rating, 
            MAX(rating) as max_rating
            FROM movies_part_2
            """)
    result = dict(res.fetchone())
    cursor.close()

    return result


# Вывод фильмов, у которых в описании (поле 'info') фигурирует 'New York City'
def sixth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT movies_part_1.name
        FROM movies_part_1 JOIN movies_part_3
        ON movies_part_1.id = movies_part_3.id
        WHERE movies_part_3.info LIKE '%New York City%'
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    result = dict()
    result['Action in New York City'] = items

    return result


db = MyModuleCS.db_connection("../fourth")

MyModuleCS.saving(first_query(db), "task_5_first_query_result")
MyModuleCS.saving(second_query(db), "task_5_second_query_result")
MyModuleCS.saving(third_query(db, 'Quentin Tarantino'), "task_5_third_query_result")
MyModuleCS.saving(fourth_query(db, 'The Godfather', 20000), "task_5_fourth_query_result")
MyModuleCS.saving(fifth_query(db), "task_5_fifth_query_result")
MyModuleCS.saving(sixth_query(db), "task_5_sixth_query_result")

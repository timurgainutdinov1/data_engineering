import sqlite3
import json


def db_connection(file_name):

    '''
    Осуществляет подключение необходимой базы данных
    '''

    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def saving(result, file_name):

    '''
    Осуществляет сохранение данных в формат json
    '''

    with open(f'{file_name}.json', 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

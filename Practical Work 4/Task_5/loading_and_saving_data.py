import csv
import json
import pickle


def load_data_set(file_name):
    items = []
    with open(file_name, "r", newline='\n', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        reader.__next__()
        for row in reader:
            item = dict()
            item['ranking'] = row[0]
            item['name'] = row[1]
            if row[2][0] == '-':
                item['year'] = int(row[2].strip('-'))
            else:
                item['year'] = int(row[2].split()[1].strip('()'))
            item['certificate'] = row[3]
            item['runtime_min'] = int(row[4].split()[0])
            item['genre'] = row[5]
            item['rating'] = float(row[6])
            if row[7] != '':
                item['metascore'] = int(row[7])
            else:
                item['metascore'] = 0
            item['info'] = row[8]
            item['director'] = row[9]
            item['actors'] = ', '.join([row[10], row[11], row[12], row[13]])
            item['votes'] = int(row[14].replace(',', ''))
            if row[15] != '':
                item['gross_collection_mln_USD'] = float(row[15].strip('$M'))
            else:
                item['gross_collection_mln_USD'] = 0
            items.append(item)
    return items


def save_data_json(result, file_name):
    with open(file_name, 'w') as output_file:
        json.dump(result, output_file, indent=4)


def save_data_pkl(result, file_name):
    with open(file_name, "wb") as output_file:
        pickle.dump(result, output_file)


movies = load_data_set("imdb (1000 movies) in june 2022.csv")
save_data_json(movies[:501], "data_first.json")
save_data_pkl(movies[501:], "data_second.pkl")

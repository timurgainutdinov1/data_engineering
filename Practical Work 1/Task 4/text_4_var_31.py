import csv

var = 31
aver_salary = 0
items = []

with open('text_4_var_31', newline='\n', encoding='utf-8') as input_file:
    reader = csv.reader(input_file, delimiter=',')
    for row in reader:
        item = {
            'number': int(row[0]),
            'name': f'{row[2]} {row[1]}',
            'age': int(row[3]),
            'salary': int(row[4].rstrip('₽$€'))
        }
        aver_salary += item['salary']
        items.append(item)

aver_salary /= len(items)

filtered = []
for item in items:
    if item['salary'] > aver_salary and item['age'] > (25 + (var % 10)):
        filtered.append(item)

filtered = sorted(filtered, key=lambda i: i['number'])

with open('text_4_var_31_result', 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file, delimiter=',')

    for item in filtered:
        writer.writerow(item.values())

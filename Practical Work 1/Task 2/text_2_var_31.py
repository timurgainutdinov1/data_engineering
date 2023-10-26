with open('text_2_var_31', 'r') as input_file:
    lines = input_file.readlines()

average_list = []

for line in lines:
    numbers_in_line = line.split('.')
    sum = 0
    for number in numbers_in_line:
        sum += int(number)
    average = sum/len(numbers_in_line)
    average_list.append(average)

with open('text_2_var_31_result', 'w') as output_file:
    for average in average_list:
        output_file.write(f'{average:.2f}\n')

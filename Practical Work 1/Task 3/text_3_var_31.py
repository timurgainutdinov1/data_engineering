with open('text_3_var_31', 'r') as input_file:
    lines = input_file.readlines()

var = 31
filter_numb = 50 + var

output_numbers = []

for line in lines:
    numbers_in_line = line.strip().split(',')
    for i in range(len(numbers_in_line)):
        if numbers_in_line[i] == 'NA':
            numbers_in_line[i] = str(int(numbers_in_line[i-1]) + int(numbers_in_line[i+1]) / 2)
    for number in numbers_in_line:
        if float(number) ** 0.5 < filter_numb:
            numbers_in_line.remove(number)

    output_numbers.append(','.join(numbers_in_line))

with open('text_3_var_31_result', 'w') as output_file:
    for line in output_numbers:
        output_file.write(line + '\n')

with open('text_1_var_31', 'r') as input_file:
    lines = input_file.readlines()

word_stat_dict = {}

for line in lines:
    row = ((line
           .replace('!', ' ')
           .replace('?', ' ')
           .replace('.', ' ')
           .replace(',', ' '))
           .strip())
    words = row.split()
    for word in words:
        if word in word_stat_dict:
            word_stat_dict[word] += 1
        else:
            word_stat_dict[word] = 1

word_stat_dict = dict(sorted(word_stat_dict.items(), reverse=True, key=lambda item: item[1]))

with open('text_1_var_31_result', 'w') as output_file:
    for key, value in word_stat_dict.items():
        output_file.write(f'{key}:{value}\n')

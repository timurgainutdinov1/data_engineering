import numpy as np
import json

matrix = np.load('matrix_31.npy')

size = len(matrix)

matrix_stat = dict()

matrix_stat['sum'] = np.sum(matrix)
matrix_stat['avr'] = np.average(matrix)
matrix_stat['sumMD'] = np.trace(matrix)
matrix_stat['avrMD'] = matrix_stat['sumMD'] / size
matrix_stat['sumSD'] = np.trace(np.fliplr(matrix))
matrix_stat['avrSD'] = matrix_stat['sumSD'] / size
matrix_stat['max'] = np.max(matrix)
matrix_stat['min'] = np.min(matrix)

for key in matrix_stat.keys():
    matrix_stat[key] = float(matrix_stat[key])

with open('matrix_31_result.json', 'w') as output_file:
    json.dump(matrix_stat, output_file, indent=4)

norm_matrix = matrix / matrix_stat['sum']

np.save('norm_matrix_31', norm_matrix)

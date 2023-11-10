import numpy as np
import os.path

var_num = 31
lim = 500 + var_num

matrix = np.load('matrix_31_2.npy')

size = len(matrix)

x = list()
y = list()
z = list()

for i in range(size):
    for j in range(size):
        if matrix[i, j] > lim:
            x.append(i)
            y.append(j)
            z.append(matrix[i, j])

np.savez('results_31', x=x, y=y, z=z)
np.savez_compressed('results_zip_31', x=x, y=y, z=z)

print(f"Size of results    : {os.path.getsize('results_31.npz')}")
print(f"Size of results_zip: {os.path.getsize('results_zip_31.npz')}")

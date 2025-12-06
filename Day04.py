import numpy as np
with open('Day3SampleInput.txt', 'r') as file:
# with open('Day3Input.txt', 'r') as file:
    data = file.read()
lines = data.strip().split('\n')
data_array = []
for line in lines:
    data_array.append([i for i in line])
np_array = np.array(data_array)

np_array[np_array == '.'] = 0
np_array[np_array == '@'] = 1
np_array = np_array.astype(int)

accessible_rolls = 0
for i in range(0, np_array.shape[0]):
    for j in range(0, np_array.shape[1]):
        if np_array[i, j] == 0:
            continue
        local_grid = np_array[max(i-1, 0): min(i+2, np_array.shape[0]),
                              max(j-1, 0): min(j+2, np_array.shape[1])]
        if (local_grid.sum() - np_array[i, j]) < 4:
            accessible_rolls += 1

print(accessible_rolls)


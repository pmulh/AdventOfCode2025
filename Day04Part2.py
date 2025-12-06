import numpy as np
# with open('Day04SampleInput.txt', 'r') as file:
with open('Day04Input.txt', 'r') as file:
    data = file.read()
lines = data.strip().split('\n')
data_array = []
for line in lines:
    data_array.append([i for i in line])
np_array = np.array(data_array)

np_array[np_array == '.'] = 0
np_array[np_array == '@'] = 1
np_array = np_array.astype(int)
original_num_rolls = np_array.sum()

def find_accessible_rolls(np_array):
    accessible_rolls = np.full((np_array.shape[0], np_array.shape[1]), False)
    for i in range(0, np_array.shape[0]):
        for j in range(0, np_array.shape[1]):
            if np_array[i, j] == 0:
                continue
            local_grid = np_array[max(i-1, 0): min(i+2, np_array.shape[0]),
                                  max(j-1, 0): min(j+2, np_array.shape[1])]
            if (local_grid.sum() - np_array[i, j]) < 4:
                accessible_rolls[i, j] = True
    return accessible_rolls

prev_num_rolls = -1
new_num_rolls = original_num_rolls
while new_num_rolls != prev_num_rolls:
    prev_num_rolls = new_num_rolls
    accessible_rolls = find_accessible_rolls(np_array)
    np_array[accessible_rolls] = 0
    new_num_rolls = np_array.sum()

print(f"{original_num_rolls:}, {new_num_rolls:}")
print(f"Rolls removed: {original_num_rolls- new_num_rolls}")




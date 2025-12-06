import numpy as np

# with open('Day2SampleInput.txt', 'r') as file:
with open('Day2Input.txt', 'r') as file:
    lines = file.readlines()
ranges = lines[0].strip(',\n').split(',')

def is_id_invalid(id):
    id = str(id)
    len_id = len(id)
    if len_id % 2 == 1:  # Odd numbered IDs can't be False
        return False
    if id[:len_id // 2] == id[len_id // 2:]:
        return True
    return False

ranges_ints = []
for id_range in ranges:
    range_start, range_end = id_range.split('-')
    range_start = int(range_start)
    range_end = int(range_end)
    if range_start > range_end:
        print(f"{range_start} is >= {range_end}")
    ranges_ints.append((range_start, range_end))

invalid_id_total = 0
for id_range in ranges_ints:
    ids = np.arange(id_range[0], id_range[1] + 1)
    for id in ids:
        if is_id_invalid(id):
            # print(id)
            invalid_id_total += id

print(invalid_id_total)
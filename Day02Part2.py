import numpy as np

# with open('Day02SampleInput.txt', 'r') as file:
with open('Day02Input.txt', 'r') as file:
    lines = file.readlines()
ranges = lines[0].strip(',\n').split(',')

def is_id_invalid(id):
    id = str(id)
    len_id = len(id)
    for pattern_length in range(1, len_id // 2 + 1):
        for starting_pos in range(0, len_id // 2):
            pattern = id[starting_pos:starting_pos + pattern_length]
            if pattern * (len_id // len(pattern)) == id:
                return True
    return False

# for id in range(2121212118,2121212124+1):
#     print(id, is_id_invalid(id))

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

# with open('Day2SampleInput.txt', 'r') as file:
with open('Day2Input.txt', 'r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

ranges = [i for i in lines if '-' in i]
ids = set([int(i) for i in lines if '-' not in i and i != ''])

num_fresh_ids = 0
for id in ids:
    for id_range in ranges:
        range_start, range_end = id_range.split('-')
        range_start = int(range_start)
        range_end = int(range_end)
        if range_start <= id <= range_end:
            num_fresh_ids += 1
            break

print(num_fresh_ids)

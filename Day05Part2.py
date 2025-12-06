from collections import deque

# with open('Day05SampleInput.txt', 'r') as file:
# with open('Day05SampleInput2.txt', 'r') as file:
with open('Day05Input.txt', 'r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

ranges = [i for i in lines if '-' in i]
ranges_ints = []

for id_range in ranges:
    range_start, range_end = id_range.split('-')
    range_start = int(range_start)
    range_end = int(range_end)
    if range_start > range_end:
        print(f"{range_start} is >= {range_end}")
    ranges_ints.append((range_start, range_end))

# Combine overlapping ranges
sorted_ranges_ints = deque(sorted(ranges_ints))
combined_range_ids = []
while len(sorted_ranges_ints) > 0:
    range_start, range_end = sorted_ranges_ints.popleft()
    while len(sorted_ranges_ints) > 0 and range_end >= sorted_ranges_ints[0][0]:
        next_range = sorted_ranges_ints.popleft()
        # Needed this to handle cases where next range is entirely within this range
        # (which led to too low a final answer)
        range_end = max(range_end, next_range[1])
    combined_range_ids.append((range_start, range_end))
    continue

total_fresh_ids = 0
for combined_range in combined_range_ids:
    range_start, range_end = combined_range
    total_fresh_ids += (range_end - range_start + 1)

print(total_fresh_ids)

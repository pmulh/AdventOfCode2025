# with open('Day08SampleInput.txt') as file:
with open('Day08Input.txt') as file:
        lines = file.readlines()
NUM_PAIRS = 1000

lines = [line.strip('\n') for line in lines]
coords = []
for line in lines:
    coords.append(tuple([int(i) for i in line.split(',')]))

def calc_distance(coord_1, coord_2):
    return ((coord_1[0] - coord_2[0]) ** 2
            + (coord_1[1] - coord_2[1]) ** 2
            + (coord_1[2] - coord_2[2]) ** 2)

def calculate_all_distances(coords):
    distances = {}
    for coord_1 in coords:
        for coord_2 in coords:
            if coord_1 == coord_2:
                continue
            distance = calc_distance(coord_1, coord_2)
            distances[tuple(sorted((coord_1, coord_2)))] = distance
    sorted_distances = sorted(distances.items(), key=lambda item: item[1])
    return sorted_distances


def find_closest_boxes(sorted_distances, ignore_list):
    for pair, distance in sorted_distances:
        return pair

distances = calculate_all_distances(coords)

circuits = {}
ignore_list = []
boxes_in_circuits = set()
box_circuit_map = {}
i = 0
while i < NUM_PAIRS:#len(ignore_list) < NUM_PAIRS:
    if i > 3:
        print(f"Iteration: {i}; lengths of top 3 circuits: "
              f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-1][1])}, "
              f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-2][1])}, "
              f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-3][1])}")
    print(len(ignore_list))
    box_a, box_b = find_closest_boxes(distances[i:], ignore_list=ignore_list)
    i += 1
    ignore_list.append(sorted((box_a, box_b)))
    boxes_in_circuits.add(box_a)
    boxes_in_circuits.add(box_b)
    new_circuit = True

    box_a_circuit_num = box_circuit_map.get(box_a)
    box_b_circuit_num = box_circuit_map.get(box_b)
    # Special handling if both boxes are already in circuits, but different circuits
    if box_a_circuit_num and box_b_circuit_num and box_a_circuit_num != box_b_circuit_num:
        # Combine the two circuits
        circuit_num = max(circuits.keys()) + 1 if circuits else 0
        circuits[circuit_num] = circuits[box_a_circuit_num].union(circuits[box_b_circuit_num])
        for box in circuits[circuit_num]:
            box_circuit_map[box] = circuit_num
        # Clear out the old circuits
        del circuits[box_a_circuit_num]
        del circuits[box_b_circuit_num]
        new_circuit = False
    elif box_a_circuit_num and box_b_circuit_num and box_a_circuit_num == box_b_circuit_num:
        # Nothing to do
        continue
    elif box_a_circuit_num:
        # Box A is already a circuit, Box B isn't; add it to the same circuit as Box A
        circuits[box_a_circuit_num].add(box_b)
        box_circuit_map[box_b] = box_a_circuit_num
        new_circuit = False
    elif box_b_circuit_num:
        # Box B is already a circuit, Box A isn't; add it to the same circuit as Box B
        circuits[box_b_circuit_num].add(box_a)
        box_circuit_map[box_a] = box_b_circuit_num
        new_circuit = False
    if new_circuit:
        circuit_num = max(circuits.keys()) + 1 if circuits else 0
        circuits[circuit_num] = set(sorted((box_a, box_b)))
        box_circuit_map[box_a] = circuit_num
        box_circuit_map[box_b] = circuit_num

print(f"Iteration: {i}; lengths of top 3 circuits: "
      f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-1][1])}, "
      f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-2][1])}, "
      f"{len(sorted(circuits.items(), key=lambda item: len(item[1]))[-3][1])}")

circuit_lengths = []
for _, circuit in circuits.items():
    circuit_lengths.append(len(circuit))
circuit_lengths = sorted(circuit_lengths)
print(circuit_lengths[-1] * circuit_lengths[-2] * circuit_lengths[-3])

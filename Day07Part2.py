from collections import Counter
import numpy as np
# with open('Day07SampleInput.txt', 'r') as file:
# with open('Day07SampleInput2.txt', 'r') as file:
with open('Day07Input.txt', 'r') as file:
    data = file.read()
lines = data.strip().split('\n')
data_array = []
for line in lines:
    data_array.append([i for i in line])
GRID = np.array(data_array)
START_POS = tuple(np.argwhere(GRID == 'S')[0])
FIRST_NODE = (2, 70)
grid_with_beams = GRID.copy()


class Beam:
    def __init__(self, previous_node_pos, start_pos):
        self.previous_node_pos = previous_node_pos
        self.start_pos = start_pos
        self.end_pos = self._calculate_end_pos()
        self.all_pos = self._calculate_beam_coverage()

    def _calculate_end_pos(self) -> tuple | None:
        for i in range(self.start_pos[0], GRID.shape[0]):
            if GRID[i, self.start_pos[1]] == '^':
                return i, self.start_pos[1]
        return None

    def _calculate_beam_coverage(self) -> list:
        positions = []
        end_position = GRID.shape[0] if self.end_pos is None else self.end_pos[0]
        for i in range(self.start_pos[0], end_position + 1):
            positions.append((i, self.start_pos[1]))
        return positions


def _can_beam_split(splitter_pos, all_beam_positions):
    for potential_new_beam_start_pos in [
        (splitter_pos[0], splitter_pos[1] - 1),
        (splitter_pos[0], splitter_pos[1] + 1)
    ]:
        if potential_new_beam_start_pos not in all_beam_positions:
            return True
    return False


def _make_new_beams(splitter_pos):
    new_beams = []
    for potential_new_beam_start_pos in [
        (splitter_pos[0], splitter_pos[1] - 1),
        (splitter_pos[0], splitter_pos[1] + 1)
    ]:
        new_beams.append(Beam(splitter_pos, potential_new_beam_start_pos))
    return new_beams


def get_children_nodes(node_pos):
    new_beams = _make_new_beams(node_pos)
    return new_beams[0].end_pos, new_beams[1].end_pos


paths_to_node_dict = Counter()
paths_to_node_dict[FIRST_NODE] = 1

initial_beam = Beam(START_POS, FIRST_NODE)
all_beams = [initial_beam]
all_beam_start_positions = [initial_beam.start_pos]
all_beam_positions = initial_beam.all_pos
inactive_splitter_positions = []
split_count = 0
splitters_in_row_positions = []
for row in range(0, GRID.shape[0]):
    if '^' not in GRID[row]:
        continue

    row_new_beams = []
    splitter_indices = np.argwhere(GRID[row] == '^')
    splitters_in_row_positions = [
        (row, int(splitter_indices[i])) for i in range(len(splitter_indices))
    ]
    for splitter_pos in splitters_in_row_positions:
        if splitter_pos not in all_beam_positions:
            continue

        new_beams = _make_new_beams(splitter_pos)
        # We're making a split; increment the split count and add a beam
        split_count += 1
        row_new_beams.extend(new_beams)
        for new_beam in new_beams:
            paths_to_node_dict[new_beam.end_pos] += paths_to_node_dict[splitter_pos]

    for new_beam in row_new_beams:
        all_beams.append(new_beam)
        all_beam_start_positions.append(new_beam.start_pos)
        all_beam_positions.extend(new_beam.all_pos)

    # for pos in all_beam_positions:
    #     if pos == START_POS:
    #         continue
    #     grid_with_beams[pos] = '|'
    #
    # for pos in all_beam_start_positions:
    #     grid_with_beams[pos] = '*'
    #
    # for pos in inactive_splitter_positions:
    #     grid_with_beams[pos] = 'X'

print(paths_to_node_dict[None])

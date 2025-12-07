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
grid_with_beams = GRID.copy()
grid_with_beam_count = np.zeros(GRID.shape)

class Beam:
    def __init__(self, start_pos):
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
        new_beams.append(Beam(potential_new_beam_start_pos))
    return new_beams


initial_beam = Beam(START_POS)
all_beams = [initial_beam]
all_beam_start_positions = [initial_beam.start_pos]
all_beam_positions = initial_beam.all_pos
inactive_splitter_positions = []
split_count = 0
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

    for new_beam in row_new_beams:
        all_beams.append(new_beam)
        all_beam_start_positions.append(new_beam.start_pos)
        all_beam_positions.extend(new_beam.all_pos)

    # FOR MAKING "VISUALS"
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

# OLD CODE FROM WHEN I DIDN'T READ THE PROBLEM PROPERLY
# active_beams = deque([START_POS])
# all_beams = []
# all_beam_start_positions = []
# all_beam_positions = []
# beam_split_count = 0
# while active_beams:#len(active_beams) > 0:
#     # active_beams = deque(sorted(active_beams))
#     beam_start_pos = active_beams.popleft()
#     # if beam_start_pos in all_beam_start_positions:
#     #     continue
#     # beam_split_count += 1
#     # all_beam_start_positions.append(beam_start_pos)
#     beam = Beam(start_pos=beam_start_pos)
#     # Don't add this beam if there's already a beam covering this path
#
#
#     all_beam_positions.extend(beam.all_pos)
#     # all_beam_start_positions.append(beam.start_pos)
#     all_beams.append(beam)
#     if beam.end_pos is None:
#         continue
#
#     beam_split_count += 1
#
#     for potential_beam_start in [(beam.end_pos[0], beam.end_pos[1] - 1),
#                                  (beam.end_pos[0], beam.end_pos[1] + 1)]:
#         active_beams.append(potential_beam_start)
#
#     # does_beam_add_split = False
#     # for potential_beam_start in [(beam.end_pos[0], beam.end_pos[1] - 1),
#     #                              (beam.end_pos[0], beam.end_pos[1] + 1)]:
#     #     if ((potential_beam_start not in all_beam_positions)):#
#     #         does_beam_add_split = True
#     #         # and (potential_beam_start not in all_beam_start_positions)):
#     #         if potential_beam_start not in all_beam_start_positions:
#     #             active_beams.append(potential_beam_start)
#     #             all_beam_start_positions.append(potential_beam_start)
#     # if does_beam_add_split:
#     #     beam_split_count += 1
#     # else:
#     #     print('hi')
#     # active_beams.append((beam.end_pos[0], beam.end_pos[1] - 1))
#     # active_beams.append((beam.end_pos[0], beam.end_pos[1] + 1))
#     # all_beams.append(beam)
    # print('hi')

print(split_count)

import numpy as np
from functools import cache

# with open('Day09SampleInput.txt', 'r') as file:
with open('Day09Input.txt', 'r') as file:
        lines = file.readlines()
lines = [line.strip() for line in lines]

# Swapping order to better match example diagrams
red_tiles = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in lines]
GRID_MIN_Y = min([i[1] for i in red_tiles]) #+ 1
GRID_MAX_Y = max([i[1] for i in red_tiles]) #+ 1
GRID_MIN_X = min([i[0] for i in red_tiles]) #+ 1
GRID_MAX_X = max([i[0] for i in red_tiles]) #+ 1

# Shift the tiles so they start at 0
red_tiles = [(tile[0] - GRID_MIN_X, tile[1] - GRID_MIN_Y) for tile in red_tiles]


def connect_red_tiles(tile_a, tile_b):
    if tile_a[0] == tile_b[0]:
        # Red tiles are in the same row
        green_tiles = [(tile_a[0], i) for i in range(min(tile_a[1], tile_b[1]) + 1,
                                                     max(tile_a[1], tile_b[1]))]
    elif tile_a[1] == tile_b[1]:
        # Red tiles are in the same column
        green_tiles = [(i, tile_a[1]) for i in range(min(tile_a[0], tile_b[0]) + 1,
                                                     max(tile_a[0], tile_b[0]))]
    else:
        print('help!')
    return green_tiles

green_tiles = []
for i in range(0, len(red_tiles) - 1):
    tile_a, tile_b = red_tiles[i], red_tiles[i+1]
    green_tiles.extend(connect_red_tiles(tile_a, tile_b))
# And then complete the loop
tile_a, tile_b = red_tiles[-1], red_tiles[0]
green_tiles.extend(connect_red_tiles(tile_a, tile_b))

def make_grid(red_tiles, green_tiles):
    grid = np.zeros([GRID_MAX_X + 2 - GRID_MIN_X, GRID_MAX_Y + 2 - GRID_MIN_Y], dtype=np.byte)
    for tile in red_tiles:
        grid[tile] = 1
    for tile in green_tiles:
        grid[tile] = 2
    return grid

global GRID
GRID_OUTLINE = make_grid(red_tiles, green_tiles)
GRID = GRID_OUTLINE.copy()#make_grid(red_tiles, green_tiles)

# @cache
def is_point_inside_polygon(coord):
    # print('hi')
    # Crossing number algorithm
    crossings = 0
    # j = coord[1] + 1
    if GRID[coord] == 1 or GRID[coord] == 2:
        return True
    if (GRID_OUTLINE[coord[0], coord[1]:].sum() // 2)% 2 == 0:
        GRID[coord] = -1
        return False
    GRID[coord] = 2
    return True


def calc_rectangle_area(a, b):
    area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
    return area

red_and_green_tiles = red_tiles + green_tiles

# internal_tiles = []
# for i in range(GRID_MIN_X, GRID_MAX_X):
#     print(f"{i} / {GRID_MAX_X}")
#     for j in range(GRID_MIN_Y, GRID_MAX_Y):
#         # print(j)
#         if is_point_inside_polygon((i,j)):#red_tiles, green_tiles):
#             internal_tiles.append((i, j))

# red_and_green_tiles.extend(internal_tiles)
red_and_green_tiles = sorted(list(set(red_and_green_tiles)))


def is_valid_rectangle(tile_a, tile_b, red_and_green_tiles):
    x0 = min(tile_a[0], tile_b[0])
    x1 = max(tile_a[0], tile_b[0])
    y0 = min(tile_a[1], tile_b[1])
    y1 = max(tile_a[1], tile_b[1])

    top_left_corner = (x0, y0)
    top_right_corner = (x0, y1)
    bottom_right_corner = (x1, y1)
    bottom_left_corner = (x1, y0)

    # Initial filter
    for coord in [top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner]:
        if not is_point_inside_polygon(coord):
            return False

    # Walk along perimeter of rectangle
    # Top
    if GRID[x0, y0: y1 + 1].min() < 0:
        return False
    if GRID[x0, y0: y1 + 1].min() < 1:
        for j in range(y0, y1):
            if (x0, j) not in red_and_green_tiles and not is_point_inside_polygon((x0, j)):
                # print('Failed on Top check')
                return False

    # Right-hand side
    if GRID[x0: x1 + 1, y1].min() < 0:
        return False
    if GRID[x0: x1 + 1, y1].min() < 1:
        for i in range(x0, x1):
            if (i, y1) not in red_and_green_tiles and not is_point_inside_polygon((i, y1)):
                # print('Failed on right-hand side check')
                return False

    # Bottom
    if GRID[x1, y0: y1 + 1].min() < 0:
        return False
    if GRID[x1, y0: y1 + 1].min() < 1:
        for j in range(y0, y1):
            if (x1, j) not in red_and_green_tiles and not is_point_inside_polygon((x1, j)):
                # print('Failed on bottom check')
                return False

    # Left-hand side
    if GRID[x0: x1 + 1, y0].min() < 0:
        return False
    if GRID[x0: x1 + 1, y0].min() < 1:
        for i in range(x0, x1):
            if (i, y0) not in red_and_green_tiles and not is_point_inside_polygon((i, y0)):
                # print('Failed on left-hand side check')
                return False

    # Start checking internal points
    # for i in range(x0, x1):
    #     for j in range(y0, y1):
    #         if not is_point_inside_polygon((i, j), grid):
    #             return False
    return True


all_rectangles = []
# print(f"{perc_grid_unmapped:2f}% grid unmapped")
for i in range(len(red_tiles)):
    coord_a = red_tiles[i]
    for j in range(i + 1, len(red_tiles)):
        coord_b = red_tiles[j]
        area = calc_rectangle_area(coord_a, coord_b)
        all_rectangles.append({'tile_a': coord_a, 'tile_b': coord_b, 'area': area})
        print(f"{i}, {j} --> {area}")

all_rectangles.sort(key=lambda d: d["area"], reverse=True)

def is_valid_rectangle_v2(tile_a: tuple, tile_b: tuple, border_tiles: list) -> bool:
    x_min = min(tile_a[0], tile_b[0])
    x_max = max(tile_a[0], tile_b[0])
    y_min = min(tile_a[1], tile_b[1])
    y_max = max(tile_a[1], tile_b[1])

    # Rectangle isn't valid if it encloses any point on the green and red tile border
    for tile in border_tiles:
        if x_min < tile[0] < x_max and y_min < tile[1] < y_max:
            return False
    return True

for i, rectangle in enumerate(all_rectangles):
    print(f"{i} / {len(all_rectangles)}")
    if is_valid_rectangle_v2(rectangle['tile_a'], rectangle['tile_b'], red_and_green_tiles):
        print(f"---> Max Area: {rectangle['area']}")
        break
    # else:
        # print(f"Rectangle {rectangle} isn't valid")
    # if is_valid_rectangle(rectangle['tile_a'], rectangle['tile_b'], red_and_green_tiles):
    #     print(f"---> Max Area: {rectangle['area']}")
    #     break

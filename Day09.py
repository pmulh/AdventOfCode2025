# with open('Day09SampleInput.txt', 'r') as file:
with open('Day09Input.txt', 'r') as file:
        lines = file.readlines()
lines = [line.strip() for line in lines]

coords = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in lines]

def calc_rectangle_area(a, b):
    area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
    return area

areas = []
for i in range(len(coords)):
    coord_a = coords[i]
    for j in range(i, len(coords)):
        coord_b = coords[j]
        area = calc_rectangle_area(coord_a, coord_b)
        areas.append(area)
        print(f"{i}, {j} --> {area}")

print(f"Max area: {max(areas)}")

import networkx as nx

# with open('Day08SampleInput.txt') as file:
with open('Day08Input.txt') as file:
        lines = file.readlines()

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
        if list(pair) in ignore_list:
            continue
        return pair

distances = calculate_all_distances(coords)

# Initialize graph
G = nx.Graph()
# Put all your nodes into graph
G.add_nodes_from(coords)
connections = []
for pair, distance in distances[:1000]:
    connections.append(pair)
# Add edges to graph
for n1, n2 in connections:
    G.add_edge(n1, n2)
# Create list of connected components of G
C = [list(c) for c in nx.connected_components(G)]

sorted_list = sorted(C, key=len, reverse=True)
print(len(sorted_list[0]) * len(sorted_list[1]) * len(sorted_list[2]))

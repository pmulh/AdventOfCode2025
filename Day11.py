# with open('Day11SampleInput.txt', 'r') as file:
with open('Day11Input.txt', 'r') as file:
        lines = file.readlines()
lines = [line.strip() for line in lines]

connections = {}
for line in lines:
    parent = line.split(':')[0]
    children = line.split(': ')[1].split(' ')
    connections[parent] = children

def rfunc(node, connections):
    count = 0
    if node == 'out':
        count += 1
    else:
        for child in connections[node]:
            count += rfunc(child, connections)
    return count

print(rfunc('you', connections))
# with open('Day01SampleInput.txt', 'r') as file:
with open('Day01Input.txt', 'r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

def rotate(current_position, action):
    if action[0] == 'L':
        new_position = (current_position - (int(action[1:])))  % 100
    else:
        new_position = (current_position + (int(action[1:])))  % 100
    return new_position

zero_counts = 0
position = 50
for line in lines:
    print(position)
    position = rotate(position, line)
    if position == 0:
        zero_counts += 1

print(f"Final Position: {position}")
print(f"Zero Counts: {zero_counts}")

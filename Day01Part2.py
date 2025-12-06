# with open('Day01SampleInput.txt', 'r') as file:
with open('Day01Input.txt', 'r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]
# lines = lines[:1000]

# lines = ['R1000']

# def rotate(current_position, action):
#     zero_passes = 0
#     if action[0] == 'L':
#         new_position = (current_position - (int(action[1:]))) % 100
#         full_rotations = int(action[1:]) // 100
#         new_position = new_position % 100
#         # print(f"----{new_position} {full_rotations} {current_position}")
#         if new_position == current_position:
#             zero_passes = full_rotations
#         elif new_position > current_position:
#             zero_passes = 1 + full_rotations
#     else:
#         # print(current_position, action)
#         new_position = (current_position + (int(action[1:]))) % 100
#         full_rotations = int(action[1:]) // 100
#         new_position = new_position % 100
#         # print(f"----{new_position} {full_rotations} {current_position}")
#         if new_position == current_position:
#             zero_passes = full_rotations
#         if new_position < current_position:
#             zero_passes = 1 + full_rotations
#     return new_position, zero_passes

def rotate(current_position, action):
    zero_passes = 0
    direction = action[0]
    turns = int(action[1:])
    full_rotations = turns // 100
    zero_passes += full_rotations
    turns = turns % 100
    if direction == 'L':
        new_position = (current_position - turns) % 100
        if current_position != 0 and new_position > current_position:
            zero_passes += 1 #+ full_rotations
        # elif new_position == current_position:
        #     zero_passes += full_rotations
        if new_position == 0:
            zero_passes += 1
    else:
        new_position = (current_position + turns) % 100
        if current_position != 0 and new_position < current_position:
            zero_passes += 1# + full_rotations
        # if new_position == 0:
        #     zero_passes += 1
        # elif new_position == current_position:
        #     zero_passes += full_rotations
    print(f"Current Position: {current_position}, Direction: {direction}, New Position: {new_position}, full rotations: {full_rotations}, Zero Passes: {zero_passes}")
    return new_position, zero_passes

    # if action[0] == 'L':
    #     new_position = (current_position - turns) % 100
    #     full_rotations = turns // 100
    #     new_position = new_position % 100
    #     # print(f"----{new_position} {full_rotations} {current_position}")
    #     if new_position == current_position:
    #         zero_passes = full_rotations
    #     elif new_position > current_position:
    #         zero_passes = 1 + full_rotations
    # else:
    #     # print(current_position, action)
    #     new_position = (current_position + (int(action[1:]))) % 100
    #     full_rotations = int(action[1:]) // 100
    #     new_position = new_position % 100
    #     # print(f"----{new_position} {full_rotations} {current_position}")
    #     if new_position == current_position:
    #         zero_passes = full_rotations
    #     if new_position < current_position:
    #         zero_passes = 1 + full_rotations
    # return new_position, zero_passes


zero_counts = 0
position = 50
for line in lines:
    position, zero_passes = rotate(position, line)
    zero_counts += zero_passes

    print(f"{line}, {position}, {zero_passes} --> total: {zero_counts}")


print(f"Final Position: {position}")
print(f"Zero Counts: {zero_counts}")

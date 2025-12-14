import numpy as np
# with open('Day10SampleInput.txt', 'r') as file:
with open('Day10Input.txt', 'r') as file:
        lines = file.readlines()

lines = [line.strip().split(' ') for line in lines]

def calculate_min_button_presses(line):
    target_input = line[0]
    joltage_input = line[-1]
    buttons_input = line[1:-1]

    target = [1 if i == '#' else 0 for i in target_input.strip('[]')]  # e.g. [0, 1, 1, 0]
    buttons = []
    for button_input in buttons_input:
        button_action = [int(i) for i in button_input.strip('()').split(',')]
        button_action = [1 if i in button_action else 0 for i in range(len(target))]
        buttons.append(button_action)

    target = np.array(target)
    buttons = np.array(buttons)
    from itertools import product
    possible_button_press_combinations = [i for i in product('01', repeat=len(buttons))]
    valid_button_press_combinations_counts = {}
    for button_press_combination in possible_button_press_combinations:
        n_presses = np.array([int(i) for i in button_press_combination])
        if np.array_equal(np.matmul(buttons.T, n_presses) % 2, target):
            valid_button_press_combinations_counts[button_press_combination] = n_presses.sum()
    min_button_presses = min(valid_button_press_combinations_counts.values())
    return min_button_presses

total_min_button_presses = 0
for line in lines:
    min_button_presses = calculate_min_button_presses(line)
    print(f"{line} --> {min_button_presses}")
    total_min_button_presses += min_button_presses

print(f"Total: {total_min_button_presses}")

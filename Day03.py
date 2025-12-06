import numpy as np

# with open('Day3SampleInput.txt', 'r') as file:
with open('Day3Input.txt', 'r') as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]

total_joltage = 0
for line in lines:
    bank_array = np.array([int(i) for i in line])
    # Largest value (but it can't be the last one)
    first_digit = bank_array[:-1].max()
    # Second digit has to be after the largest value
    second_digit = bank_array[bank_array[:-1].argmax() + 1:].max()
    print(first_digit, second_digit)
    max_joltage = int(f"{first_digit}{second_digit}")
    total_joltage += max_joltage

print(total_joltage)

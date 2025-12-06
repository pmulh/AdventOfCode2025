import numpy as np

REQUIRED_DIGITS = 12

# with open('Day03SampleInput.txt', 'r') as file:
with open('Day03Input.txt', 'r') as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]

def find_largest_useful_digit(array, start_idx, min_digits_from_end):
    array = array[start_idx:]
    if min_digits_from_end > 0:
        largest_value = array[:-min_digits_from_end].max()
        largest_value_idx = array[:-min_digits_from_end].argmax()
    else:
        largest_value = array.max()
        largest_value_idx = array.argmax()
    return largest_value, largest_value_idx + start_idx

def find_maximum_bank_joltage(bank):
    bank_array = np.array([int(i) for i in bank])

    digits = []
    remaining_digits = REQUIRED_DIGITS
    digit_i_idx = -1
    while remaining_digits > 0:
        digit_i, digit_i_idx = find_largest_useful_digit(array=bank_array,
                                                         start_idx=digit_i_idx + 1,
                                                         min_digits_from_end=remaining_digits - 1)
        digits.append(digit_i)
        remaining_digits -= 1
    max_joltage = int(''.join([str(i) for i in digits]))
    print(max_joltage)
    return max_joltage

total_joltage = 0
for line in lines:
    total_joltage += find_maximum_bank_joltage(line)

print(total_joltage)

from itertools import product
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import nnls, lsq_linear, Bounds, minimize
from sympy import Matrix, nsimplify

# with open('Day10SampleInput.txt', 'r') as file:
with open('Day10Input.txt', 'r') as file:
        lines = file.readlines()

MAX_FREE_VARIABLE_PRESSES = 100

lines = [line.strip().split(' ') for line in lines]

def calculate_min_button_presses(line):
    target_input = line[-1]
    buttons_input = line[1:-1]

    target = [int(i) for i in target_input.strip('{}').split(',')]  # e.g. [0, 1, 1, 0]
    buttons = []
    for button_input in buttons_input:
        button_action = [int(i) for i in button_input.strip('()').split(',')]
        button_action = [1 if i in button_action else 0 for i in range(len(target))]
        buttons.append(button_action)

    target = np.array(target)
    buttons = np.array(buttons)
    # print(target)

    # reg = LinearRegression(positive=True, fit_intercept=False,).fit(buttons.T, target)
    # n_presses = np.array([int(round(i, 8)) for i in reg.coef_])
    # coefs = np.array([i for i in reg.coef_])
    # print(n_presses)

    # Basically want to solve Ax = b, where A is the matrix describing what each button does,
    # b is the target vector, and x is a vector indicating how many times each button needs pressed.
    # Combine the buttons matrix and target matrix to create an augmented matrix
    augmented_matrix = np.c_[buttons.T, target]
    # Use sympy to transform into Reduced Row Echelon Form (RREF)
    # applyfunc(nsimplify) probably not needed; added when trying to bugfix
    rref, pivot_columns = Matrix(augmented_matrix).applyfunc(nsimplify).echelon_form().rref()
    # rref, pivot_columns = Matrix(buttons.T).echelon_form().rref()
    rref = np.array(rref)#.astype(int)  # Converting here to int caused issues - hard to find!
    free_variables = [i for i in range(len(buttons_input)) if i not in pivot_columns]

    # Some systems of equations will be easily solvable; others will have 1, 2 or 3 free variables
    # Hacky approach below here just has separate functions to handle each case
    def handle_zero_free_variables(free_variables, rref, target):
        n_presses = [rref[i, -1] for i in range(len(buttons_input))]
        return [n_presses]

    def handle_one_free_variable(free_variables, rref, target, max_iterations = 100):
        possible_button_press_combinations = []
        # Test out different values of the free variable
        for free_variable_a_value in range(0, max_iterations):
            n_presses = [0 for _ in range(len(buttons_input))]
            n_presses[free_variables[0]] = free_variable_a_value
            # Look at each row in RREF version of matrix, and calculate how many times each other
            # button will need pressed given this value of the free variable (because we've got
            # the matrix A into RREF, each variable is expressed in terms of the free variable).
            for row_num in range(0, rref.shape[0]):
                temp = list(rref[row_num, :])
                temp[free_variables[0]] *= free_variable_a_value
                if sum(temp) == 0:
                    continue
                pivot_column = pivot_columns[row_num]
                n_presses[pivot_column] = (
                        temp[-1] - (sum(temp[:pivot_column]) + sum(temp[pivot_column+1:-1]))
                )
                # Can't have negative button presses - if this choice of value for the free variable
                # means we need to have negative button presses, we want to move on to the next
                # iteration of the free_variable_a_value loop (so break out of this loop early,
                # and hit the if min(n_presses) < 0 check below)
                if n_presses[pivot_column] < 0:
                    break
            # Can't have negative button presses
            if min(n_presses) < 0:
                continue
            # Also can't have non-integer button presses (e.g. can't have a half-button press)
            if [int(i) for i in n_presses] != n_presses:
                continue
            # print(f"{n_presses} --> {np.matmul(buttons.T, n_presses)}")
            # Check that the number of button presses we've worked out actually satisfies the
            # Ax = b requirement
            if np.array_equal(np.matmul(buttons.T, n_presses), target):
                # print(f"FOUND ANSWER: {n_presses} ({sum(n_presses)})")
                possible_button_press_combinations.append(n_presses)
        # If we haven't found any suitable solutions by now, we're in trouble...
        if len(possible_button_press_combinations) < 1:
            print('help!')
        return possible_button_press_combinations

    def handle_two_free_variables(free_variables, rref, target, max_iterations=100):
        min_found_so_far = 9999999
        possible_button_press_combinations = []
        for free_variable_a_value in range(0, max_iterations):
            if free_variable_a_value > min_found_so_far:
                break
            for free_variable_b_value in range(0, max_iterations):
                # Some rough checks to reduce number of iterations we'll do
                if free_variable_b_value > min_found_so_far:
                    break
                if free_variable_a_value + free_variable_b_value > min_found_so_far:
                    break
                n_presses = [0 for _ in range(len(buttons_input))]
                n_presses[free_variables[0]] = free_variable_a_value
                n_presses[free_variables[1]] = free_variable_b_value
                for row_num in range(0, rref.shape[0]):#row_num = 0
                    temp = list(rref[row_num, :])
                    temp[free_variables[0]] *= free_variable_a_value
                    temp[free_variables[1]] *= free_variable_b_value
                    if sum(temp) == 0:
                        continue
                    pivot_column = pivot_columns[row_num]
                    n_presses[pivot_column] = (
                            temp[-1] - (sum(temp[:pivot_column]) + sum(temp[pivot_column+1:-1]))
                    )
                    # Can't have negative button presses
                    if n_presses[pivot_column] < 0:
                        break
                # Can't have negative button presses
                if min(n_presses) < 0:
                    continue
                # Also can't have non-integer button presses
                if [int(i) for i in n_presses] != n_presses:
                    continue
                # print(f"{n_presses} --> {np.matmul(buttons.T, n_presses)}")
                if np.array_equal(np.matmul(buttons.T, n_presses), target):
                    # print(f"FOUND ANSWER: {n_presses} ({sum(n_presses)})")
                    possible_button_press_combinations.append(n_presses)
                    min_found_so_far = min(
                        min_found_so_far, min([sum(i) for i in possible_button_press_combinations])
                    )

        if len(possible_button_press_combinations) < 1:
            print('help!')
        return possible_button_press_combinations

    def handle_three_free_variables(free_variables, rref, target, max_iterations=100):
        min_found_so_far = 9999999
        possible_button_press_combinations = []
        for free_variable_a_value in range(0, max_iterations):
            # Some rough checks to reduce number of iterations we'll do
            if free_variable_a_value > min_found_so_far:
                break
            for free_variable_b_value in range(0, max_iterations):
                if free_variable_b_value > min_found_so_far:
                    break
                for free_variable_c_value in range(0, max_iterations):
                    if free_variable_c_value > min_found_so_far:
                        break
                    if free_variable_a_value + free_variable_b_value + free_variable_c_value > min_found_so_far:
                        break
                    n_presses = [0 for _ in range(len(buttons_input))]
                    n_presses[free_variables[0]] = free_variable_a_value
                    n_presses[free_variables[1]] = free_variable_b_value
                    n_presses[free_variables[2]] = free_variable_c_value
                    for row_num in range(0, rref.shape[0]):#row_num = 0
                        temp = list(rref[row_num, :])
                        temp[free_variables[0]] *= free_variable_a_value
                        temp[free_variables[1]] *= free_variable_b_value
                        temp[free_variables[2]] *= free_variable_c_value
                        if sum(temp) == 0:
                            continue
                        pivot_column = pivot_columns[row_num]
                        n_presses[pivot_column] = (
                                temp[-1] - (sum(temp[:pivot_column]) + sum(temp[pivot_column+1:-1]))
                        )
                        # Can't have negative button presses
                        if n_presses[pivot_column] < 0:
                            break
                    # Can't have negative button presses
                    if min(n_presses) < 0:
                        continue
                    # Also can't have non-integer button presses
                    if [int(i) for i in n_presses] != n_presses:
                        continue
                    # print(f"{n_presses} --> {np.matmul(buttons.T, n_presses)}")
                    if np.array_equal(np.matmul(buttons.T, n_presses), target):
                        # print(f"FOUND ANSWER: {n_presses} ({sum(n_presses)})")
                        possible_button_press_combinations.append(n_presses)
                        min_found_so_far = min(
                            min_found_so_far, min([sum(i) for i in possible_button_press_combinations])
                        )
        if len(possible_button_press_combinations) < 1:
            print('help!')
        return possible_button_press_combinations

    if len(free_variables) == 0:
        possible_button_press_combinations = handle_zero_free_variables(free_variables, rref, target)
    elif len(free_variables) == 1:
        possible_button_press_combinations = handle_one_free_variable(free_variables, rref, target)
        if not possible_button_press_combinations:
            possible_button_press_combinations = handle_one_free_variable(
                free_variables, rref, target, max_iterations=1000
            )
    elif len(free_variables) == 2:
        possible_button_press_combinations = handle_two_free_variables(free_variables, rref, target)
        # Try with default of max_iterations = 100; if we haven't found any solutions, try again
        # with a higher value
        if not possible_button_press_combinations:
            possible_button_press_combinations = handle_two_free_variables(
                free_variables, rref, target, max_iterations=1000
            )
    elif len(free_variables) == 3:
        possible_button_press_combinations = handle_three_free_variables(free_variables, rref, target)
        # Try with default of max_iterations = 100; if we haven't found any solutions, try again
        # with a higher value
        if not possible_button_press_combinations:
            possible_button_press_combinations = handle_three_free_variables(
                free_variables, rref, target, max_iterations=1000
            )
    else:
        print(f"Can't handle {len(free_variables)} free variables")

    min_button_presses = min([sum(i) for i in possible_button_press_combinations])
    return min_button_presses


    # solution = nnls(a, b)[0]
    # coefs = nnls(buttons.T, target)[0]
    # # coefs = lsq_linear(buttons.T, target, bounds=Bounds(lb=[0 for _ in range(len(buttons))], ub=[100000 for _ in range(len(buttons))]))#['unbounded_sol'][0]
    # # coefs = np.linalg.lstsq(buttons.T, target, rcond=None)[0]
    # # print(f"{coefs}: {round(sum(coefs),0)}")
    # # return int(round(sum(coefs), 0))
    # possible_button_press_combinations_add_on = [i for i in product('012', repeat=len(buttons))]
    # possible_button_press_combinations = []
    # for add_on in possible_button_press_combinations_add_on:
    #     add_on = [int(i) - 1 for i in add_on]
    #     button_press_combo = np.clip(
    #         # np.array([coefs + add_on]),
    #         [int(i) for i in (coefs + add_on)],
    #         # np.array([max(int(round(i, 8)), 0) for i in coefs]) + add_on,
    #         a_min=0, a_max=None
    #     )
    #     # print(button_press_combo)
    #     # button_press_combo = np.array([max(int(round(i, 8)), 0) for i in n_presses]) + add_on
    #     # print(f"{np.matmul(buttons.T, button_press_combo)} <--> {target} --> {np.array_equal(np.matmul(buttons.T, button_press_combo), target)}")
    #     if np.array_equal(np.matmul(buttons.T, button_press_combo), target):
    #         # print(add_on)
    #         possible_button_press_combinations.append(button_press_combo)
    #
    # if not possible_button_press_combinations:
    #     print('no solutions found, widening search')
    #     possible_button_press_combinations_add_on = [i for i in product('01234', repeat=len(buttons))]
    #     possible_button_press_combinations = []
    #     for add_on in possible_button_press_combinations_add_on:
    #         add_on = [int(i) - 2 for i in add_on]
    #         button_press_combo = np.clip(
    #             # np.array([coefs + add_on]),
    #             [int(i) for i in (coefs + add_on)],
    #             # np.array([max(int(round(i, 8)), 0) for i in coefs]) + add_on,
    #             a_min=0, a_max=None
    #         )
    #         if np.array_equal(np.matmul(buttons.T, button_press_combo), target):
    #             possible_button_press_combinations.append(button_press_combo)
    #
    # if not possible_button_press_combinations:
    #     print('no solutions found, widening search')
    #     possible_button_press_combinations_add_on = [i for i in product('0123456', repeat=len(buttons))]
    #     possible_button_press_combinations = []
    #     for add_on in possible_button_press_combinations_add_on:
    #         add_on = [int(i) - 3 for i in add_on]
    #         button_press_combo = np.clip(
    #             # np.array([coefs + add_on]),
    #             [int(i) for i in (coefs + add_on)],
    #             # np.array([max(int(round(i, 8)), 0) for i in coefs]) + add_on,
    #             a_min=0, a_max=None
    #         )
    #         if np.array_equal(np.matmul(buttons.T, button_press_combo), target):
    #             possible_button_press_combinations.append(button_press_combo)
    #
    # if not possible_button_press_combinations:
    #     print('no solutions found, widening search')
    #     possible_button_press_combinations_add_on = [i for i in product('012345678', repeat=len(buttons))]
    #     possible_button_press_combinations = []
    #     for add_on in possible_button_press_combinations_add_on:
    #         add_on = [int(i) - 4 for i in add_on]
    #         button_press_combo = np.clip(
    #             # np.array([coefs + add_on]),
    #             [int(i) for i in (coefs + add_on)],
    #             # np.array([max(int(round(i, 8)), 0) for i in coefs]) + add_on,
    #             a_min=0, a_max=None
    #         )
    #         if np.array_equal(np.matmul(buttons.T, button_press_combo), target):
    #             possible_button_press_combinations.append(button_press_combo)
    #
    # # if not possible_button_press_combinations:
    # #     print('no solutions found, widening search')
    # #     possible_button_press_combinations_add_on = [i for i in product('012', repeat=len(buttons))]
    # #     possible_button_press_combinations = []
    # #     for add_on in possible_button_press_combinations_add_on:
    # #         add_on = [int(i) - 3 for i in add_on]
    # #         button_press_combo = np.clip(
    # #             # np.array([coefs + add_on]),
    # #             [int(i) for i in (coefs + add_on)],
    # #             # np.array([max(int(round(i, 8)), 0) for i in coefs]) + add_on,
    # #             a_min=0, a_max=None
    # #         )
    # #         # print(button_press_combo)
    # #         # button_press_combo = np.array([max(int(round(i, 8)), 0) for i in n_presses]) + add_on
    # #         # print(f"{np.matmul(buttons.T, button_press_combo)} <--> {target} --> {np.array_equal(np.matmul(buttons.T, button_press_combo), target)}")
    # #         if np.array_equal(np.matmul(buttons.T, button_press_combo), target):
    # #             # print(add_on)
    # #             possible_button_press_combinations.append(button_press_combo)
    #
    # #
    # # [i for i in product(''.join([str(i) for i in range(0, max(target) + 1)]), repeat=len(buttons))]
    # # possible_button_press_combinations = []
    # # n_presses = [int(i) for i in coefs]
    # #
    # # # possible_button_press_combinations = [i for i in product(''.join([str(i) for i in range(0, max(target) + 1)]), repeat=len(buttons))]
    # #
    # # # if not np.array_equal(np.matmul(buttons.T, n_presses), target):
    # # #     print('hi')
    # # print('hi')
    #
    # # Determine max number of button presses we need to consider by looking at max joltage in target
    # # possible_button_press_combinations = [i for i in product(''.join([str(i) for i in range(0, max(target) + 1)]), repeat=len(buttons))]
    # # valid_button_press_combinations_counts = {}
    # # for button_press_combination in possible_button_press_combinations:
    # #     n_presses = np.array([int(i) for i in button_press_combination])
    # #     if np.array_equal(np.matmul(buttons.T, n_presses), target):
    # #         valid_button_press_combinations_counts[button_press_combination] = n_presses.sum()
    # # min_button_presses = min(valid_button_press_combinations_counts.values())
    # min_button_presses = min([sum(i) for i in possible_button_press_combinations])
    # print(possible_button_press_combinations)
    # return min_button_presses
    # return 0

total_min_button_presses = 0
for line in lines:
    min_button_presses = calculate_min_button_presses(line)
    print(f"{line} --> {min_button_presses}")
    total_min_button_presses += min_button_presses

print(f"Total: {total_min_button_presses}")

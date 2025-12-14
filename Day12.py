import numpy as np
# with open('Day12SampleInput.txt', 'r') as file:  # Note - solution doesn't work for sample input!
with open('Day12Input.txt', 'r') as file:
    lines = file.readlines()

shapes = lines[:30]
regions = lines[30:]

shapes = ''.join(shapes).strip().split('\n\n')
shape_arrays = {}
for shape in shapes:
    shape_num, shape_spec = shape.split(':')
    shape_num = int(shape_num)

    shape_array = np.array([list(i) for i in shape_spec.split()])
    shape_array = np.where(shape_array == '#', 1, 0)
    shape_arrays[shape_num] = {}
    shape_arrays[shape_num]['array'] = shape_array

    shape_arrays[shape_num]['min_space_fill'] = 7
    shape_arrays[shape_num]['max_space_fill'] = 9

region_details = {}
for i in range(len(regions)):
    dimensions, num_presents = regions[i].strip().split(': ')
    width, height = dimensions.split('x')
    num_presents = [int(i) for i in num_presents.split(' ')]
    present_requirements = {}
    for j in range(len(num_presents)):
        present_requirements[j] = num_presents[j]
    region_details[i] = {'region_num': i,
                         'width': int(width),
                         'height': int(height),
                         'area': int(width) * int(height),
                         'full_presents_width': int(width) // 3,
                         'full_presents_height': int(height) // 3,
                         'num_presents': present_requirements,
                         'total_num_presents': sum(num_presents)}

def calculate_area_upper_lower_bounds(num_presents, present_shapes):
    lower_bound = 0
    upper_bound = 0
    for present_num, present_count in num_presents.items():
        # # Two of present shape 4 fit together very well; handle these separately
        # if present_num == 4:
        #     print('hi')
        #     two_present_min_space_fill = 14
        #     two_present_max_space_fill = 16
        lower_bound += present_count * present_shapes[present_num]['min_space_fill']
        upper_bound += present_count * present_shapes[present_num]['max_space_fill']
    return lower_bound, upper_bound


# def create_double_presents(num_presents, present_shapes):
#     print('hi')
#     double_present_counts = {'00': 0, '44': 0, '55': 0, '02': 0}
#     # double_present_components = {'44': [4, 4], '55': [5, 5], '02': [0, 2]}
#     for present_id in [4, 5]:
#         while num_presents[present_id] >= 2:
#             double_present_id = str(present_id) + str(present_id)
#             double_present_counts[double_present_id] += 1
#             for component in double_present_id:
#                 num_presents[int(component)] -= 1
#     present_id_pairs = [(0, 2)]
#     for present_id_pair in present_id_pairs:
#         while num_presents[present_id_pair[0]] >= 1 and num_presents[present_id_pair[1]] >= 1:
#             double_present_id = str(present_id_pair[0]) + str(present_id_pair[1])
#             double_present_counts[double_present_id] += 1
#             num_presents[present_id_pair[0]] -= 1
#             num_presents[present_id_pair[1]] -= 1


suitable_regions_count = 0
maybe_count = 0
not_suitable_region_count = 0
for region_num, region in region_details.items():
    print(f"\n--- Region: {region_num} ---")
    area_lower_bound, area_upper_bound = calculate_area_upper_lower_bounds(
        num_presents=region['num_presents'], present_shapes=shape_arrays
    )

    print(f"Area required: {area_lower_bound} --> {area_upper_bound}")
    print(f" Available area: {region['area']}")
    if area_lower_bound > region['area']:
        print(f"--> DEFINITELY NOT POSSIBLE")
        not_suitable_region_count += 1
        continue
    if (region['full_presents_width'] * region['full_presents_height']) >= region['total_num_presents']:
        suitable_regions_count += 1
        print(f"--> DEFINITELY POSSIBLE")
        continue

    # create_double_presents(region['num_presents'], shape_arrays)
    print(f"--> NOT SURE ...")
    maybe_count += 1

print('\n---------')
print(f"Possible regions: {suitable_regions_count}")
print(f"Maybe possible regions: {maybe_count}")
print(f"Not possible regions: {not_suitable_region_count}")

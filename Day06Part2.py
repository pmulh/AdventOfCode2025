import pandas as pd
import numpy as np

# input_file = 'Day06SampleInput.txt'
input_file = 'Day06Input.txt'

with open(input_file, 'r') as file:
    data = file.read()

lines = data.split('\n')
lines = [i for i in lines if i != '']
data_array = []
for line in lines[:-1]:
    data_array.append([i for i in line])
np_array = np.array(data_array)

for column in range(np_array.shape[1]):
    if all(np_array[:, column] == ' '):
        np_array[:, column] = ','
np_array[np_array == ' '] = '0'

formatted_lines = []
for row in range(np_array.shape[0]):
    formatted_lines.append(''.join(np_array[row]).split(','))
formatted_data = pd.DataFrame(formatted_lines).T

data = pd.read_csv(input_file, header=None, sep=r'\s+').T
data = data.rename(columns={len(data.columns) - 1: 'operation'})

def get_actual_numbers(str_series):
    filled_str_series = str_series.str.replace('0', ' ')
    df = pd.DataFrame(filled_str_series.apply(lambda x: list(x)).to_list()).astype(str)
    return df.astype(str).sum().astype(int)

actual_data = (formatted_data[[i for i in formatted_data.columns if i not in ['operation']]]
               .apply(get_actual_numbers, axis=1))
actual_data['operation'] = data['operation']

# actual_data has some nans because of some columns having numbers in the thousands and others
# only in the tens or hundreds. Just fill these with 0s or 1s when doing the sum or product
# as appropriate
actual_data['sum'] = actual_data[
    [i for i in actual_data.columns if i not in ['operation', 'sum', 'product']]
].fillna(0).astype(int).sum(axis=1)
actual_data['product'] = actual_data[
    [i for i in actual_data.columns if i not in ['operation', 'sum', 'product']]
].fillna(1).astype(int).product(axis=1)
actual_data['solution'] = np.where(actual_data['operation'] == '*', actual_data['product'],
                                   actual_data['sum'])

print(actual_data['solution'].sum())



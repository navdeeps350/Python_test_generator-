import os
import re
from importlib.machinery import SourceFileLoader
from instrumentor import BranchTransformer
import ast 
import inspect
from testgen_random import test_gen_1
import time
from deap_config import deap, find_key_by_element
import numpy as np
import plotly.graph_objects as go


NPOP = 300  # 300
NGEN = 200
INDMUPROB = 0.05  # 0.05
MUPROB = 0.1  # 0.1
CXPROB = 0.5  # 0.5
TOURNSIZE = 3
# LOW = -1000
# UP = 1000
REPS = 10
# MAX_STRING_LENGTH = 10


test_file_name = input('Enter the file to be injected with mutation: ')
path_original = 'benchmark/' + test_file_name
path_test = 'tests_' + test_file_name
path_deap_test = 'deap_tests_' + test_file_name
test_file_name_1 = "instrumented_" + test_file_name
path_1 = test_file_name_1

test_file_1 = SourceFileLoader(test_file_name_1, path_1).load_module()

type_list = []

test_file = SourceFileLoader(test_file_name, path_original).load_module()
# test_file_1 = SourceFileLoader(path_deap_test, path_deap_test).load_module()


function_names = [func for func in dir(test_file) if not func.startswith('__')]

b_transformer = BranchTransformer(function_names)

for func in function_names:
    globals()[func] = getattr(test_file, func)
    source = inspect.getsource(globals()[func])
    node = ast.parse(source)
    tree = b_transformer.visit(node)

for t in b_transformer.arg_type_list:
    type_list.append(t.annotation.id)



pool_size = int(input("Please enter the POOL size: "))

if len(set(type_list)) == 1:
    pool_type = type_list[0]
else:
    pool_type = 'tuple'

n = len(type_list)
if pool_type == 'int':
    MIN_VAL, MAX_VAL = input('Enter min. and max. values for the integer: ').split()
    parameters = (MIN_VAL, MAX_VAL)
elif pool_type == 'str':
    MAX_STRING_LENGTH = input('Enter max. length of the string: ')
    parameters = (MAX_STRING_LENGTH,)
elif pool_type == 'tuple':
    MAX_STRING_LENGTH, MIN_VAL, MAX_VAL = input('Enter max. length of the string and min. and max. values for the integer: ').split()
    parameters = (MAX_STRING_LENGTH, MIN_VAL, MAX_VAL)

num_exp = int(input('Enter the number of test cases you want to run: '))

o_1_list = []

for i in range(10):

    test_gen_1(test_file_name, pool_size, type_list, num_exp, *parameters)


    stream_1 = os.popen(f'mut.py --target {path_original} --unit-test {path_test}')
    output_test = stream_1.read()
    o_1 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_test).group(1)
    # print(o_1)
    o_1_list.append(o_1)


o_2_list = []


swap_dict_list, list_of_nodes = deap(n, pool_type, function_names, test_file_name, *parameters)
print(swap_dict_list)
# print(list_of_nodes)

for sdk in swap_dict_list:
    # print('sdk: ', sdk)
    f = open("deap_tests_" + test_file_name, "w")
    f.write("from unittest import TestCase\n")
    for func in function_names: 
        f.write(f"from {os.path.splitext(path_original)[0].replace('/', '.')} import {func}\n")

    f.write("\nclass Test_example(TestCase):\n")
    i = 0
    for key_tup in sdk.keys():
        # print(key_tup)
        func_set = set()
        for k in key_tup:
            o = find_key_by_element(list_of_nodes, k)
            func_set.add(o)
        for fs in func_set:
            # print(fs)
            i = i + 1
            n_o = fs[:fs.rfind('_')]
            f.write(f"\n\tdef test_{n_o}_{i}(self):\n")
            # i = i + 1
            f.write(f"\t\ty = {n_o}{tuple(sdk[key_tup])}\n")
            try:
                globals()[fs] = getattr(test_file_1, fs)
                output = globals()[fs](*tuple(sdk[key_tup]))
                if type(output) == str:
                    output = output.replace("\\", "\\\\").replace("'", "\\'")
                    f.write(f"\t\tassert y == '{output}'\n")
                else:
                    f.write(f"\t\tassert y == {output}\n")
            except BaseException:
                pass
    f.close()
    # print(path_original, path_deap_test)
    stream_2 = os.popen(f'mut.py --target {path_original} --unit-test {path_deap_test}')
    output_deap_test = stream_2.read()
    # print(output_deap_test)
    o_2 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_deap_test).group(1)
    # print(o_2)
    o_2_list.append(o_2)
    time.sleep(1)


print('o_1_list', o_1_list)
print('o_2_list', o_2_list)




o_1_values = [float(value) for value in o_1_list]
o_2_values = [float(value) for value in o_2_list]

print('Fuzzer avg. mutation score: ', np.mean(o_1_values))
print('GA avg. mutation score: ', np.mean(o_2_values))


def cohen_d(group1, group2):
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    n1, n2 = len(group1), len(group2)

    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    pooled_std = np.sqrt(pooled_var)

    effect_size = (mean1 - mean2) / pooled_std

    return effect_size


effect_size = cohen_d(o_1_values, o_2_values)
print(f"Cohen's d: {effect_size}")


fig = go.Figure()

fig.add_trace(go.Box(y=o_1_values, name='Fuzzer'))
fig.add_trace(go.Box(y=o_2_values, name='GA'))

fig.update_layout(
    title='Fuzzer vs. GA',
    xaxis=dict(title=f'{os.path.splitext(test_file_name)[0].upper()}'),
    yaxis=dict(title='Values')
    
)

# Show the plot
fig.show()

fig.write_image(f"{os.path.splitext(test_file_name)[0]}.png")


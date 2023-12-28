

import os
import re
from importlib.machinery import SourceFileLoader
from instrumentor import BranchTransformer
import ast 
import inspect
from testgen_random import test_gen

# from deap import creator, base, tools, algorithms

from deap_config import deap

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

type_list = []

test_file = SourceFileLoader(test_file_name, path_original).load_module()


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

    test_gen(test_file_name, pool_size, type_list, num_exp, *parameters)


    stream_1 = os.popen(f'mut.py --target {path_original} --unit-test {path_test}')
    output_test = stream_1.read()
    o_1 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_test).group(1)
    print(o_1)
    o_1_list.append(o_1)

print(o_1_list)


# deap(n, pool_type, function_names, *parameters)
# stream_2 = os.popen(f'mut.py --target {path_original} --unit-test {path_deap_test}')
# output_deap_test = stream_2.read()
# o_2 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_deap_test).group(1)
# print(o_2)




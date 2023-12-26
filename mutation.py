import os
import re

test_file_name = input('Enter the file to be injected with mutation: ')
path_original = 'benchmark/' + test_file_name
path_test = 'tests_' + test_file_name
path_deap_test = 'deap_tests_' + test_file_name


stream_1 = os.popen(f'mut.py --target {path_original} --unit-test {path_test}')
output_test = stream_1.read()
stream_2 = os.popen(f'mut.py --target {path_original} --unit-test {path_deap_test}')
output_deap_test = stream_2.read()

o_1 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_test).group(1)
print(o_1)

o_2 = re.search('Mutation score \[.*\]: (\d+\.\d+)\%', output_deap_test).group(1)
print(o_2)


import ast
import inspect
import sys
import random
import nltk
import random
import os

from importlib.machinery import SourceFileLoader

from _ast import Assert, Return
from typing import Any

from instrumentor import BranchTransformer, distances_true, distances_false

def get_imported_functions(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imported_functions = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_functions.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            for alias in node.names:
                imported_functions.add(f"{alias.name}")

    return imported_functions

class fuzzer_test_gen:
    def __init__(self, POOL: int):
        self.POOL = POOL

    def random_string(self, MAX_STRING_LENGTH: int):
        string_pool = []
        for p in range(self.POOL):
            l = random.randint(0, MAX_STRING_LENGTH)
            s = ""
            for i in range(l):
                random_character = chr(random.randrange(97, 122))
                s = s + random_character
            string_pool.append([s])
        return string_pool
    
    def random_string_string(self, MAX_STRING_LENGTH: int):
        string_pool = []
        for p in range(self.POOL):
            l = random.randint(0, MAX_STRING_LENGTH)
            s = ""
            k = ""
            for i in range(l):
                random_character = chr(random.randrange(97, 122))
                s = s + random_character
                random_character = chr(random.randrange(97, 122))
                k = k + random_character
            string_pool.append([s, k])
        return string_pool
    
    def random_int(self, MIN_INT: int, MAX_INT: int):
        return [[random.randint(MIN_INT, MAX_INT)] for i in range(self.POOL)]
    
    def random_int_int(self, MIN_INT: int, MAX_INT: int):
        return [[random.randint(MIN_INT, MAX_INT), random.randint(MIN_INT, MAX_INT)] for i in range(self.POOL)]
    
    def random_int_int_int(self, MIN_INT: int, MAX_INT: int):
        return [[random.randint(MIN_INT, MAX_INT), random.randint(MIN_INT, MAX_INT), random.randint(MIN_INT, MAX_INT)] for i in range(self.POOL)]
    

    def random_str_int(self, MAX_STRING_LENGTH: int, MIN_INT: int, MAX_INT: int):
        pool = []
        for p in range(self.POOL):
            l = random.randint(0, MAX_STRING_LENGTH)
            s = ""
            for i in range(l):
                random_character = chr(random.randrange(97, 122))
                s = s + random_character
            pool.append([(s, random.randint(MIN_INT, MAX_INT))])
        return pool
        
    def mutate_string(self, individuals: list):
        for string in individuals:
            for idx, _ in enumerate(string):
                chromosome = string[idx]
                mutated = chromosome[:]
                if len(mutated) > 0:
                    prob = 1.0 / len(mutated)
                    for pos in range(len(mutated)):
                        if random.random() < prob:
                            new_c = chr(random.randrange(97, 122))
                            mutated = mutated[:pos] + new_c + mutated[pos + 1:]
                    string[idx] = mutated
        return individuals
    
    def mutate_int(self, int_lists: list, *args):
        MIN_VAL, MAX_VAL = args
        mutated_list = []
        for l in int_lists:
            mutated_individual = l.copy()

            for i in range(len(mutated_individual)):
                if random.random() < 1 / len(mutated_individual):
                    mutated_individual[i] += random.randint(int(MIN_VAL), int(MAX_VAL))

            mutated_list.append(mutated_individual)
        return mutated_list
    
    
    def mutate_str_int(self, lists: list, *args):
        MAX_STRING_LENGTH, MIN_VAL, MAX_VAL = args
        str_int_list = []
        for l in lists:
            r = random.choice(l[0])
            if type(r) == str:
                chromosome = r
                mutated = chromosome[:]
                if len(mutated) > 0:
                    prob = 1.0 / len(mutated)
                    for pos in range(len(mutated)):
                        if random.random() < prob:
                            new_c = chr(random.randrange(97, 122))
                            mutated = mutated[:pos] + new_c + mutated[pos + 1:]
                    r = mutated
                    str_int_list.append([(r, l[0][1])])
                else:
                    str_int_list.append([('', l[0][1])])
            elif type(r) == int:
                mutated_individual = r
                if random.random() < 1 / len(l[0]):
                    mutated_individual += random.randint(int(MIN_VAL), int(MAX_VAL))
                r = mutated_individual
                str_int_list.append([(l[0][0], r)])
        return str_int_list
       


    def crossover_str(self, individual1: list, individual2: list):
        idx = 0
        for parent1, parent2 in zip(individual1, individual2):
            if len(parent1) > 1 and len(parent2) > 1:
                pos = random.randint(1, len(parent1))
                offspring1 = parent1[:pos] + parent2[pos:]
                offspring2 = parent2[:pos] + parent1[pos:]
                individual1[idx] = offspring1
                individual2[idx] = offspring2
                idx += 1
        return individual1, individual2
    

    def crossover_int(self, individual1: list, individual2: list):
        parent1 = individual1
        parent2 = individual2
        parent1[-1], parent2[-1] = parent2[-1], parent1[-1]
        return parent1, parent2
    
    def crossover_str_int(self, individual1: list, individual2: list):
        parent1 = individual1[0][0]
        parent2 = individual2[0][0]
        if len(parent1) > 1 and len(parent2) > 1:
            pos = random.randint(1, len(parent1))
            offspring1 = parent1[:pos] + parent2[pos:]
            offspring2 = parent2[:pos] + parent1[pos:]
        else:
            return [(parent1, individual1[0][1])], [(parent2, individual2[0][1])]
        return [(offspring1, individual1[0][1])], [(offspring2, individual2[0][1])]
    

    def test_gen(self, data_pool: list, *args):
        para = args
        test_generation = ['random initializer', 'mutation', 'crossover']
        choice = random.choice(test_generation)
        if type(data_pool[0][0]) == str:
            if choice == 'random initializer':
                test_case = random.choice(data_pool)
            elif choice == 'mutation':
                test_case = random.choice(data_pool)
                test_case = self.mutate_string([test_case])[0]
            elif choice == 'crossover':
                test_case_1 = random.choice(data_pool)
                test_case_2 = random.choice(data_pool)
                test_case = random.choice(self.crossover_str(test_case_1, test_case_2))
        elif type(data_pool[0][0]) == int:
            if choice == 'random initializer':
                test_case = random.choice(data_pool)
            elif choice == 'mutation':
                test_case = random.choice(data_pool)
                test_case = self.mutate_int([test_case], *para)[0]
            elif choice == 'crossover':
                test_case_1 = random.choice(data_pool)
                test_case_2 = random.choice(data_pool)
                test_case = random.choice(self.crossover_int(test_case_1, test_case_2))
        elif type(data_pool[0][0]) == tuple:
            if choice == 'random initializer':
                test_case = random.choice(data_pool)
            elif choice == 'mutation':
                test_case = random.choice(data_pool)
                test_case = self.mutate_str_int([test_case], *para)[0]
            elif choice == 'crossover':
                test_case_1 = random.choice(data_pool)
                test_case_2 = random.choice(data_pool)
                test_case = random.choice(self.crossover_str_int(test_case_1, test_case_2))
        return test_case
    
    def test_input(self, type_list: list, *args):
        para = args
        if len(set(type_list)) == 1:
            pool_type = type_list[0]
        else:
            pool_type = 'tuple'
        n = len(type_list)
        # print(pool_type)
        # pool_type = input("Please enter the POOL type: ")
        if pool_type == 'int':
            # MIN_VAL, MAX_VAL = input('Enter min. and max. values for the integer: ').split()
            # n = len(type_list)
            # n = int(input('Enter the number of integer inputs: '))
            if n == 1:
                test_input = self.test_gen(self.random_int(int(MIN_VAL), int(MAX_VAL)), *para)
            elif n == 2:
                test_input = self.test_gen(self.random_int_int(int(MIN_VAL), int(MAX_VAL)), *para)
            elif n == 3:
                test_input = self.test_gen(self.random_int_int_int(int(MIN_VAL), int(MAX_VAL)), *para)
        elif pool_type == 'str':
            # MAX_STRING_LENGTH = input('Enter max. length of the string: ')
            # n = len(type_list)
            # n = int(input('Enter the number of string inputs: '))
            if n == 1:
                test_input = self.test_gen(self.random_string(int(MAX_STRING_LENGTH)))
            elif n == 2: 
                test_input = self.test_gen(self.random_string_string(int(MAX_STRING_LENGTH)))
        elif pool_type == 'tuple':
            # MAX_STRING_LENGTH, MIN_VAL, MAX_VAL = input('Enter max. length of the string and min. and max. values for the integer: ').split()
            test_input = self.test_gen(self.random_str_int(int(MAX_STRING_LENGTH), int(MIN_VAL), int(MAX_VAL)), *para)[0]
        return test_input

if __name__ == '__main__':

    type_list = []

    test_file_name = input('enter the file for testing: ')
    path_original = 'benchmark/' + test_file_name
    path_instrumented = 'instrumented_' + test_file_name

    test_file = SourceFileLoader(test_file_name, path_original).load_module()

    

    function_names = [func for func in dir(test_file) if not func.startswith('__')]
    # print(function_names)

    b_transformer = BranchTransformer(function_names)

    for func in function_names:
        globals()[func] = getattr(test_file, func)
        source = inspect.getsource(globals()[func])
        node = ast.parse(source)
        tree = b_transformer.visit(node)

    for t in b_transformer.arg_type_list:
        type_list.append(t.annotation.id)

    
    # print(type_list)

    # print(b_transformer.arg_type_list)

    
    pool_size = int(input("Please enter the POOL size: "))
    # fuzz = fuzzer_test_gen(pool_size)
    # print(fuzz.test_input(type_list))

    if len(set(type_list)) == 1:
        pool_type = type_list[0]
    else:
        pool_type = 'tuple'

    # n = len(type_list)
    if pool_type == 'int':
        MIN_VAL, MAX_VAL = input('Enter min. and max. values for the integer: ').split()
        para = (MIN_VAL, MAX_VAL)
    elif pool_type == 'str':
        MAX_STRING_LENGTH = input('Enter max. length of the string: ')
        para = (MAX_STRING_LENGTH)
    elif pool_type == 'tuple':
        MAX_STRING_LENGTH, MIN_VAL, MAX_VAL = input('Enter max. length of the string and min. and max. values for the integer: ').split()
        para = (MAX_STRING_LENGTH, MIN_VAL, MAX_VAL)
    
    
    # for i in range(100):
    
    #     fuzz = fuzzer_test_gen(pool_size)
    #     print(fuzz.test_input(type_list, para))

    test_file_name_1 = "instrumented_" + test_file_name
    path_1 = test_file_name_1

    test_file_1 = SourceFileLoader(test_file_name_1, path_1).load_module()
    function_names = [func for func in dir(test_file_1) if not func.startswith('__')]
    # print(function_names)
    # print(get_imported_functions(path_1))

    num_exp = int(input('Enter the number of test cases you want to run: '))
    fuzz = fuzzer_test_gen(pool_size)
    
    dist_dict = {}
    out = {}
    prev_distances_true = {}
    # test_case = [[-5, 1], [-5, 2]]
    for func in function_names:
        if func not in get_imported_functions(path_1):
            # prev_distances_true = {}
            # out = {}
            out[func] = {}
            globals()[func] = getattr(test_file_1, func)
            for i in range(num_exp):
                test_case = fuzz.test_input(type_list, *para)
                # print(test_case)
                # test_case = [-5, 1]
                try:
                    globals()[func](*test_case)
                    # print('func: ', func)
                    # print(test_case)
                    # print(distances_true, distances_false)
                    # # print(test_case[i])
                    # print('pr_d', prev_distances_true)
                    # print('d', distances_true)
                    if len(distances_true) > len(prev_distances_true):
                        keys = set(distances_true.keys()).difference(set(prev_distances_true.keys()))
                        # print('keys: ', keys)
                        out[func][str(list(keys))] = {}
                        out[func][str(list(keys))][str(test_case)] = globals()[func](*test_case)
                        # out[str(list(keys))] = {}
                        # out[str(list(keys))][str(test_case)] = globals()[func](*test_case)
                        # print(out[str(list(keys))][str(test_case)])
                    dist_dict = [distances_true, distances_false]
                    prev_distances_true = distances_true.copy()
                except AssertionError:
                    pass
            
    print(dist_dict)
    print(out)

    function_names = [func for func in dir(test_file) if not func.startswith('__')]


    # for func in function_names:
    #     if func not in get_imported_functions(path_1):

            # globals()[func] = getattr(test_file_1, func)
            # print(globals()[func](5, 3))
    
    f = open("tests_" + test_file_name, "w")
    f.write("from unittest import TestCase\n")
    for func in function_names: 
        f.write(f"from {os.path.splitext(path_original)[0].replace('/', '.')} import {func}\n")

    f.write("\nclass Test_example(TestCase):\n")
    i = 0
    for o in out.keys():
        # print(out[o])
        for n in out[o].keys():
            i += 1
            n_o = o[:o.rfind('_')]
            # print(out[o][n])
            for k in out[o][n].keys():
                f.write(f"\tdef test_{n_o}_{i}(self):\n")
                f.write(f"\t\ty = {n_o}{tuple(ast.literal_eval(k))}\n")
                # print('k', tuple(ast.literal_eval(k)))
                if type(out[o][n][k]) == str:
                    f.write(f"\t\tassert y == \'{out[o][n][k]}\'\n")
                else:
                    f.write(f"\t\tassert y == {out[o][n][k]}\n")     
                # print(type(out[o][n][k]))     

    f.close()

import ast
import inspect
import sys
import random
import nltk
import random

from benchmark import *
from importlib.machinery import SourceFileLoader

from _ast import Assert, Return
from typing import Any




class fuzzer_test_gen:
    def __init__(self, POOL: int):
        self.POOL = POOL

    def random_string(self, MAX_STRING_LENGTH: int):
        string_pool = []
        for i in range(self.POOL):
            l = random.randint(0, MAX_STRING_LENGTH)
            s = ""
            for i in range(l):
                random_character = chr(random.randrange(97, 122))
                s = s + random_character
            string_pool.append([s])
        return string_pool
    
    def random_string_string(self, MAX_STRING_LENGTH: int):
        string_pool = []
        for i in range(self.POOL):
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
        for i in range(self.POOL):
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
    
    def mutate_int(self, int_lists: list):
        mutated_list = []
        for l in int_lists:
            mutated_individual = l.copy()

            for i in range(len(mutated_individual)):
                if random.random() < 1 / len(mutated_individual):
                    mutated_individual[i] += random.randint(-1000, 1000)

            mutated_list.append(mutated_individual)
        return mutated_list
    
    
    def mutate_str_int(self, lists: list):
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
                    mutated_individual += random.randint(-1000, 1000)
                r = mutated_individual
                str_int_list.append([(l[0][0], r)])
        return str_int_list
       


    def crossover_str(self, individual1: list, individual2: list):
        idx = 0
        for parent1, parent2 in zip(individual1, individual2):
            print(parent1)
            print(parent2)
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
    

    def fuzzer_test_gen(self, data_pool: list):
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
                test_case = self.crossover_str(test_case_1, test_case_2)
        elif type(data_pool[0][0]) == int:
            if choice == 'random initializer':
                test_case = random.choice(data_pool)
            elif choice == 'mutation':
                test_case = random.choice(data_pool)
                test_case = self.mutate_int([test_case])[0]
            elif choice == 'crossover':
                test_case_1 = random.choice(data_pool)
                test_case_2 = random.choice(data_pool)
                test_case = self.crossover_int(test_case_1, test_case_2) 
        elif type(data_pool[0][0]) == tuple:
            if choice == 'random initializer':
                test_case = random.choice(data_pool)
            elif choice == 'mutation':
                test_case = random.choice(data_pool)
                test_case = self.mutate_str_int([test_case])[0]
            elif choice == 'crossover':
                test_case_1 = random.choice(data_pool)
                test_case_2 = random.choice(data_pool)
                test_case = self.crossover_str_int(test_case_1, test_case_2)
        return test_case
        

import ast
import inspect
import sys
import random
import nltk
import random
import os

from importlib.machinery import SourceFileLoader
from nltk.metrics import distance


from _ast import Assert, Return
from typing import Any

from instrumentor import BranchTransformer, distances_true, distances_false, branches, archive_true_branches, archive_false_branches
from testgen_random import get_imported_functions

from deap import creator, base, tools, algorithms


NPOP = 300  # 300
NGEN = 200
INDMUPROB = 0.05  # 0.05
MUPROB = 0.1  # 0.1
CXPROB = 0.5  # 0.5
TOURNSIZE = 3
LOW = -1000
UP = 1000
REPS = 10
MAX_STRING_LENGTH = 10


def normalize(x):
    return x / (1.0 + x)

def get_fitness_cgi(individual:list):
    # print(individual)

    if len(set(type_list)) == 1:
        pool_type = type_list[0]
    else:
        pool_type = 'tuple'
    
    if pool_type == 'tuple':
        x = individual[0]
    else:
        x = individual
    
    global distances_true, distances_false
    global branches, archive_true_branches, archive_false_branches
    # distances_true = {}
    # distances_false = {}
    # print(distances_true, distances_false)

    # Run the function under test
    test_file_name_1 = "instrumented_" + test_file_name
    path_1 = test_file_name_1

    test_file_1 = SourceFileLoader(test_file_name_1, path_1).load_module()
    function_names = [func for func in dir(test_file_1) if not func.startswith('__')]

    for func in function_names:
        if func not in get_imported_functions(path_1):
            try:
                globals()[func] = getattr(test_file_1, func)
                globals()[func](*x)
            except BaseException:
                pass


    # Sum up branch distances
    fitness = 0.0
    for branch in branches:
        if branch in distances_true:
            if distances_true[branch] == 0 and branch not in archive_true_branches:
                archive_true_branches[branch] = x
            if branch not in archive_true_branches:
                fitness += normalize(distances_true[branch])
    for branch in branches:
        if branch in distances_false:
            if distances_false[branch] == 0 and branch not in archive_false_branches:
                archive_false_branches[branch] = x
            if branch not in archive_false_branches:
                fitness += normalize(distances_false[branch])

    return fitness,


class DeapGenetic:

    # def __init__(self, file_name: str, type_list: list):
    #     self.file_name = file_name
    #     self.type_list = type_list

    def random_integer(self):
        return random.randint(int(MIN_VAL), int(MAX_VAL))
    
    def random_string(self):
        l = random.randint(0, int(MAX_STRING_LENGTH))
        s = ""
        for i in range(l):
            random_character = chr(random.randrange(32, 127))
            s = s + random_character
        return s

    def random_str_int(self):
        l = random.randint(0, int(MAX_STRING_LENGTH))
        s = ""
        for i in range(l):
            random_character = chr(random.randrange(97, 122))
            s = s + random_character
        return (s, random.randint(int(MIN_VAL), int(MAX_VAL)))
    
    def crossover_int(self, individual1: list, individual2: list):
        parent1 = individual1
        parent2 = individual2
        parent1[-1], parent2[-1] = parent2[-1], parent1[-1]
        return parent1, parent2

    def mutate_int(self, individual: list):
        mutated_individual = individual.copy()

        for i in range(len(mutated_individual)):
            if random.random() < 1 / len(mutated_individual):
                mutated_individual[i] += random.randint(int(MIN_VAL), int(MAX_VAL))
                
        return creator.Individual(mutated_individual),
    
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


    def mutate_str(self, individuals: list):
        for idx, _ in enumerate(individuals):
            chromosome = individuals[idx]
            mutated = chromosome[:]
            if len(mutated) > 0:
                prob = 1.0 / len(mutated)
                for pos in range(len(mutated)):
                    if random.random() < prob:
                        new_c = chr(random.randrange(97, 122))
                        mutated = mutated[:pos] + new_c + mutated[pos + 1:]
                individuals[idx] = mutated
        return creator.Individual(individuals),


    def crossover_str_int(self, individual1: list, individual2: list):
        parent1 = individual1[0][0]
        parent2 = individual2[0][0]
        if len(parent1) > 1 and len(parent2) > 1:
            pos = random.randint(1, len(parent1))
            offspring1 = parent1[:pos] + parent2[pos:]
            offspring2 = parent2[:pos] + parent1[pos:]
        else:
            return creator.Individual([(parent1, individual1[0][1])]), creator.Individual([(parent2, individual2[0][1])])
        return creator.Individual([(offspring1, individual1[0][1])]), creator.Individual([(offspring2, individual2[0][1])])
    
    
    def mutate_str_int(self, lists: list):
        for l in lists:
            r = random.choice(l)
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
                    lists = [(r, l[1])]
                else:
                    lists = [('', l[1])]
            elif type(r) == int:
                mutated_individual = r
                if random.random() < 1 / len(l):
                    mutated_individual += random.randint(int(MIN_VAL), int(MAX_VAL))
                r = mutated_individual
                lists = [(l[0], r)]
        return creator.Individual(lists), 


    




if __name__ == '__main__':

    type_list = []

    test_file_name = input('enter the file for testing: ')
    path_original = 'benchmark/' + test_file_name

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

    deap = DeapGenetic()


    creator.create("Fitness", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.Fitness)
    toolbox = base.Toolbox()

    if len(set(type_list)) == 1:
        pool_type = type_list[0]
    else:
        pool_type = 'tuple'

    n = len(type_list)

    if pool_type == 'int':
        MIN_VAL, MAX_VAL = input('Enter min. and max. values for the integer: ').split()
        toolbox.register("attr_int", deap.random_integer)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=n)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", get_fitness_cgi)
        toolbox.register("mate", deap.crossover_int)
        toolbox.register("mutate", deap.mutate_int)
    elif pool_type == 'str':
        MAX_STRING_LENGTH = input('Enter max. length of the string: ')
        toolbox.register('attr_str', deap.random_string)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_str, n=n)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", get_fitness_cgi)
        toolbox.register("mate", deap.crossover_str)
        toolbox.register("mutate", deap.mutate_str)
    elif pool_type == 'tuple':
        MAX_STRING_LENGTH, MIN_VAL, MAX_VAL = input('Enter max. length of the string and min. and max. values for the integer: ').split()
        toolbox.register("attr_tuple", deap.random_str_int)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_tuple, n=n)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", get_fitness_cgi)
        toolbox.register("mate", deap.crossover_str_int)
        toolbox.register("mutate", deap.mutate_str_int)        
    
    toolbox.register("select", tools.selTournament, tournsize=TOURNSIZE)


    coverage = []
    for i in range(REPS):
        archive_true_branches = {}
        archive_false_branches = {}
        population = toolbox.population(n=NPOP)
        algorithms.eaSimple(population, toolbox, CXPROB, MUPROB, NGEN, verbose=False)
        cov = len(archive_true_branches) + len(archive_false_branches)
        print(cov, archive_true_branches, archive_false_branches)
        coverage.append(cov)

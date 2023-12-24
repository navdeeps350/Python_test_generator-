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

from instrumentor import BranchTransformer

from testgen_random import get_imported_functions

from deap import creator, base, tools, algorithms


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

distances_true: dict[int, int] = {}
distances_false: dict[int, int] = {}
branches: list[int] = [1, 2, 3, 4, 5]
archive_true_branches: dict[int, str] = {}
archive_false_branches: dict[int, str] = {}


def update_maps(condition_num, d_true, d_false):
    global distances_true, distances_false

    if condition_num in distances_true.keys():
        distances_true[condition_num] = min(
            distances_true[condition_num], d_true)
    else:
        distances_true[condition_num] = d_true

    if condition_num in distances_false.keys():
        distances_false[condition_num] = min(
            distances_false[condition_num], d_false)
    else:
        distances_false[condition_num] = d_false

def anagram_check_instrumented(s1: str, s2: str) -> bool:
    if evaluate_condition(1, 'Eq', len(s1), 1) and evaluate_condition(2, 'Eq', len(s2), 1):
        return s1 == s2
    if evaluate_condition(3, 'NotEq', len(s1), len(s2)):
        return False
    if evaluate_condition(4, 'Eq', ''.join(sorted(s1)), ''.join(sorted(s2))):
        return True
    else:
        return False
    
def decrypt_instrumented(strng: str, key: int) -> str:
    assert 0 < key <= 94
    decrypted = ''
    for x in strng:
        indx = (ord(x) - key) % 256
        if evaluate_condition(1, 'Lt', indx, 32):
            indx = indx + 95
        decrypted = decrypted + chr(indx)
    return decrypted

def encrypt_instrumented(strng: str, key: int) -> str:
    assert 0 < key <= 94
    encrypted = ''
    for x in strng:
        indx = (ord(x) + key) % 256
        if evaluate_condition(2, 'Gt', indx, 126):
            indx = indx - 95
        encrypted = encrypted + chr(indx)
    return encrypted

def check_armstrong_instrumented(n: int) -> bool:
    assert n >= 0
    if evaluate_condition(1, 'Eq', n, 0) or evaluate_condition(2, 'Eq', n, 1):
        return True
    if evaluate_condition(3, 'LtE', n, 150):
        return False
    t = n
    sum = 0
    while evaluate_condition(4, 'NotEq', t, 0):
        r = t % 10
        sum = sum + r * r * r
        t = t // 10
    if evaluate_condition(5, 'Eq', sum, n):
        return True
    else:
        return False
    
def cd_count_instrumented(a: int, b: int) -> int:
    if evaluate_condition(1, 'Eq', a, 0) or evaluate_condition(2, 'Eq', b, 0):
        return 2
    a = -1 * a if evaluate_condition(3, 'Lt', a, 0) else a
    b = -1 * b if evaluate_condition(4, 'Lt', b, 0) else b
    result = 0
    while evaluate_condition(5, 'NotEq', a, 0):
        c = a
        a = b % a
        b = c
    for i in range(1, int(b ** 0.5 + 1)):
        if evaluate_condition(6, 'Eq', b % i, 0):
            if evaluate_condition(7, 'Eq', int(b / i), i):
                result = result + 1
            else:
                result = result + 2
    return result

def exponentiation_instrumented(baseNumber: int, power: int) -> float:
    assert not (baseNumber == 0 or power <= 0)
    answer = None
    if evaluate_condition(1, 'Gt', power, 1):
        halfAnswer = exponentiation_instrumented(baseNumber, power // 2)
        answer = halfAnswer * halfAnswer
        if evaluate_condition(2, 'Eq', power % 2, 1):
            answer *= baseNumber
    elif evaluate_condition(3, 'Eq', power, 1):
        answer = baseNumber
    elif evaluate_condition(4, 'Eq', power, 0):
        answer = 1
    else:
        answer = 1 / exponentiation_instrumented(baseNumber, abs(power))
    return answer

def gcd_instrumented(a: int, b: int) -> int:
    assert a > 0 and b > 0
    if evaluate_condition(1, 'Eq', a, 1) or evaluate_condition(2, 'Eq', b, 1):
        return 1
    if evaluate_condition(3, 'Eq', a, b):
        return a
    if evaluate_condition(4, 'Gt', b, a):
        a, b = (b, a)
    while evaluate_condition(5, 'NotEq', b, 0):
        temp = b
        b = a % b
        a = temp
    return a

def longest_sorted_substr_instrumented(s: str) -> str:
    count = 0
    max_count = 0
    end_position = 0
    for char in range(len(s) - 1):
        if evaluate_condition(1, 'LtE', s[char], s[char + 1]):
            count += 1
            if evaluate_condition(2, 'Gt', count, max_count):
                max_count = count
                end_position = char + 1
        else:
            count = 0
    start_position = end_position - max_count
    return s[start_position:end_position + 1]

def rabin_karp_search_instrumented(pat: str, txt: str) -> list:
    assert len(pat) <= len(txt)
    d = 2560
    q = 101
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1
    for i in range(M - 1):
        h = h * d % q
    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q
    found_at_index = []
    for i in range(N - M + 1):
        if evaluate_condition(1, 'Eq', p, t):
            for j in range(M):
                if evaluate_condition(2, 'NotEq', txt[i + j], pat[j]):
                    break
            j += 1
            if evaluate_condition(3, 'Eq', j, M):
                found_at_index.append(i)
        if evaluate_condition(4, 'Lt', i, N - M):
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
            if evaluate_condition(5, 'Lt', t, 0):
                t = t + q
    return found_at_index

def raildecrypt_instrumented(st: str, k: int) -> str:
    assert k > 1
    c, x = (0, 0)
    m = [[0] * len(st) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = 1
        if evaluate_condition(1, 'Eq', x, 0):
            if evaluate_condition(2, 'Eq', c, k - 1):
                x = 1
                c -= 1
            else:
                c += 1
        elif evaluate_condition(3, 'Eq', c, 0):
            x = 0
            c += 1
        else:
            c -= 1
    result = []
    c, x = (0, 0)
    for i in range(k):
        for j in range(len(st)):
            if evaluate_condition(4, 'Eq', m[i][j], 1):
                m[i][j] = ord(st[x])
                x += 1
    for r in range(len(st)):
        if evaluate_condition(5, 'NotEq', m[c][r], 0):
            result.append(chr(m[c][r]))
        if evaluate_condition(6, 'Eq', x, 0):
            if evaluate_condition(7, 'Eq', c, k - 1):
                x = 1
                c -= 1
            else:
                c += 1
        elif evaluate_condition(8, 'Eq', c, 0):
            x = 0
            c += 1
        else:
            c -= 1
    return ''.join(result)

def railencrypt_instrumented(st: str, k: int) -> str:
    assert k > 1
    c = 0
    x = 0
    m = [[0] * len(st) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = ord(st[r])
        if evaluate_condition(9, 'Eq', x, 0):
            if evaluate_condition(10, 'Eq', c, k - 1):
                x = 1
                c -= 1
            else:
                c += 1
        elif evaluate_condition(11, 'Eq', c, 0):
            x = 0
            c += 1
        else:
            c -= 1
    result = []
    for i in range(k):
        for j in range(len(st)):
            if evaluate_condition(12, 'NotEq', m[i][j], 0):
                result.append(chr(m[i][j]))
    return ''.join(result)

def zeller_instrumented(d: int, m: int, y: int) -> str:
    assert abs(d) >= 1
    assert abs(m) >= 1
    assert 0 <= abs(y) <= 99 or 1000 <= abs(y) <= 3000
    d = abs(d)
    m = abs(m)
    y = abs(y)
    if evaluate_condition(1, 'Gt', d, 31):
        d = d % 31 + 1
    if evaluate_condition(2, 'Gt', m, 12):
        m = m % 12 + 1
    if evaluate_condition(3, 'Lt', y, 100) and evaluate_condition(4, 'Lt', y, 23):
        y = 2000 + y
    if evaluate_condition(5, 'Lt', y, 100) and evaluate_condition(6, 'GtE', y, 23):
        y = 1900 + y
    days = {'0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday', '6': 'Saturday'}
    if evaluate_condition(7, 'LtE', m, 2):
        y = y - 1
        m = m + 12
    c = int(str(y)[:2])
    k = int(str(y)[2:])
    t = int(2.6 * m - 5.39)
    u = int(c / 4)
    v = int(k / 4)
    x = d + k
    z = t + u + v + x
    w = z - 2 * c
    f = round(w % 7)
    for i in days:
        if evaluate_condition(8, 'Eq', f, int(i)):
            return days[i]
    

def evaluate_condition(num, op, lhs, rhs):  # type: ignore
    distance_true = 0
    distance_false = 0

    # Make sure the distance can be calculated on number and character
    # comparisons
    if (isinstance(lhs, str) and isinstance(rhs, str)) and (len(lhs) == 1 and len(rhs) == 1):
        lhs = ord(lhs)
        rhs = ord(rhs)
        print(lhs, rhs)

    if op == "Eq" and (isinstance(lhs, int)):
        if lhs == rhs:
            distance_false = 1
        else:
            distance_true = abs(lhs - rhs)

    elif op == "Lt" and (isinstance(lhs, int)):
        if lhs < rhs:
            distance_false = rhs - lhs
        else:
            distance_true = lhs - rhs + 1
    # ...
    # handle other comparison operators
    # ...
    elif op == 'Gt' and (isinstance(lhs, int)):
        if lhs > rhs:
            distance_false = lhs - rhs
        else:
            distance_true = rhs - lhs + 1 

    elif op == 'LtE' and (isinstance(lhs, int)):
        if lhs <= rhs:
            distance_false = rhs - lhs + 1
        else:
            distance_true = lhs - rhs

    elif op == 'GtE' and (isinstance(lhs, int)):
        if lhs >= rhs:
            distance_false = lhs - rhs + 1
        else:
            distance_true = rhs - lhs

    elif op == 'NotEq' and (isinstance(lhs, int)):
        if lhs == rhs:
            distance_true = 1
        else: 
            distance_false = abs(lhs - rhs)

    if (isinstance(lhs, str) and isinstance(rhs, str)) and (len(lhs) > 1 and len(rhs) > 1):

        if op == "Eq":
            if lhs == rhs:
                distance_false = 1
            else:
                distance_true = distance.edit_distance(lhs, rhs)

        elif op == 'NotEq':
            if lhs == rhs:
                distance_true = 1
            else: 
                distance_false = distance.edit_distance(lhs, rhs)


    update_maps(num, distance_true, distance_false)

    # print(num, distance_true, distance_false)

    if distance_true == 0:
        return True
    else:
        return False


def normalize(x):
        return x / (1.0 + x)

def get_fitness_cgi(individual):

    if pool_type == 'tuple':
        x = individual[0]
    else:
        x = individual
    # Reset any distance values from previous executions
    global distances_true, distances_false
    global branches, archive_true_branches, archive_false_branches
    distances_true = {}
    distances_false = {}
    # print(distances_true, distances_false)
    # Run the function under test
    
    if test_file_name == 'exponentiation.py':
        try:
            exponentiation_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'anagram_check.py':
        try: 
            anagram_check_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'caesar_cipher.py':
        try:
            decrypt_instrumented(*x)
        except BaseException:
            pass
        try: 
            encrypt_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'common_divisor_count.py':
        try:
            cd_count_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'gcd.py':
        try:
            gcd_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'longest_substring.py':
        try:
            longest_sorted_substr_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'rabin_karp.py':
        try:
            rabin_karp_search_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'check_armstrong.py':
        try:
            check_armstrong_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'railfence_cipher.py':
        try:
            raildecrypt_instrumented(*x)
        except BaseException:
            pass
        try:
            railencrypt_instrumented(*x)
        except BaseException:
            pass
    elif test_file_name == 'zellers_birthday.py':
        try:
            zeller_instrumented(*x)
        except BaseException:
            pass
    

    # Sum up branch distances
    fitness = 0.0
    for branch in branches:
        if branch in distances_true:
            if distances_true[branch] == 0 and branch not in archive_true_branches:
                archive_true_branches[branch] = x
                # print('x ', x)
                # print(archive_true_branches)
            if branch not in archive_true_branches:
                fitness += normalize(distances_true[branch])
    for branch in branches:
        if branch in distances_false:
            if distances_false[branch] == 0 and branch not in archive_false_branches:
                archive_false_branches[branch] = x
            if branch not in archive_false_branches:
                fitness += normalize(distances_false[branch])

    return fitness,


class deap_gen:

    def random_integer(self):
        return random.randint(int(MIN_VAL), int(MAX_VAL))

    def crossover_int(self, individual1: list, individual2: list):
            parent1 = individual1
            parent2 = individual2
            parent1[-1], parent2[-1] = parent2[-1], parent1[-1]
            return parent1, parent2

    def mutate_int(self, individual):
        mutated_individual = individual.copy()

        for i in range(len(mutated_individual)):
            if random.random() < 1 / len(mutated_individual):
                mutated_individual[i] += random.randint(int(MIN_VAL), int(MAX_VAL))
                
        return creator.Individual(mutated_individual),

    def random_string(self):
        l = random.randint(0, int(MAX_STRING_LENGTH))
        s = ""
        for i in range(l):
            random_character = chr(random.randrange(32, 127))
            s = s + random_character
        return s


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


    def random_str_int(self):
        l = random.randint(0, int(MAX_STRING_LENGTH))
        s = ""
        for i in range(l):
            random_character = chr(random.randrange(97, 122))
            s = s + random_character
        return (s, random.randint(int(MIN_VAL), int(MAX_VAL)))


    def crossover_str_int(self, individual1: list, individual2: list):
            # print(individual1, individual2)
            parent1 = individual1[0][0]
            parent2 = individual2[0][0]
            if len(parent1) > 1 and len(parent2) > 1:
                pos = random.randint(1, len(parent1))
                offspring1 = parent1[:pos] + parent2[pos:]
                offspring2 = parent2[:pos] + parent1[pos:]
            else:
                # print([parent1, individual1[0][1]], [parent2, individual2[0][1]])
                return creator.Individual([(parent1, individual1[0][1])]), creator.Individual([(parent2, individual2[0][1])])
            # print([offspring1, individual1[0][1]], [offspring2, individual2[0][1]])
            return creator.Individual([(offspring1, individual1[0][1])]), creator.Individual([(offspring2, individual2[0][1])])



    def mutate_str_int(self, lists: list):
        # print(lists)
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


    deap = deap_gen()

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

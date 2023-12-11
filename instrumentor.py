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


distances_true: dict[int, int] = {}
distances_false: dict[int, int] = {}
branches: list[int] = [1, 2, 3, 4, 5]
archive_true_branches: dict[int, str] = {}
archive_false_branches: dict[int, str] = {}



class BranchTransformer(ast.NodeTransformer):
    def __init__(self, function_names):
        self.arg_type_list = []
        self.function_names = function_names

    branch_num = 0

    def visit_FunctionDef(self, node):
        self.arg_type_list = node.args.args
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                if isinstance(n.value, ast.Call) and n.value.func.id in self.function_names:
                    n.value.func.id = n.value.func.id + "_instrumented"
                elif isinstance(n.value, ast.BinOp):
                     if isinstance(n.value.right, ast.Call) and n.value.right.func.id in self.function_names:
                        n.value.right.func.id = n.value.right.func.id + "_instrumented"

        node.name = node.name + "_instrumented"
        return self.generic_visit(node)
    
    def visit_Assert(self, node) :
        return node
    
    # def visit_While(self, node):
    #     return node
    
    def visit_Compare(self, node):
        if node.ops[0].__class__ in [ast.Is, ast.IsNot, ast.In, ast.NotIn]:
            return node
        self.branch_num += 1
        return ast.Call(func=ast.Name("evaluate_condition", ast.Load()),
                        args=[ast.Num(self.branch_num),
                              ast.Str(node.ops[0].__class__.__name__),
                              node.left,
                              node.comparators[0]],
                        keywords=[],
                        starargs=None,
                        kwargs=None)

    def visit_Return(self, node):
        if (isinstance(node.value, ast.Call)):
                if (isinstance(node.value.func, ast.Name)) and node.value.func.id in self.function_names:
                    node.value.func.id = node.value.func.id + "_instrumented"
        return node

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
                distance_true = nltk.metrics.distance.edit_distance(lhs, rhs)

        elif op == 'NotEq':
            if lhs == rhs:
                distance_true = 1
            else: 
                distance_false = nltk.metrics.distance.edit_distance(lhs, rhs)


    update_maps(num, distance_true, distance_false)

    print(num, distance_true, distance_false)

    if distance_true == 0:
        return True
    else:
        return False



if __name__ == '__main__':
    
    test_file_name = input('enter the file for testing: ')
    path = 'benchmark/' + test_file_name

    test_file = SourceFileLoader(test_file_name, path).load_module()

    function_names = [func for func in dir(test_file) if not func.startswith('__')]
    # print(function_names)

    b_transformer = BranchTransformer(function_names)
    # print(b_transformer.arg_type_list)

    f = open("instrumented_" + test_file_name, "w")
    f.write('from instrumentor import evaluate_condition \n\n')
    f.close()

    for func in function_names:
        globals()[func] = getattr(test_file, func)
        source = inspect.getsource(globals()[func])
        node = ast.parse(source)
        tree = b_transformer.visit(node)

        f = open("instrumented_" + test_file_name, "a")
        # print(ast.unparse(tree))
        f.write('\n\n')

        f.write(ast.unparse(tree))
    f.close()

    # print(b_transformer.arg_type_list)

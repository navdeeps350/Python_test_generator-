from instrumentor import evaluate_condition 



def gcd_instrumented(a: int, b: int) -> int:
    assert a > 0 and b > 0
    if evaluate_condition(1, 'Eq', a, 1) or evaluate_condition(2, 'Eq', b, 1):
        return 1
    if evaluate_condition(3, 'Eq', a, b):
        return a
    if evaluate_condition(4, 'Gt', b, a):
        a, b = (b, a)
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a
from instrumentor import evaluate_condition 





def cd_count_instrumented(a: int, b: int) -> int:
    if (evaluate_condition(1, 'Eq', a, 0) or evaluate_condition(2, 'Eq', b, 0)):
        return 2
    a = (((- 1) * a) if evaluate_condition(3, 'Lt', a, 0) else a)
    b = (((- 1) * b) if evaluate_condition(4, 'Lt', b, 0) else b)
    result = 0
    while evaluate_condition(5, 'NotEq', a, 0):
        c = a
        a = (b % a)
        b = c
    for i in range(1, int(((b ** 0.5) + 1))):
        if evaluate_condition(6, 'Eq', (b % i), 0):
            if evaluate_condition(7, 'Eq', int((b / i)), i):
                result = (result + 1)
            else:
                result = (result + 2)
    return result

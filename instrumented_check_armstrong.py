from instrumentor import evaluate_condition 





def check_armstrong_instrumented(n: int) -> bool:
    assert (n >= 0)
    if (evaluate_condition(1, 'Eq', n, 0) or evaluate_condition(2, 'Eq', n, 1)):
        return True
    if evaluate_condition(3, 'LtE', n, 150):
        return False
    t = n
    sum = 0
    while evaluate_condition(4, 'NotEq', t, 0):
        r = (t % 10)
        sum = (sum + ((r * r) * r))
        t = (t // 10)
    if evaluate_condition(5, 'Eq', sum, n):
        return True
    else:
        return False

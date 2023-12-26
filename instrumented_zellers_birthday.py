from instrumentor import evaluate_condition 





def zeller_instrumented(d: int, m: int, y: int) -> str:
    assert (abs(d) >= 1)
    assert (abs(m) >= 1)
    assert ((0 <= abs(y) <= 99) or (1000 <= abs(y) <= 3000))
    d = abs(d)
    m = abs(m)
    y = abs(y)
    if evaluate_condition(1, 'Gt', d, 31):
        d = ((d % 31) + 1)
    if evaluate_condition(2, 'Gt', m, 12):
        m = ((m % 12) + 1)
    if (evaluate_condition(3, 'Lt', y, 100) and evaluate_condition(4, 'Lt', y, 23)):
        y = (2000 + y)
    if (evaluate_condition(5, 'Lt', y, 100) and evaluate_condition(6, 'GtE', y, 23)):
        y = (1900 + y)
    days = {'0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday', '6': 'Saturday'}
    if evaluate_condition(7, 'LtE', m, 2):
        y = (y - 1)
        m = (m + 12)
    c = int(str(y)[:2])
    k = int(str(y)[2:])
    t = int(((2.6 * m) - 5.39))
    u = int((c / 4))
    v = int((k / 4))
    x = (d + k)
    z = (((t + u) + v) + x)
    w = (z - (2 * c))
    f = round((w % 7))
    for i in days:
        if evaluate_condition(8, 'Eq', f, int(i)):
            return days[i]

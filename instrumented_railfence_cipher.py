from instrumentor import evaluate_condition 





def raildecrypt_instrumented(st: str, k: int) -> str:
    assert (k > 1)
    (c, x) = (0, 0)
    m = [([0] * len(st)) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = 1
        if evaluate_condition(1, 'Eq', x, 0):
            if evaluate_condition(2, 'Eq', c, (k - 1)):
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
    (c, x) = (0, 0)
    for i in range(k):
        for j in range(len(st)):
            if evaluate_condition(4, 'Eq', m[i][j], 1):
                m[i][j] = ord(st[x])
                x += 1
    for r in range(len(st)):
        if evaluate_condition(5, 'NotEq', m[c][r], 0):
            result.append(chr(m[c][r]))
        if evaluate_condition(6, 'Eq', x, 0):
            if evaluate_condition(7, 'Eq', c, (k - 1)):
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
    assert (k > 1)
    c = 0
    x = 0
    m = [([0] * len(st)) for i in range(k)]
    for r in range(len(st)):
        m[c][r] = ord(st[r])
        if evaluate_condition(9, 'Eq', x, 0):
            if evaluate_condition(10, 'Eq', c, (k - 1)):
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

from instrumentor import evaluate_condition 



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
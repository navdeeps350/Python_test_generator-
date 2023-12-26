from instrumentor import evaluate_condition 





def anagram_check_instrumented(s1: str, s2: str) -> bool:
    if (evaluate_condition(1, 'Eq', len(s1), 1) and evaluate_condition(2, 'Eq', len(s2), 1)):
        return (s1 == s2)
    if evaluate_condition(3, 'NotEq', len(s1), len(s2)):
        return False
    if evaluate_condition(4, 'Eq', ''.join(sorted(s1)), ''.join(sorted(s2))):
        return True
    else:
        return False

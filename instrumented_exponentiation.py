from instrumentor import evaluate_condition 



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
from instrumentor import evaluate_condition 



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
from scipy.stats import wilcoxon


# Fuzzer avg. mutation score:  26.18
# GA avg. mutation score:  16.94
# Cohen's d: 1.6099689437998483

o_1_anagram_check = ['38.5', '23.1', '38.5', '23.1', '23.1', '23.1', '23.1', '23.1', '23.1', '23.1']
o_2_anagram_check = ['15.4', '15.4', '15.4', '15.4', '15.4', '15.4', '15.4', '15.4', '30.8', '15.4']

o_1_anagram_check = [float(value) for value in o_1_anagram_check]
o_2_anagram_check = [float(value) for value in o_2_anagram_check]


statistic_anagram_check, p_value_anagram_check = wilcoxon(o_1_anagram_check, o_2_anagram_check, alternative='two-sided')
print(p_value_anagram_check)

# Fuzzer avg. mutation score:  54.39
# GA avg. mutation score:  54.410000000000004
# Cohen's d: -0.004615807978136065

o_1_list_caesar_cipher = ['58.8', '52.9', '52.9', '52.9', '52.9', '52.9', '50.0', '55.9', '50.0', '64.7']
o_2_list_caesar_cipher = ['61.8', '50.0', '52.9', '55.9', '58.8', '55.9', '52.9', '55.9', '47.1', '52.9']

o_1_list_caesar_cipher = [float(value) for value in o_1_list_caesar_cipher]
o_2_list_caesar_cipher = [float(value) for value in o_2_list_caesar_cipher]


statistic_caesar_cipher, p_value_caesar_cipher = wilcoxon(o_1_list_caesar_cipher, o_2_list_caesar_cipher, alternative='two-sided')
print(p_value_caesar_cipher)

# Fuzzer avg. mutation score:  22.6
# GA avg. mutation score:  24.21
# Cohen's d: -0.44721359549995776

o_1_list_armstrong = ['22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6']
o_2_list_armstrong =  ['38.7', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6', '22.6']

o_1_list_armstrong = [float(value) for value in o_1_list_armstrong]
o_2_list_armstrong = [float(value) for value in o_2_list_armstrong]


statistic_armstrong, p_value_armstrong = wilcoxon(o_1_list_armstrong, o_2_list_armstrong, alternative='two-sided')
print(p_value_armstrong)

# Fuzzer avg. mutation score:  40.87
# GA avg. mutation score:  42.370000000000005
# Cohen's d: -0.5566553597290542

o_1_list_common_divisor_count = ['40.4', '42.6', '38.3', '31.9', '42.6', '42.6', '42.6', '42.6', '40.4', '44.7']
o_2_list_common_divisor_count =  ['40.4', '42.6', '42.6', '40.4', '42.6', '42.6', '42.6', '44.7', '42.6', '42.6']

o_1_list_common_divisor_count = [float(value) for value in o_1_list_common_divisor_count]
o_2_list_common_divisor_count = [float(value) for value in o_2_list_common_divisor_count]


statistic_common_divisor_count, p_value_common_divisor_count = wilcoxon(o_1_list_common_divisor_count, o_2_list_common_divisor_count, alternative='two-sided')
print(p_value_common_divisor_count)


# Fuzzer avg. mutation score:  61.14
# GA avg. mutation score:  62.29
# Cohen's d: -0.09612054803526891

o_1_list_exponentiation =  ['48.6', '65.7', '40.0', '71.4', '65.7', '68.6', '71.4', '40.0', '68.6', '71.4']
o_2_list_exponentiation = ['54.3', '71.4', '54.3', '71.4', '54.3', '71.4', '68.6', '68.6', '40.0', '68.6']

o_1_list_exponentiation = [float(value) for value in o_1_list_exponentiation]
o_2_list_exponentiation = [float(value) for value in o_2_list_exponentiation]


statistic_exponentiation, p_value_exponentiation = wilcoxon(o_1_list_exponentiation, o_2_list_exponentiation, alternative='two-sided')
print(p_value_exponentiation)


# Fuzzer avg. mutation score:  37.839999999999996
# GA avg. mutation score:  42.62
# Cohen's d: -0.6904452021350683

o_1_list_gcd = ['34.8', '34.8', '47.8', '34.8', '34.8', '43.5', '43.5', '34.8', '34.8', '34.8']
o_2_list_gcd = ['52.2', '34.8', '34.8', '34.8', '34.8', '47.8', '47.8', '52.2', '52.2', '34.8']

o_1_list_gcd = [float(value) for value in o_1_list_gcd]
o_2_list_gcd = [float(value) for value in o_2_list_gcd]


statistic_gcd, p_value_gcd = wilcoxon(o_1_list_gcd, o_2_list_gcd, alternative='two-sided')
print(p_value_gcd)

# Fuzzer avg. mutation score:  77.84
# GA avg. mutation score:  80.44999999999999
# Cohen's d: -0.5267451058490136

o_1_list_longest_substring = ['73.9', '78.3', '78.3', '82.6', '73.9', '78.3', '78.3', '82.6', '82.6', '69.6']
o_2_list_longest_substring = ['78.3', '78.3', '82.6', '82.6', '87.0', '69.6', '82.6', '82.6', '73.9', '87.0']

o_1_list_longest_substring = [float(value) for value in o_1_list_longest_substring]
o_2_list_longest_substring = [float(value) for value in o_2_list_longest_substring]


statistic_longest_substring, p_value_longest_substring = wilcoxon(o_1_list_longest_substring, o_2_list_longest_substring, alternative='two-sided')
print(p_value_longest_substring)

# Fuzzer avg. mutation score:  24.73
# GA avg. mutation score:  59.96999999999999
# Cohen's d: -12.245021361953873

o_1_list_rabin_karp = ['26.3', '22.8', '26.3', '26.3', '28.1', '19.3', '26.3', '22.8', '26.3', '22.8']
o_2_list_rabin_karp = ['59.6', '59.6', '59.6', '57.9', '57.9', '57.9', '59.6', '59.6', '59.6', '68.4']

o_1_list_rabin_karp = [float(value) for value in o_1_list_rabin_karp]
o_2_list_rabin_karp = [float(value) for value in o_2_list_rabin_karp]


statistic_rabin_karp, p_value_rabin_karp = wilcoxon(o_1_list_rabin_karp, o_2_list_rabin_karp, alternative='two-sided')
print(p_value_rabin_karp)


# Fuzzer avg. mutation score:  80.96
# GA avg. mutation score:  54.239999999999995
# Cohen's d: 4.663113932207819

o_1_list_railfence_cipher = ['89.4', '86.2', '85.1', '79.8', '79.8', '68.1', '85.1', '72.3', '84.0', '79.8']
o_2_list_railfence_cipher = ['57.4', '55.3', '54.3', '58.5', '54.3', '55.3', '45.7', '45.7', '57.4', '58.5']

o_1_list_railfence_cipher = [float(value) for value in o_1_list_railfence_cipher]
o_2_list_railfence_cipher = [float(value) for value in o_2_list_railfence_cipher]


statistic_railfence_cipher, p_value_railfence_cipher = wilcoxon(o_1_list_railfence_cipher, o_2_list_railfence_cipher, alternative='two-sided')
print(p_value_railfence_cipher)

# Fuzzer avg. mutation score:  42.84
# GA avg. mutation score:  55.65
# Cohen's d: -3.030171973073049

o_1_list_zeller = ['44.2', '40.0', '39.2', '39.2', '48.3', '42.5', '42.5', '39.2', '43.3', '50.0']
o_2_list_zeller = ['65.0', '53.3', '50.0', '58.3', '56.7', '48.3', '57.5', '55.8', '55.8', '55.8']

o_1_list_zeller = [float(value) for value in o_1_list_zeller]
o_2_list_zeller = [float(value) for value in o_2_list_zeller]


statistic_zeller, p_value_zeller = wilcoxon(o_1_list_zeller, o_2_list_zeller, alternative='two-sided')
print(p_value_zeller)
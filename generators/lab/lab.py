import random

import click
import numpy as np
import math
from scipy.stats import chi2
import matplotlib.pyplot as plt

def gen_random_numbers(file_path, n):
    f = open(file_path, "w", encoding="utf-8")
    numbers = [random.randint(1, 10) % 2 for _ in range(n)]
    f.write(" ".join(map(str, numbers)))


def transform_lst_nums(num_lst):
    max_elem = max(num_lst) + 1
    return [num / max_elem for num in num_lst]


def get_data_from_file(file_path):
    with open(file_path, "r") as file:
        data_line = file.readline()
        num_lst = list(map(int, data_line.strip().split()))
    return transform_lst_nums(num_lst)


def check_chi_square(lst_num, alpha=0.05, lst_=None, exp=None, param=None):
    if param is None:
        param = len(np.unique(lst_num))
    if lst_ is None:
        _, lst_ = np.unique(lst_num, return_counts=True)
    if exp is None:
        exp = np.array([len(lst_num) / param] * param)

    chi = np.sum((lst_ - exp) ** 2 / exp)
    stat = chi2.ppf(1 - alpha, param - 1)
    return chi > stat


def check_series(numbers):
    d = 16
    alpha = 0.05
    param = d ** 2
    res = [0] * param

    for j in range(len(numbers) // 2):
        res[int(numbers[2 * j] * d) * d + int(numbers[2 * j + 1] * d)] += 1

    exp = np.array(param * [len(numbers) / (2 * param)])
    return check_chi_square(numbers, alpha, res, exp, param)


def check_interval(numbers, alpha=0.05, n=256, t=10, a=0.5, b=1):
    j, s, c_r = -1, 0, np.array([0] * (t + 1))
    while s < n:
        r = 0
        j += 1
        while j < len(numbers) and a <= numbers[j] <= b:
            r += 1
            j += 1
        c_r[min(r, t)] += 1
        s += 1
    p = b - a
    arr_1 = [n * p * pow(1.0 - p, r) for r in range(t)]
    arr_2 = [n * pow(1.0 - p, t)]
    exp = arr_1 + arr_2
    return check_chi_square(numbers, alpha, np.array(c_r), np.array(exp), t + 1)


def check_partitions(seq):
    alpha = 0.05
    n = 100
    param = int(10000 / n)
    r = np.array([0] * (param + 1))

    for i in range(n):
        r[len(np.unique(seq[param * i: param * (i + 1)]))] += 1

    p = []
    s = 1

    for i in range(param + 1):
        d = 100
        p_i = d
        for j in range(1, i):
            p_i *= d - j
        p.append(p_i / pow(d, param) * s)

    dk_lst = np.array([math.comb(param + i - 1, i) / pow(d, param) for i in range(param + 1)])
    return check_chi_square(seq, alpha, dk_lst[1:], p[1:], param)


def check_permutations(seq):
    alpha = 0.05
    t = 10
    n = len(seq)
    dict = {}
    param = math.factorial(t)

    for i in range(0, n, t):
        group = tuple(sorted(seq[i:i + t]))
        dict[group] = dict.get(group, 0) + 1

    lst_obs = sorted(list(dict.values()), reverse=True)

    exp = np.array([n / param] * len(lst_obs))

    return check_chi_square(seq, alpha, lst_obs, exp, param)


def check_monotony(seq):
    alpha = 0.05
    A = [
        [4529.4, 9044.9, 13568, 22615, 22615, 27892],
        [9044.9, 18097, 27139, 36187, 452344, 55789],
        [13568, 27139, 40721, 54281, 67582, 83685],
        [18091, 36187, 54281, 72414, 90470, 111580],
        [22615, 45234, 67852, 90470, 113262, 139476],
        [27892, 55789, 83685, 111580, 139476, 172860]
    ]
    b = [1 / 6, 5 / 24, 11 / 120, 19 / 720, 29 / 5040, 1 / 840]
    n = len(seq)
    lst = []

    i = 0
    while i < n:
        s = 1
        while i + s < n and seq[i + s - 1] <= seq[i + s]:
            s += 1
        lst.append(s)
        i += s

    counts = {}
    for l in lst:
        counts[l] = counts.get(l, 0) + 1

    res = []
    temp = 0
    for c in lst:
        m = 1 / 6
        min_val = min(c, 6)
        for i in range(min_val):
            for j in range(min_val):
                m += (seq[i + temp] - n * b[i]) * (seq[j + temp] - n * b[j]) * A[i][j]
        temp += c
        res.append(m)

    return check_chi_square(res, alpha)


def check_conflicts(srq):
    m = 1024
    l = len(srq)
    sr = l / m
    p0 = 1 - l / m + math.factorial(l) / (2 * math.factorial(l - 2) * m * 2)
    conf = l / m - 1 + p0
    return abs(conf - sr) > 10


def math_expectation_and_deviation(numbers):
    return numbers.mean(), numbers.std()


@click.command()
@click.option("/file", default=None, help="Имя файла с входной последовательностью")
def main(file):
    if file is None:
        gen_random_numbers("input_file.txt", 10_000)
        numbers = np.array(get_data_from_file("input_file.txt"))
    else:
        numbers = np.array(get_data_from_file(file))

    math_expectation, deviation = math_expectation_and_deviation(numbers)

    try:
        print(f"Мат. ожидание: {math_expectation}")
        print(f"Cр-кв. отклонение: {deviation}")
        print(f"Критерий хи-квадрат: {check_chi_square(numbers)}")
        print(f"Критерий серийт: {check_series(numbers)}")
        print(f"Критерий интервалов {check_interval(numbers)}")
        print(f"Критерий разбиений: {check_partitions(numbers)}")
        print(f"Критерий перестановок: {check_permutations(numbers)}")
        print(f"Критерий монотонности: {check_monotony(numbers)}")
        print(f"Критерий конфликтов: {check_conflicts(numbers)}")

    except Exception as err:
        print(f"В процессе произошла ошибка: {err}")

    size, mean, std = [], [], []
    for i in range(len(numbers)):
        size.append(i + 1)
        mean.append(numbers[:i + 1].mean())
        std.append(numbers[:i + 1].std())

    plt.xlabel("Объем выборки")
    plt.ylabel("Оценка")

    plt.plot(size, mean, label="Мат. ожидание")
    plt.plot(size, std, label="Cр-кв. отклонение")

    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()

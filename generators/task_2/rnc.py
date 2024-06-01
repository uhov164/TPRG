import math

import click


def uniform_distribution(a, b, numbers):
    m = max(numbers) + 1
    for x in numbers:
        yield x / m * b + a


def triangular_distribution(a, b, lst):
    m = max(lst) + 1
    lst = [x / m for x in lst]
    lst.append(lst[-1])
    for i in range(len(lst) - 1):
        even = lst[i]
        odd = lst[i + 1]
        yield a + b * (even + odd - 1)


def exp_distribution(a, b, numbers):
    m = max(numbers) + 1
    numbers = [x / m for x in numbers]
    for u in numbers:
        yield int(-b * math.log(u) + a)


def norm_distribution(mu, sigma, numbers):
    m = max(numbers) + 1
    numbers = [x / m for x in numbers]
    numbers.append(numbers[-1])
    odd = 0
    for i in range(len(numbers)):
        if i % 2 == 0:
            even = numbers[i]
            z1 = mu + sigma * math.sqrt(-2 * math.log(1 - odd)) * math.cos(2 * math.pi * even)
            z2 = mu + sigma * math.sqrt(-2 * math.log(1 - odd)) * math.sin(2 * math.pi * even)
            yield z1
            yield z2
        else:
            odd = numbers[i]


def gamma_distribution(a, b, numbers, k):
    m = max(numbers) + 1
    numbers = [x / m for x in numbers]
    lst_U_k = []
    for i in range(0, len(numbers), k):
        lst_U_k.append(numbers[i: i + k])

    if len(lst_U_k[-1]) != k:
        lst_U_k.pop()

    for arr in lst_U_k:
        val_mul = 1
        for num in arr:
            val_mul *= 1 - num
        res_val = a - b * math.log(val_mul)
        yield res_val


def longnorm_distribution(a, b, numbers):
    numbers = norm_distribution(0, 1, numbers)
    for z in numbers:
        yield a + math.exp(b - z)


def logistic_distribution(a, b, numbers):
    m = max(numbers) + 1
    numbers = [x / m for x in numbers]
    for u in numbers:
        yield a + b * math.log(u / (1 - u))


def binomial_distribution(p, count, numbers):
    n = len(numbers)
    m = max(numbers) + 1
    numbers = [x / m for x in numbers]
    for i in range(1, n):

        acc = 0
        y = numbers[i]

        while acc < numbers[i]:
            k = 0
            while y > k:
                c = math.comb(n, k)
                pow_p = pow(p, k)
                subs = pow(1 - p, n - k)
                acc += c * pow_p * subs
                k += 1
            y += 1

        num = 1
        i = 0
        while i < count:
            num *= 10
            i += 1

        yield int(y * 10**23) % num


def write_to_file(numbers, filepath):
    f = open("result/"+filepath, "w", encoding="UTF-8")
    data = " ".join(map(str, numbers))
    f.write(data)
    f.close()


def read_from_file(filepath):
    f = open(filepath, "r", encoding="UTF-8")
    numbers = map(int, f.read().split())
    return numbers


distributions = {
    'st': uniform_distribution,
    'tr': triangular_distribution,
    'ex': exp_distribution,
    'nr': norm_distribution,
    'gm': gamma_distribution,
    'ln': longnorm_distribution,
    'ls': logistic_distribution,
    'bi': binomial_distribution
}


@click.command()
@click.option(
    "/d", help="Указывает тип распределения: "
               "st – стандартное равномерное с заданным интервалом, "
               "tr – треугольное распределение, "
               "ex – общее экспоненциальное распределение, "
               "nr – нормальное распределение, "
               "gm – гамма распределение, "
               "ln – логнормальное распределение, "
               "ls – логистическое распределение, "
               "bi – биномиальное распределение",
    required=True, type=click.Choice(["st", "tr", "ex", "nr", "gm", "ln", "ls", "bi"]))
@click.option("/f", nargs=1, default="generated.dat",
              help="Указывает путь до файла из которого берется входная последовательность чисел")
@click.option("/p1", nargs=1, type=int, required=True,
              help="1-й параметр, необходимый, для генерации ПСЧ заданного распределения")
@click.option("/p2", nargs=1, type=int, required=True,
              help="2-й параметр, необходимый, для генерации ПСЧ заданного распределения (в случае bi указывает на количество разрядов в генерируемом числе до 10^6)")
@click.option("/p3", nargs=1, type=int, help="3-й параметр, необходимый, для генерации ПСЧ гамма-распределением",
              default=None)
def main(d, f, p1, p2, p3):
    try:
        distribution = distributions[d]
        input_numbers = list(read_from_file(f))

        numbers = []
        if p3 == None:
            numbers = [_ for _ in distribution(p1, p2, input_numbers)]
        else:
            numbers = [_ for _ in distribution(p1, p2, input_numbers, p3)]

        write_to_file(numbers, f"distr-{d}.dat")

    except Exception as err:
        print(f"В процессе произошла ошибка: {err}")


"""
python rnc.py /d st /p1 134 /p2 123124
python rnc.py /d tr /p1 289 /p2 1323
python rnc.py /d ex /p1 289 /p2 1323
python rnc.py /d nr /p1 234 /p2 12300
python rnc.py /d gm /p1 289 /p2 1323 /p3 2
python rnc.py /d ln /p1 289 /p2 132
python rnc.py /d ls /p1 289 /p2 132
python rnc.py /d bi /p1 234 /p2 5
"""
if __name__ == "__main__":
    main()

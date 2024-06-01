import click


def linear_congruent_generator(mod, a, c, x0, n=20):
    for _ in range(n):
        yield (a * x0 + c) % mod
        x0 = (a * x0 + c) % mod


def additive_generator(m, k, j, sequence, n=20):
    for _ in range(n):
        value = (sequence[-k] + sequence[-j]) % m
        sequence.append(value)
        yield value


def rslos_generator(coefs, register, n=20):
    len_registr = len(str(register))
    coefs, register = int(str(coefs), base=2), int(str(register), base=2)

    for _ in range(n):
        new_bit = (register ^ ((register ^ coefs) >> 1)) & 1
        register = (register >> 1) | (new_bit << (len_registr - 1))
        yield register


def five_parameter_generator(p, q1, q2, q3, w, x0, n=20):
    x0 = int(str(x0), 2)
    for _ in range(n):
        cur = 0
        for _ in range(w):
            bit_q1 = (x0 >> p - q1) & 1
            bit_q2 = (x0 >> p - q2) & 1
            bit_q3 = (x0 >> p - q3) & 1
            bit_x0 = x0 & 1
            xor = bit_q1 ^ bit_q2 ^ bit_q3 ^ bit_x0
            cur = (cur << 1) | xor
            x0 = (x0 >> 1) | (xor << p - 1)
        yield cur % 2 ** 10


def nonlinear_lfsr_generator(R1, R2, R3, w, x1, x2, x3, n=10000):
    lR1 = len(str(R1))
    lR2 = len(str(R2))
    lR3 = len(str(R3))
    for _ in range(n):
        cur = 0
        for _ in range(w):
            xorR1 = (x1 ^ (x1 >> lR1 - 1))
            xorR2 = (x2 ^ (x2 >> lR1 - 1))
            xorR3 = (x3 ^ (x3 >> lR1 - 1))
            res = ((xorR1 ^ xorR2) + (xorR2 ^ xorR3) + xorR3) & 1
            x1 = (x1 >> 1) | (res << lR1 - 1)
            x2 = (x2 >> 1) | (res << lR2 - 1)
            x3 = (x3 >> 1) | (res << lR3 - 1)
            cur = (cur << 1) | res
        yield cur % 2 ** 10


def mersen_generator(seed, mod, count_num=20):
    u, s, t, l, w, p, r, q = 11, 7, 15, 18, 32, 624, 31, 397
    b = 0x9D2C5680
    c = 0xEFC60000
    a = 0x9908B0DF

    def twist(arr_state):
        for i in range(p):
            y = (arr_state[i] >> r) + (arr_state[(i + 1) % p] & ((1 << r) - 1))
            arr_state[i] = arr_state[(i + q) % p] ^ (y >> 1)
            if y % 2 != 0:
                arr_state[i] ^= a

    def get_start_arr(seed, p):
        w = 32
        start_arr = [0] * p
        start_arr[0] = seed
        for i in range(1, p):
            start_arr[i] = (start_arr[i - 1] ^ (start_arr[i - 1] >> 30) + i) & ((1 << w) - 1)
        return start_arr

    def extract_number(arr_state, index):
        if index >= 624:
            twist(arr_state)
            index = 0

        y = arr_state[index]
        y ^= (y >> u)
        y ^= ((y << s) & b)
        y ^= ((y << t) & c)
        y ^= (y >> l)

        return y & ((1 << w) - 1), index + 1

    start_arr = get_start_arr(seed, mod)
    index = 0

    for _ in range(count_num):
        rand_num, index = extract_number(start_arr, index)
        yield rand_num


def rc4_generator(lst_start_params, n=20):
    length_key = len(lst_start_params)
    S = list(range(4096))
    j = 0
    for i in range(4096):
        j = (j + S[i] + lst_start_params[i % length_key]) % 4096
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    for _ in range(n):
        i = (i + 1) % 4096
        j = (j + S[i]) % 4096
        S[i], S[j] = S[j], S[i]
        key_val = S[(S[i] + S[j]) % 4096]
        yield key_val


def rsa_generator(n, e, w, x0, count=20):
    for _ in range(count):
        num = 0
        for _ in range(w):
            x0 = pow(x0, e, n)
            num = (num << 1) | (x0 & 1)
        yield num


def bbs_generator(x0, w, p=127, q=131, count_num=20):
    n = p * q
    for _ in range(count_num):
        num = 0
        for _ in range(w):
            x0 = pow(x0, 2, n)
            num = (num << 1) | (x0 & 1)
        yield num


generators = {
    'lc': lambda lst: linear_congruent_generator(lst[0], lst[1], lst[2], lst[3], lst[4]),
    'add': lambda lst: additive_generator(lst[0], lst[1], lst[2], lst[3:-1:], lst[-1]),
    '5p': lambda lst: five_parameter_generator(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6]),
    'lfsr': lambda lst: rslos_generator(lst[0], lst[1], lst[2]),
    'nfsr': lambda lst: nonlinear_lfsr_generator(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7]),
    'mt': lambda lst: mersen_generator(lst[0], lst[1], lst[2]),
    'rc4': lambda lst: rc4_generator(lst[0:-1:], lst[-1]),
    'rsa': lambda lst: rsa_generator(lst[0], lst[1], lst[2], lst[3], lst[4]),
    'bbs': lambda lst: bbs_generator(lst[0], lst[1], lst[2], lst[3], lst[4])
}


def write_to_file(data_list, filepath):
    f = open("result/"+filepath, "w", encoding="UTF-8")
    data = " ".join(map(str, data_list))
    f.write(data)
    f.close()


@click.command()
@click.option(
    '/g', type=click.Choice(["lc", "add", "5p", "lfsr", "nfsr", "mt", "rc4", "rsa", "bbs"]), required=True,
    help=(
            "Параметр указывает на метод генерации ПСЧ. "
            "код_метода может быть одним из следующих:\n"
            "  • lc – линейный конгруэнтный метод (i: a c m x[0] – целые неотрицательные числа; m > 0)\n"
            "  • add – аддитивный метод (i: c m a[1] a[2] ... a[s] x[1] ... x[s] – целые неотрицательные числа, меньше m; m > 0)\n"
            "  • 5p – пятипараметрический метод (i: p q1 q2 q3 w x0 – целые неотрицательные числа; w – разрядность выходного числа; p > q1, q2, q3 > 0; q1, q2, q3 – попарно различны; x0 – p-битное число)\n"
            "  • lfsr – регистр сдвига с обратной связью (РСЛОС) (i: p a x[0] l; a, x0 – p-битные неотрицательные числа, a и x0 интерпретируются как двоичный вектор)\n"
            "  • nfsr – нелинейная комбинация РСЛОС (i: n l p[1] a[1] x0[1] p[2] a[2] x0[2] ... p[n] a[n] x0[n] c[1] ... c[m]; n – количество генераторов, n > 0; l – количество бит в сгенерированном значении; p[i], a[i], x0[i] – параметры соответствующего РСЛОС; c[i] – n-битные числа)\n"
            "  • mt – вихрь Мерсенна (i: p w r q a u s t l b c; w – размерность слова; r – позиция разделения, r <= w; p, q – два положительных числа, 0 < q <= p; a, b, c – w-разрядные неотрицательные числа, 0 <= a, b, c < 2^w; u, s, t, l – коэффициенты, 0 <= u, s, t, l <= w)\n"
            "  • rc4 – RC4 (i: w K0 … K255, где w – длина в битах, на которую разбиваются блоки; K0 … K255 – некоторая перестановка чисел от 0 до 255)\n"
            "  • rsa – ГПСЧ на основе RSA (i: n e x0 w l - положительные целые числа; w > 0, x0 < n; w – количество генерируемых бит за шаг, l – разрядность выходного числа)\n"
            "  • bbs – алгоритм Блюма-Блюма-Шуба (i: n x0 l – положительные целые числа; x0 < n; l – разрядность выходного числа)"
    )
)
@click.option('/n', type=int, default=10000,
              help="- количество генерируемых чисел. Если параметр не указан, то генерируется 10000 чисел.")
@click.option('/f', default="rnd.dat",
              help="- полное имя файла, в который будут выводиться данные. Если параметр не указан, данные должны записываться в файл с именем rnd.dat.")
@click.option('/i', type=str, help="Перечисление параметров для выбранного генератора")
def main(g, i, n, f):
    i = list(map(int, i.split()))

    try:
        generator_name = g
        arguments = i + [n]
        generator = generators[generator_name]
        file = generator_name + "_" + f

        numbers = [i for i in generator(arguments)]
        write_to_file(numbers, file)

    except Exception as err:
        print(f"Произошла ошибка: {err}")


"""
Команды для запуска python файла:

python prng.py /g lc /i "1023 127 131 1024" /n 60
python prng.py /g add /i "1024 5 9 6667 9059 3718 5389 853 9038 224 249 3437 6699 7717 2761 1714 1377 3620 4124 6814 3110 7969 1477 1298" /n 600
python prng.py /g 5p /i "38 3 10 20 10 10101011010101001010110101000111010101" /n 600
python prng.py /g lfsr /i "1000010001 1011010110" /n 600
python prng.py /g nfsr /i "1101011001 1100010001 1011010110 10 857 785 726" /n 600
python prng.py /g mt /i "6423 1234" /n 60
python prng.py /g rc4 /i "2309 1203 3836 4107 1944 1438 7472 4532 9239 1077 5584 4680 5754 5801 199 5117 2565 1804 7971 6885 8378 1106 8790 5904 4452 9068 6075 2725 9864 8279 1988 4034 1876 5932 1248 2420 8835 6797 2803 5213 4804 3972 6051 7912 6017 4107 3940 3122 9365 5713 6289 5731 364 8800 7892 3089 3138 5523 3726 5040 1898 7809 1386 2869 7844 8246 5254 2503 1253 1130 3368 4382 5316 5249 6276 4071 7893 1765 4508 9952 2734 3559 2313 3554 4483 889 7323 1518 3766 672 2132 4096 6167 8673 1219 4086 3241 7996 4274 7696 5617 8175 3383 4388 519 9199 9937 8095 489 5095 7591 2498 476 1727 4817 3592 9017 9533 7800 247 8154 2620 9273 8977 8271 5786 301 8425 3318 9171 8835 3691 2379 6213 5385 8338 7764 5322 3286 2193 2187 6189 3051 9366 1614 8210 9968 4723 2478 435 3064 9248 8619 2021 3841 5971 2077 382 7749 9034 8472 8598 5136 8417 5803 9549 4291 4550 4321 1675 2637 6206 4375 7893 9847 7974 5142 6210 7902 6811 5930 5351 7533 4732 944 2317 4393 3491 9393 8178 2293 6346 172 508 9567 6172 673 6877 2249 9612 9801 6299 7482 2324 6037 2548 910 5037 5532 5077 2594 9638 4022 719 5356 1184 4081 2277 7486 9883 8842 7460 266 246 8079 6422 8838 2102 1858 9034 9417 9342 351 4897 1161 2116 3740 4348 4506 4074 8019 7703 2228 279 2787 1763 2594 4193 9236 3038 3772 9463 9862 1853 7645 721" /n 60
python prng.py /g rsa /i "37320042546258151385585748655126402275533898458677529665166237785905883512912615700605768608589299896136946304126741313488484989387521930513771133544049676415442489082044251499963695092831431208960561181495913575017558079374616598365042558446225838569076192130606654969509117761161385964776929093056043562942995644496964324119684633518554350805247688958172238783753657689734635149 21313771133544049676415442489082044251416763454483249741353934747840086819619366458506965160046575598181142166390510565647991519183809143795101153952660774855424443628817863597390818864925727668200496135675357577444496964324119684633518554350805247626192861013350488647068390875204840518919456340410569301907212781232077722298951260234859218593729374772847487435338361409891082097 10 10778408789827883569250963876980263028140342166390510565647991519183809143795122415167903694505657190781037011063318254988841723817121548695115458698533321645606935495430645111037117339877785302353945125794644703173404840518919456340410569301907212781238950110437222437807668278467459925384821541691940460003" /n 60
python prng.py /g bbs /i "620 5 127 131" /n 60
"""
if __name__ == "__main__":
    main()

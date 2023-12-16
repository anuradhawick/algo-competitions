import math
from collections import Counter


def get_masks(size):
    vals = []
    for x in range(1, 10**size):
        val = bin(x)[2:]
        if len(val) > size:
            return vals
        vals.append(val.rjust(size, "0"))


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = math.sqrt(n)
    for i in range(3, int(sqrt_n) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_replaceables(num, replace_count):
    num = str(num)
    chars = list(num)
    counts = Counter(chars)
    replace_max = 9 - replace_count

    positions = []

    for char, count in counts.items():
        if int(char) <= replace_max:
            pos = [n for n, c in enumerate(chars[:-1]) if c == char]
            if len(pos):
                positions += [pos]

    return positions


def get_prime_replacement_counts(number, count):
    len_num = len(str(number))
    positions = get_replaceables(number, count)
    for position in positions:
        size = len(position)
        masks = get_masks(size)

        for mask in masks:
            number_to_add = ["0" for _ in range(len_num)]
            for n, p in enumerate(position):
                number_to_add[p] = mask[n]

            number_to_add = int("".join(number_to_add))
            primes_seen = 0
            for x in range(10):
                new_number = number + number_to_add * x
                if len(str(new_number)) != len(str(number)):
                    break
                if is_prime(new_number):
                    primes_seen += 1

            if primes_seen == count:
                print(number, primes_seen)
                return True


s = 100001
c = 8
for x in range(s, s * 10, 2):
    if is_prime(x):
        if get_prime_replacement_counts(x, c):
            break

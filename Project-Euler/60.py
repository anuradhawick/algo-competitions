import math
from functools import cache
from collections import defaultdict


def sieve_of_Sundaram(n):
    """The sieve of Sundaram is a simple deterministic algorithm for finding all the prime numbers up to a specified integer."""
    k = (n - 2) // 2
    integers_list = [True] * (k + 1)
    result = []
    for i in range(1, k + 1):
        j = i
        while i + j + 2 * i * j <= k:
            integers_list[i + j + 2 * i * j] = False
            j += 1
    if n > 2:
        result.append(2)
    for i in range(1, k + 1):
        if integers_list[i]:
            result.append(2 * i + 1)
    return result


def is_prime_low_perf(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = math.sqrt(n)
    for i in range(3, int(sqrt_n) + 1, 2):
        if n % i == 0:
            return False
    return True


primes = sieve_of_Sundaram(10000000)
primes_subset = [p for p in primes if p < 10000]
primes_cache = set(primes)
pairs = []

is_prime = lambda x: x in primes_cache if x <= primes[-1] else is_prime_low_perf(x)


@cache
def valid_pair(m, n):
    return is_prime(int(str(m) + str(n))) and is_prime(int(str(n) + str(m)))


def get_groups(sorted_primes):
    groups = defaultdict(list)

    for m, p in enumerate(sorted_primes):
        for q in sorted_primes[m + 1 :]:
            if valid_pair(p, q):
                groups[(p,)].append(q)

    return groups


reps = 5
groups = get_groups(primes_subset)
for i in range(0, reps - 2):
    for k, v in list(groups.items()):
        k_groups = get_groups(v)

        for kk, v in k_groups.items():
            if len(v) + len(k) + len(kk) >= reps:
                groups[k + kk] = v
        del groups[k]

smallest = 99999999
choice = None

for k, v in groups.items():
    if smallest > sum(k) + v[0]:
        choice = k + tuple(v)
        smallest = sum(k) + v[0]

print(choice)
print(sum(choice))

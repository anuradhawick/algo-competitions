triangle = lambda n: str(int(n * (n + 1) / 2))
square = lambda n: str(int(n**2))
pentagonal = lambda n: str(int(n * (3 * n - 1) / 2))
hexagonal = lambda n: str(int(n * (2 * n - 1)))
heptagonal = lambda n: str(int(n * (5 * n - 3) / 2))
octagonal = lambda n: str(int(n * (3 * n - 2)))

tri = []
sq = []
pen = []
hexa = []
hepta = []
octa = []

for x in range(10000):
    if len(t := triangle(x)) == 4:
        tri.append(t)
    if len(s := square(x)) == 4:
        sq.append(s)
    if len(p := pentagonal(x)) == 4:
        pen.append(p)
    if len(hx := hexagonal(x)) == 4:
        hexa.append(hx)
    if len(hp := heptagonal(x)) == 4:
        hepta.append(hp)
    if len(oc := octagonal(x)) == 4:
        octa.append(oc)

kinds = [tri, sq, pen, hexa, hepta, octa]
found = []


def search_cycles(remaining_kinds=list(kinds), numbers=[]):
    if (
        len(remaining_kinds) == 0
        and numbers[0][:2] == numbers[-1][-2:]
        and len(set(numbers)) == len(kinds)
    ):
        found.append(numbers)

    if len(numbers) == 0:
        start_kind = remaining_kinds[0]
        for start in start_kind:
            search_cycles(remaining_kinds[1:], [start])
    else:
        last_number = numbers[-1]
        for kind in remaining_kinds:
            for next_number in kind:
                if last_number[-2:] == next_number[:2]:
                    search_cycles(
                        [k for k in remaining_kinds if k != kind],
                        numbers + [next_number],
                    )


search_cycles()
print(sum([int(x) for x in found[0]]))

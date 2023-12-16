from collections import defaultdict

data = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

data = open('4.txt').read()

s = 0

copies = defaultdict(int)
all_cards = [line.strip().split(":")[0] for line in data.strip().split("\n")]

for n, line in enumerate(data.strip().split("\n")):
    card_no, wnos_nos = line.strip().split(":")
    wnos, nos = wnos_nos.strip().split("|")
    wnos = list(map(int, (wnos.strip().split())))
    nos = list(map(int, (nos.strip().split())))

    copies[card_no] += 1

    for x in range(copies[card_no]):
        matches = sum([1 for x in nos if x in wnos])
        next_cards = all_cards[n+1:][:matches]

        for next_card_no in next_cards:
            copies[next_card_no] += 1

print(sum(copies.values()))

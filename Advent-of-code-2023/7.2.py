from collections import Counter


def fivekind(x):
    return 7 if len(set(x)) == 1 else 0


def fourkind(x):
    c = Counter(x)
    return 6 if c.most_common()[0][1] == 4 else 0


def fullhouse(x):
    c = Counter(x)
    return 5 if len(c) == 2 and c.most_common()[0][1] == 3 else 0


def threekind(x):
    c = Counter(x)
    return 4 if len(c) == 3 and c.most_common()[0][1] == 3 else 0


def twopair(x):
    c = Counter(x)
    return (
        3
        if len(c) == 3 and c.most_common()[0][1] == 2 and c.most_common()[1][1] == 2
        else 0
    )


def onepair(x):
    return 2 if len(set(x)) == 4 else 0


def highcard(x):
    return 1 if len(set(x)) == 5 else 0


alphabet = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

data = open("7.txt").read()

data = [
    (line.strip().split()[0], int(line.strip().split()[1]))
    for line in data.strip().split("\n")
]

def apply_wild_card(x):
    c = Counter(x)
    c.pop('J')
    if len(c) == 0:
        return 'AAAAA'
    return x.replace('J', c.most_common()[0][0])
    

def sort_key(args):
    original_card, bid = args
    if 'J' not in original_card:
        x = original_card
    else:
        x = apply_wild_card(original_card)
    
    print(x)
    
    return [
        fivekind(x)
        + fourkind(x)
        + fullhouse(x)
        + threekind(x)
        + twopair(x)
        + onepair(x)
        + highcard(x)
    ] + [alphabet[c] for c in original_card]


sorted_data = sorted(data, key=sort_key)
print(sum([(n + 1) * bid for n, (_, bid) in enumerate(sorted_data)]))


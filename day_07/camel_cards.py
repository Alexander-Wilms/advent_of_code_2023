from pprint import pprint

# https://stackoverflow.com/a/57003713/2278742
from functools import cmp_to_key


def primary_ordering(hand) -> int:
    print(f"primary_ordering({hand})")
    card_counts = {}
    for card in hand:
        try:
            card_counts[card] += 1
        except Exception:
            card_counts[card] = 1
    pprint(card_counts)

    strength = -1
    if len(list(card_counts.keys())) == 1:
        strength = 6

    if 4 in card_counts.values():
        strength = 5

    if 3 in card_counts.values() and 2 in card_counts.values():
        strength = 4

    if 3 in card_counts.values() and 1 in card_counts.values():
        strength = 3

    if 2 in card_counts.values() and 1 in card_counts.values():
        strength = 2

    if len(list(card_counts.keys())) == 4:
        strength = 1

    if len(list(card_counts.keys())) == 5:
        strength = 0

    print(f"{strength=}")
    print()
    return strength


# def secondary_ordering(hand) -> int:


def compare_hands(item1, item2) -> bool:
    item1 = item1["hand"]
    item2 = item2["hand"]
    print(f"comparing {item1} and {item2}")
    # return True if item1 > item2
    strength_1 = primary_ordering(item1)
    strength_2 = primary_ordering(item2)
    if strength_1 != strength_2:
        print(f"{item1} != {item2}")
        return strength_1 - strength_2
    else:
        print(f"{item1} == {item2}")
        secondary_ordering = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
        for index in range(5 + 1):
            if secondary_ordering[item1[index]] != secondary_ordering[item2[index]]:
                return secondary_ordering[item1[index]] - secondary_ordering[item2[index]]
    return False


def solve_puzzle_part(file_name: str, part: int) -> int:
    hands = []
    with open(file_name) as f:
        for line in f.readlines():
            hand = {}
            hand["hand"] = line.split(" ")[0]
            hand["bid"] = int(line.split(" ")[1])
            hands.append(hand)
    print("hands:")
    pprint(hands)

    sorted_hands = sorted(hands, key=cmp_to_key(compare_hands))

    print("sorted hands:")
    pprint(sorted_hands)

    total_winnings = 0
    for idx in range(len(sorted_hands)):
        bid = sorted_hands[idx]["bid"]
        hand = sorted_hands[idx]["hand"]

        print(f"{bid} * {idx+1} + ", end="")
        total_winnings += bid * (idx + 1)

    print("0")

    print(f"{total_winnings=}")
    return total_winnings


def test_solutions():
    for hand in ["AAAAA", "AA8AA", "23332", "TTT98", "23432", "A23A4", "23456"]:
        primary_ordering({"hand": hand})

    sum = solve_puzzle_part("day_07/example_1.txt", 1)
    assert sum == 6440

    sum = solve_puzzle_part("day_07/input.txt", 1)
    print(sum)


if __name__ == "__main__":
    test_solutions()

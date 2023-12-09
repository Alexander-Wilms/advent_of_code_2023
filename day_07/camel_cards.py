# https://stackoverflow.com/a/57003713/2278742
from functools import cmp_to_key, lru_cache
from pprint import pprint


def primary_ordering(hand) -> int:
    global part
    # print(f"primary_ordering({hand})")
    card_counts = {}
    for card in hand:
        try:
            card_counts[card] += 1
        except Exception:
            card_counts[card] = 1
    # pprint(card_counts)

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

    # print(f"{strength=}")
    # print()
    return strength


# def secondary_ordering(hand) -> int:
@lru_cache(maxsize=None)
def get_strongest_joker_replacement(hand: str) -> tuple[str, int]:
    if "J" not in hand:
        return hand, primary_ordering(hand)
    # print(f"get_strongest_joker_replacement({hand})")
    possible_cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    cards = ["", "", "", "", ""]

    strongest_hand_yet = hand
    highest_strength_yet = 0

    for cards[0] in possible_cards:
        for cards[1] in possible_cards:
            for cards[2] in possible_cards:
                for cards[3] in possible_cards:
                    for cards[4] in possible_cards:
                        possible_hand = ""
                        for card_idx in range(len(hand)):
                            if hand[card_idx] == "J":
                                possible_hand += cards[card_idx]
                            else:
                                possible_hand += hand[card_idx]
                        # print(f"{possible_hand=}")
                        strength = primary_ordering(possible_hand)
                        if strength > highest_strength_yet:
                            highest_strength_yet = strength
                            strongest_hand_yet = possible_hand

    # print(f"{strongest_hand_yet=}")
    assert strongest_hand_yet != ""
    return strongest_hand_yet, highest_strength_yet


def compare_hands(item1, item2) -> int:
    global part
    item1 = item1["hand"]
    item2 = item2["hand"]
    # print(f"comparing {item1} and {item2}")
    # return True if item1 > item2
    if part == 1:
        strength_1 = primary_ordering(item1)
        strength_2 = primary_ordering(item2)
    else:
        # for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be
        # thus, don't overwrite item1 and item2
        _, strength_1 = get_strongest_joker_replacement(item1)
        _, strength_2 = get_strongest_joker_replacement(item2)

    if strength_1 != strength_2:
        # print(f"{item1} != {item2}")
        return strength_1 - strength_2
    else:
        # print(f"{item1} == {item2}")
        if part == 1:
            secondary_ordering = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
        else:
            secondary_ordering = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
        for index in range(5):
            if secondary_ordering[item1[index]] != secondary_ordering[item2[index]]:
                return secondary_ordering[item1[index]] - secondary_ordering[item2[index]]

    # equal value
    return 0


def solve_puzzle_part(file_name: str, part_selection: int) -> int:
    global part
    part = part_selection
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
    global part
    part = 2

    for hand in ["AAAAA", "AA8AA", "23332", "TTT98", "23432", "A23A4", "23456"]:
        primary_ordering({"hand": hand})

    sum = solve_puzzle_part("day_07/example_1.txt", 1)
    assert sum == 6440

    sum = solve_puzzle_part("day_07/input.txt", 1)
    assert sum == 249748283

    sum = solve_puzzle_part("day_07/example_1.txt", 2)
    assert sum == 5905

    # 32T3K is still the only one pair
    strength = primary_ordering("32T3K")
    assert strength == 1

    # KK677 is now the only two pair
    strength = primary_ordering("KK677")
    assert strength == 2

    # T55J5, KTJJT, and QQQJA are now all four of a kind
    joker_replacement, _ = get_strongest_joker_replacement("T55J5")
    print(joker_replacement)
    assert joker_replacement == "T5555"
    strength = primary_ordering(joker_replacement)
    assert strength == 5

    joker_replacement, _ = get_strongest_joker_replacement("KTJJT")
    assert joker_replacement == "KTTTT"
    strength = primary_ordering(joker_replacement)
    assert strength == 5

    joker_replacement, _ = get_strongest_joker_replacement("QQQJA")
    assert joker_replacement == "QQQQA"
    strength = primary_ordering(joker_replacement)
    assert strength == 5

    strongest_hand_yet, _ = get_strongest_joker_replacement("69QK2")
    assert strongest_hand_yet == "69QK2"

    assert compare_hands({"hand": "JKKK2"}, {"hand": "QQQQ2"}) < 0

    sum = solve_puzzle_part("day_07/example_2.txt", 1)
    print(sum)

    assert compare_hands({"hand": "AT934"}, {"hand": "2249A"}) < 0

    assert compare_hands({"hand": "557T5"}, {"hand": "A777A"}) < 0

    sum = solve_puzzle_part("day_07/input.txt", 2)
    print(sum)
    assert sum > 247900123
    assert sum == 248029057


if __name__ == "__main__":
    test_solutions()

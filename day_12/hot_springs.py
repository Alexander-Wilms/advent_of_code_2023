import re
from pprint import pprint


def replace_recursive(template: str, groups: list, match_count: int = 0) -> int:
    # print(f"replace_recursive({template})")
    unknown_count = template.count("?")
    matches = re.findall(r"1+", template)
    # pprint(f"{template}: {matches=}")

    if unknown_count == 0:
        if len(matches) == len(groups):
            match_lengths = [len(x) for x in matches]
            if match_lengths == groups:
                # print("could be a match")
                return match_count + 1
        return match_count
    else:
        template_0 = template.replace("?", "0", 1)
        match_count = replace_recursive(template_0, groups, match_count)
        template_1 = template.replace("?", "1", 1)
        match_count = replace_recursive(template_1, groups, match_count)
        return match_count


def solve_puzzle_part(file_name: str) -> int:
    springs = {}

    with open(file_name) as f:
        count = 0
        for line in f.readlines():
            line = line.strip()
            springs[count] = {}
            tmp = line.split(" ")[0]
            tmp = re.sub(r"\.+", ".", tmp)
            springs[count][0] = tmp.replace(".", "0").replace("#", "1").strip("0")
            tmp = line.split(" ")[1].split(",")
            tmp = [int(x) for x in tmp]
            springs[count][1] = tmp
            count += 1

    print("preprocessed data:")
    pprint(springs)

    sum_of_counts = 0
    for val in springs.values():
        sum_of_counts += replace_recursive(val[0], val[1])

    return sum_of_counts


def test_solutions():
    number_of_possible_arrangements = replace_recursive("???", [1, 1])
    assert number_of_possible_arrangements == 1

    number_of_possible_arrangements = replace_recursive("??0??", [1, 1])
    assert number_of_possible_arrangements == 4

    number_of_possible_arrangements = replace_recursive("?1?1?1?1?1?1?1?", [1, 3, 1, 6])
    assert number_of_possible_arrangements == 1

    number_of_possible_arrangements = replace_recursive("????", [1])
    assert number_of_possible_arrangements == 4

    number_of_possible_arrangements = replace_recursive("?111????????", [3, 2, 1])
    assert number_of_possible_arrangements == 10

    sum_of_counts = solve_puzzle_part("day_12/example_1.txt")
    assert sum_of_counts == 21

    sum_of_counts = solve_puzzle_part("day_12/input.txt")
    assert sum_of_counts == 7506


if __name__ == "__main__":
    test_solutions()

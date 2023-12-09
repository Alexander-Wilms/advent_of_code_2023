import re
from pprint import pprint


def solve_puzzle_part(file_name: str, part: int) -> int:
    report = []
    with open(file_name) as f:
        for line in f.readlines():
            history = re.findall(r"\d+", line)
            history = [int(x) for x in history]
            report.append([history])
    # print("report:")
    # pprint(report)

    sum = 0
    idx = 0
    for histories_idx in range(len(report)):
        print(f"{histories_idx}/{len(report)}")
        all_deltas_zeros = False
        indent = ""
        idx = 0
        while not all_deltas_zeros:
            history = report[histories_idx][idx]

            sum += report[histories_idx][-1][-1]

            if report[histories_idx][-1].count(0) == len(report[histories_idx][-1]):
                all_deltas_zeros = True
            # print(indent, end="")
            # for value in history:
            # print(f"{value:=3} ", end="")
            # print()

            differences = []
            for history_idx in range(len(history) - 1):
                differences.append(history[history_idx + 1] - history[history_idx])

            report[histories_idx].append(differences)
            if differences.count(0) == len(differences):
                all_deltas_zeros = True

            # pprint(report)
            idx += 1
        # print()

    print(f"{sum=}")

    return sum


def test_solutions() -> None:
    sum = solve_puzzle_part("day_09/example_1.txt", 1)
    assert sum == 114

    sum = solve_puzzle_part("day_09/input.txt", 1)
    print(sum)
    assert sum > 1715873178


if __name__ == "__main__":
    test_solutions()

import math
import re
from pprint import pprint


def get_actual_seeds(seeds: list[int]) -> list[int]:
    actual_seeds = []
    for idx in range(0, len(seeds), 2):
        # print(f"The {idx+1}. range starts with seed number {seeds[idx]} and contains {seeds[idx + 1]} values:")
        this_range = list(range(seeds[idx], seeds[idx] + seeds[idx + 1]))
        # pprint(this_range)
        actual_seeds += this_range
    return actual_seeds


def map_almanach_item(almanach: dict, source_value: int, origin_type: str) -> tuple[int, str]:
    destination_type = list(almanach[origin_type].keys())[0]

    count = 1
    mapping_found = False
    for mapping in almanach[origin_type][destination_type]:
        # print(f"Checking mapping {count} of {len(almanach[origin_type][destination_type])}")
        count += 1
        # pprint(mapping)
        # print(f"Source range starts at {mapping['source_range_start']} and contains {mapping['range_length']} values:")
        # pprint(list(range(mapping["source_range_start"], mapping["source_range_start"] + mapping["range_length"])))

        # print(f"Destination range starts at {mapping['destination_range_start']} and contains {mapping['range_length']} values:")
        # pprint(list(range(mapping["destination_range_start"], mapping["destination_range_start"] + mapping["range_length"])))

        if source_value >= mapping["source_range_start"] and source_value <= mapping["source_range_start"] + mapping["range_length"]:
            # print(f"Origin value {source_value} in source range")
            destination_value = source_value - mapping["source_range_start"] + mapping["destination_range_start"]
            mapping_found = True
            break
        else:
            pass
            # print(f"Origin value {source_value} not in source range")
    if not mapping_found:
        destination_value = source_value

    # print(f">>> {origin_type} {source_value} mapped to {destination_type} {destination_value}")
    return destination_value, destination_type


def solve_puzzle_part(file_name: str, part: int) -> int:
    almanach = {}
    with open(file_name) as f:
        lines = f.readlines()
        processing_map = False
        origin = ""
        destination = ""
        map_idx = 0
        almanach_origin_created = False
        for i in range(len(lines)):
            line = lines[i].strip()
            print(f"{line=}")
            if not line:
                continue

            if line.startswith("seeds"):
                seeds = re.findall(r"\d+", line)
                seeds = [int(seed) for seed in seeds]
                print(f"{seeds=}")

            if "map" in line:
                processing_map = True
                origin = line.split("-")[0]
                destination = line.split("-")[2].split(" ")[0]
                map_idx = 0
                almanach_origin_created = False

            if processing_map and "map" not in line:
                current_map = re.findall(r"\d+", line)
                if not almanach_origin_created:
                    almanach[origin] = {}
                    almanach_origin_created = True
                if map_idx == 0:
                    almanach[origin][destination] = list()
                    pprint(almanach)
                print(map_idx)
                almanach[origin][destination].append({})
                almanach[origin][destination][map_idx]["destination_range_start"] = int(current_map[0])
                almanach[origin][destination][map_idx]["source_range_start"] = int(current_map[1])
                almanach[origin][destination][map_idx]["range_length"] = int(current_map[2])
                pprint(almanach)
                map_idx += 1

    pprint(almanach)

    lowest_location_number = math.inf

    if part == 2:
        seeds = get_actual_seeds(seeds)

    for seed in seeds:
        source_type = "seed"
        source_value = seed
        destination_value = -1
        while source_type in almanach.keys():
            print(f"{source_type} {source_value}, ", end="")
            destination_value, destination_type = map_almanach_item(almanach, source_value, source_type)
            source_value = destination_value
            source_type = destination_type
        print(f"{source_type} {source_value}")
        if source_value < lowest_location_number:
            lowest_location_number = source_value

    print(f"{lowest_location_number=}")
    return lowest_location_number


def test_solutions():
    sum = solve_puzzle_part("day_05/example_1.txt", 1)
    assert sum == 35

    sum = solve_puzzle_part("day_05/input.txt", 1)
    assert sum == 323142486

    expected_actual_seeds = list(range(79, 79 + 14)) + list(range(55, 55 + 13))
    actual_seeds = get_actual_seeds([79, 14, 55, 13])
    print(f"{expected_actual_seeds=}")
    print(f"{actual_seeds=}")
    assert expected_actual_seeds == actual_seeds

    sum = solve_puzzle_part("day_05/test_case_ranges.txt", 2)
    assert sum == 46

    sum = solve_puzzle_part("day_05/example_1.txt", 2)
    assert sum == 46

    sum = solve_puzzle_part("day_05/input.txt", 2)
    print(sum)


if __name__ == "__main__":
    test_solutions()

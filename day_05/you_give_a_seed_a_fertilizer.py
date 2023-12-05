import math
import re
from pprint import pprint
import itertools
from functools import lru_cache

almanac = {}


def get_actual_seeds(seeds: list[int]) -> list[int]:
    actual_seeds = range(0, -1)
    for idx in range(0, len(seeds), 2):
        # print(f"The {idx+1}. range starts with seed number {seeds[idx]} and contains {seeds[idx + 1]} values:")
        actual_seeds = itertools.chain(actual_seeds, range(seeds[idx], seeds[idx] + seeds[idx + 1]))
        # pprint(this_range)
    return actual_seeds


@lru_cache(maxsize=None)
def map_almanac_item(source_value: int, origin_type: str) -> tuple[int, str]:
    global almanac
    destination_type = list(almanac[origin_type].keys())[0]

    count = 1
    mapping_found = False
    for mapping in almanac[origin_type][destination_type]:
        # print(f"Checking mapping {count} of {len(almanac[origin_type][destination_type])}")
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
    global almanac
    with open(file_name) as f:
        lines = f.readlines()
        processing_map = False
        origin = ""
        destination = ""
        map_idx = 0
        almanac_origin_created = False
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
                almanac_origin_created = False

            if processing_map and "map" not in line:
                current_map = re.findall(r"\d+", line)
                if not almanac_origin_created:
                    almanac[origin] = {}
                    almanac_origin_created = True
                if map_idx == 0:
                    almanac[origin][destination] = list()
                    pprint(almanac)
                print(map_idx)
                almanac[origin][destination].append({})
                almanac[origin][destination][map_idx]["destination_range_start"] = int(current_map[0])
                almanac[origin][destination][map_idx]["source_range_start"] = int(current_map[1])
                almanac[origin][destination][map_idx]["range_length"] = int(current_map[2])
                pprint(almanac)
                map_idx += 1

    pprint(almanac)

    lowest_location_number = math.inf

    if part == 1:
        actual_seeds = seeds
    else:
        actual_seeds = get_actual_seeds(seeds)

    for seed in actual_seeds:
        source_type = "seed"
        source_value = seed
        destination_value = -1
        while source_type in almanac.keys():
            print(f"{source_type} {source_value}, ", end="")
            destination_value, destination_type = map_almanac_item(source_value, source_type)
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
    assert expected_actual_seeds == list(actual_seeds)

    sum = solve_puzzle_part("day_05/test_case_ranges.txt", 2)
    assert sum == 46

    sum = solve_puzzle_part("day_05/example_1.txt", 2)
    assert sum == 46

    # sum = solve_puzzle_part("day_05/input.txt", 2)
    # print(sum)


if __name__ == "__main__":
    test_solutions()

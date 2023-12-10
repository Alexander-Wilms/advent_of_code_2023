# comment out networkx to compile code with Cython
import math
from pprint import pprint
from typing import Dict

import networkx as nx

map: Dict[str, Dict[str, str]] = {}


def solve_puzzle_part(file_name: str, part: int) -> int:
    G = nx.DiGraph()
    options = {
        "font_size": 10,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
    }
    labels = {}
    pipe_connectivity = {"|": [[0, -1], [0, 1]], "-": [[-1, 0], [1, 0]], "L": [[0, -1], [1, 0]], "J": [[0, -1], [-1, 0]], "7": [[-1, 0], [0, 1]], "F": [[1, 0], [0, 1]]}
    start_node = "-1,-1"
    with open(file_name) as f:
        row_idx = 0
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            col_idx = 0
            for char in line:
                if char != ".":
                    print(f"char: '{char}'")
                    id = f"{col_idx},{row_idx}"

                    print(f"{id=}")
                    G.add_node(id)
                    labels[id] = char

                    try:
                        connection_1 = f"{col_idx+pipe_connectivity[char][0][0]},{row_idx+pipe_connectivity[char][0][1]}"
                        connection_2 = f"{col_idx+pipe_connectivity[char][1][0]},{row_idx+pipe_connectivity[char][1][1]}"

                        print(f"{connection_1=}")
                        print(f"{connection_2=}")

                        G.add_edge(id, connection_1)
                        G.add_edge(id, connection_2)
                    except:
                        pass

                    if char == "S":
                        start_node = id
                        for row_delta in [-1, 0, 1]:
                            for col_delta in [-1, 0, 1]:
                                if not (row_delta == 0 and col_delta == 0):
                                    G.add_edge(id, f"{col_idx+col_delta},{row_idx+row_delta}")

                    # nx.draw_networkx(G, nx.kamada_kawai_layout(G), **options)
                    # nx.draw_networkx_labels(G, nx.kamada_kawai_layout(G), labels)
                    # plt.show(block=True)
                col_idx += 1

            row_idx += 1

    # nx.draw_networkx(G, nx.kamada_kawai_layout(G), **options)
    # plt.show(block=True)

    # remove nodes without edges
    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isolate.isolates.html
    G.remove_nodes_from(list(nx.isolates(G)))

    # nx.draw_networkx(G, nx.kamada_kawai_layout(G), **options)
    # plt.show(block=True)

    # https://stackoverflow.com/a/35684668/2278742
    G = G.to_undirected(True)
    simple_cycles = list(nx.simple_cycles(G))
    pprint(f"{start_node=}")
    if start_node == "-1,-1":
        relevant_cycle = simple_cycles
    else:
        pprint(f"{simple_cycles=}")
        for cycle in simple_cycles:
            if start_node in cycle:
                relevant_cycle = cycle
                break

    cycle_nodes = sorted(relevant_cycle)
    pprint(cycle_nodes)

    # nx.draw_networkx(G_reduced, nx.kamada_kawai_layout(G), **options)
    # plt.show(block=True)

    if start_node == "-1,-1":
        steps_to_farthest_point = math.floor(len(*cycle_nodes) / 2)
    else:
        steps_to_farthest_point = math.floor(len(cycle_nodes) / 2)

    print()

    return steps_to_farthest_point


def test_solutions():
    steps = solve_puzzle_part("day_10/example_1.txt", 1)
    print(steps)
    assert steps == 4

    steps = solve_puzzle_part("day_10/example_4_without_S.txt", 1)
    assert steps == 8

    steps = solve_puzzle_part("day_10/example_4.txt", 1)
    assert steps == 8

    steps = solve_puzzle_part("day_10/input.txt", 1)
    assert steps == 6690


if __name__ == "__main__":
    test_solutions()

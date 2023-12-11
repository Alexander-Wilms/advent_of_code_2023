# comment out networkx to compile code with Cython
import copy
import math
import os
from pprint import pprint
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from pandas import DataFrame

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
    G_everything = nx.Graph()
    G_pipes = nx.DiGraph()

    options = {
        "font_size": 10,
        "node_size": 500,
        "node_color": "white",
        "edgecolors": "black",
    }
    pipe_connectivity = {"|": [[0, -1], [0, 1]], "-": [[-1, 0], [1, 0]], "L": [[0, -1], [1, 0]], "J": [[0, -1], [-1, 0]], "7": [[-1, 0], [0, 1]], "F": [[1, 0], [0, 1]]}
    start_node = "-1,-1"
    with open(file_name) as f:
        data = f.readlines()
    with open(f"{file_name}.csv", "w") as f:
        for line in data:
            start_of_line = True
            for char in line:
                if char != "\n":
                    if not start_of_line:
                        f.write(",")
                    f.write(f"{char}")
                start_of_line = False
            f.write("\n")

    map: DataFrame = pd.read_csv(f"{file_name}.csv", header=None)
    os.remove(f"{file_name}.csv")

    print(map)

    (rows, cols) = map.shape

    print(f"{rows=}")
    print(f"{cols=}")
    start_node = "-1,-1"
    for col_idx in range(cols):
        for row_idx in range(rows):
            char = map.at[row_idx, col_idx]
            # print(f"char: '{char}'", end=", ")
            id = f"{row_idx},{col_idx}"
            # print(f"{id=}")

            if char == "S":
                start_node = id

            if part == 2:
                # add node to both graphs
                G_everything.add_node(id)
                G_pipes.add_node(id)

            if part == 1:
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
            else:
                # add directed pipe connections
                if char in list(pipe_connectivity.keys()):
                    try:
                        connection_1 = f"{row_idx+pipe_connectivity[char][0][1]},{col_idx+pipe_connectivity[char][0][0]}"
                        connection_2 = f"{row_idx+pipe_connectivity[char][1][1]},{col_idx+pipe_connectivity[char][1][0]}"

                        # print(f"{connection_1=}")
                        # print(f"{connection_2=}")

                        G_pipes.add_edge(id, connection_1)
                        G_pipes.add_edge(id, connection_2)
                    except:
                        pass

                for row_delta in [-1, 0, 1]:
                    for col_delta in [-1, 0, 1]:
                        if not (row_delta == 0 and col_delta == 0) and abs(row_delta) != abs(col_delta):
                            neighbor_col = col_idx + col_delta
                            neighbor_row = row_idx + row_delta
                            if neighbor_row in range(rows) and neighbor_col in range(cols):
                                # add undirected connection
                                G_everything.add_edge(id, f"{neighbor_row},{neighbor_col}")
                                pass

            # nx.draw_networkx(G, nx.kamada_kawai_layout(G), **options)
            # nx.draw_networkx_labels(G, nx.kamada_kawai_layout(G), labels)
            # plt.show(block=True)

    print("Done creating graphs")

    print("Processing graphs...")
    if part == 1:
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

        print(f"{steps_to_farthest_point=}")

        return steps_to_farthest_point
    else:
        copy.copy(G_pipes)

        # G_pipes.remove_nodes_from(list(nx.isolates(G_pipes)))
        # plt.title(f"{file_name}: Isolates removed")
        # nx.draw_networkx(G_pipes, nx.kamada_kawai_layout(G_pipes), **options)
        # plt.show(block=True)

        # convert to undirected to find cycles
        # https://stackoverflow.com/a/35684668/2278742
        G_pipes_undirected = copy.copy(G_pipes)
        G_pipes_undirected = G_pipes_undirected.to_undirected(False)

        G_pipes_undirected_isolated_removed = G_pipes_undirected
        G_pipes_undirected_isolated_removed.remove_nodes_from(list(nx.isolates(G_pipes_undirected_isolated_removed)))

        G_pipes_isolated_removed = nx.DiGraph(G_pipes)
        G_pipes_isolated_removed.remove_nodes_from(list(nx.isolates(copy.copy(G_pipes_isolated_removed))))

        print("Searching simple cycles in graph...")
        simple_cycles = list(nx.simple_cycles(G_pipes_undirected_isolated_removed))
        if simple_cycles:
            print("Simple cycles found")
        else:
            print("No simple cycles found")
        pprint(f"{start_node=}")
        # pprint(f"{simple_cycles=}")
        if start_node == "-1,-1":
            relevant_cycle = simple_cycles
        else:
            # pprint(f"{simple_cycles=}")
            for cycle in simple_cycles:
                if start_node in cycle:
                    relevant_cycle = cycle
                    break

        pprint(G_pipes.nodes.keys())
        cycle_nodes = sorted(relevant_cycle)
        print(f"{cycle_nodes=}")
        G_reduced = G_pipes_undirected.subgraph(cycle_nodes)

        nodes_inside_cycle_including_cycle: set[str] = set()

        wrong_approach = False

        if wrong_approach:
            for cycle_node_start in relevant_cycle:
                for cycle_node_end in relevant_cycle:
                    if cycle_node_start != cycle_node_end:
                        shortest_path = nx.shortest_path(G_everything, cycle_node_start, cycle_node_end)

                        number_of_cycle_nodes_in_shortest_path = len(set(shortest_path).intersection(set(cycle_nodes)))
                        # print(f"{number_of_cycle_nodes_in_shortest_path=}")

                        if number_of_cycle_nodes_in_shortest_path == 2:
                            print(f"shortest path from '{cycle_node_start}' to '{cycle_node_end}': {shortest_path=}")
                            nodes_inside_cycle_including_cycle = nodes_inside_cycle_including_cycle.union(shortest_path)

        else:
            for row in range(0, rows):
                inside_cycle = False
                print()
                for col in range(1, cols):
                    previous_node = f"{row},{col-1}"
                    node_name = f"{row},{col}"
                    next_node = f"{row},{col+1}"

                    print(f"checking second node '{previous_node}' -> '{node_name}' -> '{next_node}'")

                    if node_name in cycle_nodes and ((previous_node not in cycle_nodes) or (next_node not in cycle_nodes)):
                        inside_cycle = not inside_cycle

                    if inside_cycle and node_name not in cycle_nodes:
                        nodes_inside_cycle_including_cycle.add(node_name)
                        print("node inside cycle")
                    else:
                        print("node NOT inside cycle")

        print(f"{nodes_inside_cycle_including_cycle=}")

        nodes_inside_cycle = nodes_inside_cycle_including_cycle.difference(cycle_nodes)

        print(f"{nodes_inside_cycle=}")
        number_of_tiles = len(nodes_inside_cycle)

        if "input.txt" not in file_name:
            # plotting is very slow with the amount of nodes in the input.txt file
            fig, axes = plt.subplots(nrows=5, ncols=1)
            ax = axes.flatten()

            ax[0].set_title("All nodes")
            nx.draw_networkx(G_everything, nx.kamada_kawai_layout(G_everything), **options, ax=ax[0])

            ax[1].set_title("Pipe connections")
            nx.draw_networkx(G_pipes, nx.kamada_kawai_layout(G_everything), **options, ax=ax[1])

            ax[2].set_title("Undirected graph of pipe connection")
            nx.draw_networkx(G_pipes.to_undirected(False), nx.kamada_kawai_layout(G_everything), **options, ax=ax[2])

            ax[3].set_title("Isolated nodes removed")
            nx.draw_networkx(G_pipes_undirected_isolated_removed, nx.kamada_kawai_layout(G_everything), **options, ax=ax[3])

            ax[4].set_title(f"Cycle that includes the start node '{start_node}'")
            nx.draw_networkx(G_reduced, nx.kamada_kawai_layout(G_everything), **options, ax=ax[4])

            plt.show(block=True)

        print(f"{number_of_tiles=}")
        return number_of_tiles


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

    tiles = solve_puzzle_part("day_10/example_6.txt", 2)
    assert tiles == 4

    tiles = solve_puzzle_part("day_10/example_part_2_minimal.txt", 2)
    assert tiles == 2

    #tiles = solve_puzzle_part("day_10/example_part_2.txt", 2)
    #assert tiles == 10

    # tiles = solve_puzzle_part("day_10/input.txt", 2)
    # print(tiles)


if __name__ == "__main__":
    test_solutions()

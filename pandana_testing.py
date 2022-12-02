import aequilibrae as ae
import pandana as pnd
import pandas as pd
import timeit


def pandana_init(graph: ae.Graph, cost: str, geo):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    graph.set_graph(cost)
    pnet = pnd.Network(geo[:, 0], geo[:, 1], graph.compact_graph["a_node"], graph.compact_graph["b_node"],
                       pd.DataFrame(graph.compact_cost), twoway=False)

    c = graph.compact_nodes_to_indices[graph.centroids]
    return pnet, [o for o in c for d in c], [d for o in c for d in c]


def pandana_testing(net: pnd.Network, orig, dest, iters: int = 2, repeats: int = 5):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    timer = timeit.Timer(lambda: pandana_compute(net, orig, dest))
    times = timer.repeat(repeat=repeats, number=iters)
    return times


def pandana_compute(net: pnd.Network, orig: list, dest: list):
    return net.shortest_path_lengths(orig, dest)

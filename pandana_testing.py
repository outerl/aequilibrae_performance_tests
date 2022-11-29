import aequilibrae as ae
import pandana as pnd
import timeit


def pandana_init(graph: ae.Graph, cost: str):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    net = graph.network
    pnet = pnd.Network(net["link_id"], net["link_id"], net["a_node"], net["b_node"],
                       net[[cost]], twoway=False)

    return pnet, [o for o in graph.centroids for d in graph.centroids], [d for o in graph.centroids for d in graph.centroids]


def pandana_testing(net: pnd.Network, orig, dest, iters: int = 2, repeats: int = 5):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    timer = timeit.Timer(lambda: pandana_compute(net, orig, dest))
    times = timer.repeat(repeat=repeats, number=iters)
    return times


def pandana_compute(net: pnd.Network, orig: list, dest: list):
    return net.shortest_path_lengths(orig, dest)

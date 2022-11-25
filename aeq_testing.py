from aequilibrae.paths import NetworkSkimming
import timeit


def aequilibrae_compute_skim(graph):
    # And run the skimming
    skm = NetworkSkimming(graph)
    skm.execute()
    return skm.results.skims


def aequilibrae_init(graph, cost: str):
    """
    Prepare the graph for skimming the network for `cost`
    """
    graph.prepare_graph(graph.centroids)
    # let's say we want to minimize the cost
    graph.set_graph(cost)

    # And will skim the cost while we are at it
    graph.set_skimming(cost)

    # And we will allow paths to be compute going through other centroids/centroid connectors
    # required for the Sioux Falls network, as all nodes are centroids
    # BE CAREFUL WITH THIS SETTING
    graph.set_blocked_centroid_flows(False)
    return (graph,)


def aequilibrae_testing(graph, cost: str, iters: int = 2, repeats: int = 5):
    graph = aequilibrae_init(graph, cost)
    t = timeit.Timer(lambda: aequilibrae_compute_skim(graph))
    times = t.repeat(repeat=repeats, number=iters)
    return times

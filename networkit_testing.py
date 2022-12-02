import aequilibrae as ae
import networkit.graph as g
import networkit.distance as nk
import numpy as np
import timeit


def networkit_init(graph: ae.Graph, cost: str):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    # Setting up the compressed graph to be tested, assuming the graph exists
    graph.set_graph(cost)
    net = graph.compact_graph
    workit = g.Graph(weighted=True, directed=True)
    for i in list(zip(net["a_node"].tolist(), net["b_node"].tolist(), graph.compact_cost)):
        workit.addEdge(i[0], i[1], w=i[2], addMissing=True)
    return workit, graph.compact_nodes_to_indices[graph.centroids]


def networkit_testing(net: g.Graph, centroids):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    timer = timeit.Timer(lambda: networkit_compute(net, centroids))
    times = timer.repeat(repeat=repeats, number=iters)
    return times


def networkit_compute(net: g.Graph, centroids: list):
    """Computes centroids to centroids and returns skim"""
    # NOTE: Have to shift for the 0 node, alternatively could add a dummy node in
    results = np.empty((len(centroids), len(centroids)))
    for i in centroids:
        results[i] = nk.MultiTargetDijkstra(net, source=i, targets=centroids).run().getDistances()
    return results

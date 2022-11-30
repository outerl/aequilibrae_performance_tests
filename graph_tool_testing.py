#!/usr/bin/env python3
import warnings
try:
    import graph_tool.all as gt
except ModuleNotFoundError:
    warnings.warn('graph_tools module is not present', ImportWarning)

import numpy as np
import timeit


def graph_tool_compute_skim(graph, centroids, eweight):
    """
    Execute the skim using graph_tool.
    """
    results = np.empty((len(centroids), len(centroids)))
    for i in centroids:
        results[i] = gt.shortest_distance(graph, source=i, target=centroids, weights=eweight)
    return results


def graph_tool_init(graph, cost: str, cores: int = 0):
    """
    Prepare the aequilibrae graph for computation with graph_tool.
    """
    gt.openmp_set_num_threads(cores)
    print(cores)
    edges = graph.graph[["a_node", "b_node", "free_flow_time"]].itertuples(index=False, name=None)
    g = gt.Graph()
    eweight = g.new_edge_property("double")
    g.add_edge_list(edges, eprops=[eweight])
    return g, graph.nodes_to_indices[graph.centroids], eweight


def graph_tool_testing(graph, cost: str, cores: int = 0, iters: int = 2, repeats: int = 5):
    g, centroids, eweight = graph_tool_init(graph, cost, cores)
    t = timeit.Timer(lambda: graph_tool_compute_skim(g, centroids, eweight))
    times = t.repeat(repeat=repeats, number=iters)
    return times

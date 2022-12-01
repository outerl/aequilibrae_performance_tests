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


def graph_tool_init(graph, cost: str, cores: int = 1):
    """
    Prepare the aequilibrae graph for computation with graph_tool.
    """
    gt.openmp_set_num_threads(cores)
    edges = graph.compact_graph.loc[:, ("a_node", "b_node")]
    edges[cost] = graph.compact_cost[:-1]  # FIXME: as of writing, a partially fixed bug in aequilibrae causes graph.compact_cost
    # to contain an additional 0 at the end. This slicing avoids that.
    g = gt.Graph()
    eweight = g.new_edge_property("double")
    g.add_edge_list(edges.itertuples(index=False, name=None), eprops=[eweight])
    return g, graph.compact_nodes_to_indices[graph.centroids], eweight


def graph_tool_testing(graph, cost: str, cores: int = 0, iters: int = 2, repeats: int = 5):
    g, centroids, eweight = graph_tool_init(graph, cost, cores)
    t = timeit.Timer(lambda: graph_tool_compute_skim(g, centroids, eweight))
    times = t.repeat(repeat=repeats, number=iters)
    return times

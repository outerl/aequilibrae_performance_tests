import aequilibrae as ae
import networkit.graph as g
import networkit.distance as nk
import numpy as np
import plotly.express as px
import timeit
import warnings
import pandas as pd


def networkit_init(graph: ae.Graph, cost: str):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    #Setting up the compressed graph to be tested, assuming the graph exists
    graph.set_graph(cost)
    net = graph.compact_graph
    workit = g.Graph(weighted=True, directed=True)
    for i in list(zip(net["a_node"].tolist(), net["b_node"].tolist(), graph.compact_cost)):
        workit.addEdge(i[0], i[1], w=i[2], addMissing=True)
    return workit, graph.centroids


def networkit_testing(net: g.Graph, centroids):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    timer = timeit.Timer(lambda: networkit_compute(net, centroids))
    times = timer.repeat(repeat=repeats, number=iters)
    return times


def networkit_compute(net: g.Graph, centroids: list):
    """Only way to do centroid to all"""
    #NOTE: Have to shift for the 0 node, alternatively could add a dummy node in
    results = []
    for i in centroids:
        dist = nk.Dijkstra(net, i-1, storePaths=True).run()
        results.append(dist.getDistances(asarray=True))
    return np.array(results)

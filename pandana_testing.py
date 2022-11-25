import aequilibrae as ae
import pandana as pnd
import numpy as np
import plotly.express as px
import timeit
import warnings
import pandas as pd

def pandana_init(graph: ae.Graph, cost: str):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    net = graph.network
    pnet = pnd.Network(net["link_id"], net["link_id"], net["a_node"], net["b_node"],
                       net[[cost]], twoway=False)
    centroids = [o for o in graph.centroids for d in graph.centroids]
    return pnet, centroids

def pandana_testing(net: pnd.Network, centroids):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    timer = timeit.Timer(lambda: pandana_compute(net, centroids))
    times = timer.repeat(repeat=repeats, number=iters)
    return times

def pandana_compute(net: pnd.Network, centroids: list):
    return net.shortest_path_lengths(centroids, centroids)

   # net = graph.compact_graph
   # pnet = pnd.Network(net["link_id"], net["link_id"], net["a_node"], net["b_node"],
  #                     pd.DataFrame(graph.compact_cost), twoway=False)
  #  timer = timeit.Timer(lambda: pandana_pathes(pnet, centroids, centroids))
  #  times = timer.repeat(repeat=repeat, number=iterz)
  #  return timesz
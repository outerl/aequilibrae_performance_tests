import numpy as np
import timeit
import igraph as ig


def igraph_compute_skim(graph, centroids, weights):
    return np.array(graph.distances(source=centroids, target=centroids, weights=weights, mode="out"))


def igraph_init(graph, nodes, cost):
    # We get the graph
    # NOTE: These are 1-indexed, igraph uses 0-indexing. All names or indexs will be
    # one off
    # nodes = proj.network.nodes.data
    # ig's Graph.DataFrame method assumes the first 2 columns of the `edges` arg is
    # the sources and destination of the edge
    cols = graph.graph.columns.tolist()
    cols = [cols[1], cols[2], cols[0]] + cols[3:]
    edges = graph.graph[cols]

    # IDs in the graph need to be a sequence, so can't passing in a indexed version
    # of the graph otherwise igraph will generate a ton of empty vertexes
    g = ig.Graph.DataFrame(edges, directed=True, vertices=nodes, use_vids=True)

    g.es[cost] = edges[cost].tolist()

    centroids = graph.nodes_to_indices[graph.centroids]
    return g, centroids


def igraph_testing(graph, nodes, cost):
    g, centroids = igraph_init(graph, nodes, cost)
    t = timeit.Timer(lambda: igraph_compute_skim(g, centroids, cost))
    times = t.repeat(repeat=repeats, number=iters)
    return times

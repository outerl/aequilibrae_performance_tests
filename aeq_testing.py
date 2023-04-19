from aequilibrae import Project
from aequilibrae.paths import NetworkSkimming
import timeit


def aequilibrae_compute_skim(graph, cores):
    # And run the skimming
    skm = NetworkSkimming(graph)
    skm.results.set_cores(cores)
    skm.execute()
    return skm.results.skims


def aequilibrae_init(data):
    """
    Prepare the graph for skimming the network for `cost`
    """
    graph = data["graph"]
    cost = data["cost"]
    cores = data["cores"]
    graph.prepare_graph(graph.centroids)
    # let's say we want to minimize the cost
    graph.set_graph(cost)

    # And will skim the cost while we are at it
    graph.set_skimming(cost)

    # And we will allow paths to be compute going through other centroids/centroid connectors
    # required for the Sioux Falls network, as all nodes are centroids
    # BE CAREFUL WITH THIS SETTING
    graph.set_blocked_centroid_flows(False)
    return (graph, cores)


def aequilibrae_testing(graph, cost: str, iters: int = 2, repeats: int = 5):
    graph = aequilibrae_init(graph, cost)
    t = timeit.Timer(lambda: aequilibrae_compute_skim(graph))
    times = t.repeat(repeat=repeats, number=iters)
    return times


def aequilibrae_graph_creation_init(data):
    proj = Project()
    proj.open(data["proj_path"])
    return proj, data["cost"], "c"


def aequilibrae_graph_creation_build(proj, cost, modes):
    proj.network.build_graphs([cost], modes=modes)

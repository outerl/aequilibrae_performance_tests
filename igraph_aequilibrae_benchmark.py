#!/usr/bin/env python3
import igraph as ig
import numpy as np
import warnings
import timeit
from aequilibrae import Project
from aequilibrae.paths import NetworkSkimming


def igraph_compute_skim(graph, centroids, weights):
    return np.array(graph.distances(source=centroids,
                                    target=centroids,
                                    weights=weights,
                                    mode='out'))


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


def aequilibrae_compute(graph):
    # And run the skimming
    skm = NetworkSkimming(graph)
    skm.execute()
    return skm.results.skims


def aequilibrae_init(graph, cost):
    graph.prepare_graph(graph.centroids)
    # let's say we want to minimize the cost
    graph.set_graph(cost)

    # And will skim the cost while we are at it
    graph.set_skimming(cost)

    # And we will allow paths to be compute going through other centroids/centroid connectors
    # required for the Sioux Falls network, as all nodes are centroids
    # BE CAREFUL WITH THIS SETTING
    graph.set_blocked_centroid_flows(False)
    return graph


def aequilibrae_testing(graph, cost):
    graph = aequilibrae_init(graph, cost)
    t = timeit.Timer(lambda: aequilibrae_compute(graph))
    times = t.repeat(repeat=repeats, number=iters)
    return times


def project_init(project_name):
    proj_path = f'../models/{project_name}/'

    proj = Project()
    proj.open(proj_path)

    proj.network.build_graphs(['free_flow_time'], modes='c')
    graph = proj.network.graphs['c']
    return graph, proj.network.nodes.data


def validate(skim1, skim2, atol=1e-01):
    isclose = np.isclose(skim1, skim2, atol=atol)
    if isclose.all():
        return True
    else:
        loc = np.where(~isclose)
        for x, y in zip(*loc):
            print(f'{x}, {y}: {skim1[x, y]:.2f} != {skim2[x, y]:.2f}')
        print('[x, y: value1 != value2]')
        print(f'\nThe skims differ at {len(loc[0])} points')
        print(f'There are {len(np.unique(loc[0]))} unique x values',
              f'and {len(np.unique(loc[1]))} unique y values')
        print(f'The max absolute difference is {np.abs(skim1 - skim2).max()}')


if __name__ == '__main__':
    project_times = {'sioux_falls': {}, 'chicago_sketch': {}}

    iters = 2
    repeats = 5

    cost = 'free_flow_time'
    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action='ignore', category=FutureWarning)

        # Quickly test that both methods produce the same result. FIXME they don't...
        for project_name in project_times.keys():
            graph, nodes = project_init(project_name)

            aeq_skim = aequilibrae_compute(aequilibrae_init(graph, cost)).free_flow_time

            ig_skim = igraph_compute_skim(*igraph_init(graph, nodes, cost), cost)

            validate(aeq_skim, ig_skim)

        del graph
        del nodes

        # Benchmark time
        for project_name in project_times.keys():
            graph, nodes = project_init(project_name)

            print(f'Running aequilibrae on {project_name}...')
            project_times[project_name]['aequilibrae'] = aequilibrae_testing(graph, cost)
            print(f'Running igraph on {project_name}...')
            project_times[project_name]['igraph'] = igraph_testing(graph, nodes, cost)

        print('')
        for data, implemenations in project_times.items():
            print(data + ':')
            for name, times in implemenations.items():
                print(f'\t{name}:')
                for time in times:
                    print(f'\t\t\t{time}')
                print(f'\t\tAverage: {sum(times)/len(times)}')

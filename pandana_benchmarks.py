import aequilibrae as ae
import pandana as pnd
import numpy as np
import plotly.express as px
import timeit
import warnings
import pandas as pd

#Skimming for auequilibrae, pandana, times, save them for later
#Testing on 3 supplied databases
#Testing specifications
sample_size = 100
#with a z cause it's hip
iterz = 10
repeat = 5

project_times = {"sioux_falls": {}, "chicago_sketch": {}}


def pandana_bench(graph: ae.Graph):
    """
    Initialises the pandana network, executes each individual benchmark
    """
    #Make the pandana graph
    #The first two arguments are current passed as dummies, represent x,y coords which I believe only factor into the graphing aspect of the package
    #Note 5th argument must be a dataframe, not a series. We can parse multiple "impedences" into the network, but we have to specify one metric for path_finding
    results = {}
    net = graph.network
    pnet = pnd.Network(net["link_id"], net["link_id"], net["a_node"], net["b_node"],
                       net[["distance"]], twoway=False)
    #Test centroids: should be compared to the skim graph if I understand correctly
    #Assuming
    centroids = [o for o in graph.centroids for d in graph.centroids]
    #timer = timeit.Timer(lambda: pandana_centroid(pnet, centroids), lambda: print("skimmed"))
    #times = timer.repeat(repeat=repeat, number=iterz)
    #results["centroids"] = times

    #Pathfinding for pandana, run on the compressed graph created by aequilibrae
    net = graph.compact_graph
    pnet = pnd.Network(net["link_id"], net["link_id"], net["a_node"], net["b_node"],
                       pd.DataFrame(graph.compact_cost), twoway=False)
    timer = timeit.Timer(lambda: pandana_pathes(pnet,centroids, centroids))
    times = timer.repeat(repeat=repeat, number=iterz)
   # results["sample"] = times
    return times

def pandana_centroid(net: pnd.Network, centroids):
    """Tests the equivalent to the aequilibrae skim matrix,
    computes path for all centroids to all centroids, will output the length of each path in a (long) list"""
    #Initialising the actual arrays being parsed into shortest path
    net.shortest_path_lengths(centroids, centroids)

def pandana_pathes(net: pnd.Network, orig, dest):
    """Head to path speed comparison"""
    #Processing the random sample into the pandana approved form
    origs = [o for o in orig for d in orig]
    dests = [o for o in dest for d in dest]
    #Note there is an equivalent feature which can return the node pathes instead of the distance,
    # but not links directly
    net.shortest_paths(origs, dests)


def aequilibrae_bench(graph: ae.Graph):
    """Sets up the state needed to execute centroid and path finding tests"""
    #results = {}
    #Setting up the skim
    res = ae.PathResults()
    graph.set_graph("distance")
    graph.set_skimming("distance")
    res.prepare(graph)

    timer = timeit.Timer(lambda: aequilibrae_skim(graph), lambda: print("skimmed"))
    times = timer.repeat(repeat=repeat, number=iterz)
    #results["centroids"] = times

    #Extract compressed graph for computation


    return times

def aequilibrae_skim(graph: ae.Graph):
    """Skimming benchmark"""
    skm = ae.NetworkSkimming(graph)
    skm.execute()

def aequilibrae_path(graph: ae.Graph):
    pass



if __name__ == "__main__":
    with warnings.catch_warnings():
        #Warnings catch from Jake, he's my hero these readouts are awful
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action='ignore', category=FutureWarning)
        for project_name in project_times.keys():
            proj_path = f'../models/{project_name}/'
            #Create the project
            proj = ae.Project()
            proj.open(proj_path)

            #Building for car networks
            proj.network.build_graphs(modes=["c"])
            graph = proj.network.graphs["c"]

            #Random sample from graph being tested for pathfinding
          #  orig = graph.all_nodes[np.random.choice(len(graph.all_nodes) - 1, size=sample_size)]
           # dest = graph.all_nodes[np.random.choice(len(graph.all_nodes) - 1, size=sample_size)]
            print(f"Running aequilibrae on {project_name}...")
            project_times[project_name]["aequilibrae"] = aequilibrae_bench(graph)
            print(f"Running pandana on {project_name}...")
            project_times[project_name]["pandana"] = pandana_bench(graph)

            print(f"Path finding from centroids to centroids,",
                  f"{iterz} iterations repeated {repeat} times. (seconds)")
            for data, implemenations in project_times.items():
                print(data + ":")
                for name, times in implemenations.items():
                    print(f"\t{name}:")
                    for time in times:
                        print(f"\t\t\t{time}")
                    print(f"\t\tAverage: {sum(times) / len(times)}")




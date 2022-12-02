#!/usr/bin/env python3
from pathlib import Path
from socket import gethostname
from argparse import ArgumentParser
import sys
import timeit
import pandas as pd
import warnings

sys.path.append(str(Path(__file__).resolve().parent))
from project_utils import project_init
from pandana_testing import pandana_init, pandana_compute
from aeq_testing import aequilibrae_init, aequilibrae_compute_skim
from igraph_testing import igraph_init, igraph_compute_skim
from networkit_testing import networkit_init, networkit_compute
from graph_tool_testing import graph_tool_init, graph_tool_compute_skim
from plot_results import benchmark_chart, aeq_ratios

def run_bench(algo, project_name, init, func, data, iters: int = 2, repeats: int = 5):
    stuff = init(*data)
    t = timeit.Timer(lambda: func(*stuff))
    df = pd.DataFrame({"runtime": t.repeat(repeat=repeats, number=iters)})
    df["library"] = algo
    df["project_name"] = project_name
    df["computer"] = gethostname()
    return df


def main():
    projects = ["sioux_falls", "chicago_sketch"]
    cost = "free_flow_time"
    #List for ratios chart
    num_links = []
    libraries = ["aequilibrae", "igraph", "pandana", "networkit", "graph-tool"]

    parser = ArgumentParser()
    parser.add_argument("-m", "--model-path", dest="path", default='../models',
                        help="path to models", metavar="FILE")
    parser.add_argument("-i", "--iterations", dest="iters", default=2, type=int,
                        help="number of times to run each library per sample", metavar="X")
    parser.add_argument("-r", "--repeats", dest="repeats", default=5, type=int,
                        help="number of samples", metavar="Y")
    parser.add_argument("-c", "--cores", dest="cores", default=0, type=int,
                        help="number of cores to use. Use 0 for all cores.", metavar="N")
    parser.add_argument("-l", "--libraries", nargs='+', dest="libraries",
                        choices=libraries,
                        default=libraries,
                        help="libraries to benchmark")
    parser.add_argument("-p", "--projects", nargs='+', dest="projects",
                        choices=projects,
                        default=projects,
                        help="projects to benchmark using")

    args = vars(parser.parse_args())

    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)

        # Benchmark time
        results = []
        for project_name in args["projects"]:
            graph, nodes, geo = project_init(f"{args['path']}/{project_name}")
            num_links.append(graph.num_links)
            if "aequilibrae" in args["libraries"]:
                print(f"Running aequilibrae on {project_name}...")
                results.append(run_bench("aeq", project_name, aequilibrae_init,
                                         aequilibrae_compute_skim,
                                         (graph, cost, args["cores"])))

            if "igraph" in args["libraries"]:
                print(f'Running igraph on {project_name}...')
                results.append(run_bench("igraph", project_name, igraph_init,
                                         igraph_compute_skim,
                                         (graph, cost)))

            if "pandana" in args["libraries"]:
                print(f"Running pandana on {project_name}...")
                results.append(run_bench("pandana", project_name, pandana_init,
                                         pandana_compute,
                                         (graph, cost, geo)))

            if "networkit" in args["libraries"]:
                print(f"Running Networkit on {project_name}...")
                results.append(run_bench("networkit", project_name, networkit_init,
                                         networkit_compute,
                                         (graph, cost)))

            if "graph-tool" in args["libraries"] and "graph_tool" in sys.modules:
                print(f"Running graph-tool on {project_name}...")
                results.append(run_bench("graph-tool", project_name, graph_tool_init,
                                         graph_tool_compute_skim,
                                         (graph, cost, args["cores"])))

            print("-" * 30)

        results = pd.concat(results)
        summary = results.groupby(["project_name", "library"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        )
        print(summary)
        benchmark_chart(summary, projects, libraries).show()
        aeq_ratios(summary, projects, num_links, "igraph").show()


if __name__ == "__main__":
    main()

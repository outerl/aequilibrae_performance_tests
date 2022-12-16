#!/usr/bin/env python3
from pathlib import Path
from socket import gethostname
from argparse import ArgumentParser
from datetime import datetime
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
try:
    from plot_results import benchmark_chart, aeq_ratios
except ModuleNotFoundError:
    warnings.warn('plotting is not possible', ImportWarning)


def run_bench(lib, project_name, init, func, data):
    print(f"Running {lib} on {project_name} with {data['cores']} core(s)...")
    stuff = init(data)
    t = timeit.Timer(lambda: func(*stuff))
    df = pd.DataFrame({"runtime": [x / data["iters"] for x in t.repeat(repeat=data["repeats"], number=data["iters"])]})
    df["library"] = lib
    df["project_name"] = project_name
    df["cores"] = data['cores']
    df["computer"] = gethostname()
    if data["details"]:
        df["details"] = data["details"]
    return df


def main():
    projects = ["sioux_falls", "chicago_sketch"]
    libraries = ["aequilibrae", "igraph", "pandana", "networkit", "graph-tool"]

    parser = ArgumentParser()
    parser.add_argument("-m", "--model-path", dest="path", default='../models',
                        help="path to models", metavar="FILE")
    parser.add_argument("-o", "--output-path", dest="output", default='./Images',
                        help="where to place output data and images", metavar="FILE")
    parser.add_argument("-i", "--iterations", dest="iters", default=2, type=int,
                        help="number of times to run each library per sample", metavar="X")
    parser.add_argument("-r", "--repeats", dest="repeats", default=5, type=int,
                        help="number of samples", metavar="Y")
    parser.add_argument("-c", "--cores", nargs="+", dest="cores", default=0,
                        help="number of cores to use. Use 0 for all cores.",
                        type=int, metavar="N")
    parser.add_argument("-l", "--libraries", nargs='+', dest="libraries",
                        choices=libraries, default=libraries,
                        help="libraries to benchmark")
    parser.add_argument("-p", "--projects", nargs='+', dest="projects",
                        default=projects, help="projects to benchmark using")
    parser.add_argument("--cost", dest="cost", default='free_flow_time',
                        help="cost column to skim for")
    parser.add_argument('--no-plots', dest='plots', action='store_false')
    parser.add_argument('--plots', dest='plots', action='store_true')
    parser.add_argument('--details', dest='details')
    parser.set_defaults(feature=True)

    args = vars(parser.parse_args())

    libraries = args['libraries']
    output_path = args["output"]
    cores = args["cores"]
    print(f"Now benchmarking {libraries} on the {args['projects']} model(s).")
    print(f"Running with {args['iters']} iterations, {args['repeats']}",
          f"times, for a total of {args['iters'] * args['repeats']} samples.")
    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)

        # Benchmark time
        results = []
        proj_series = []
        for project_name in args["projects"]:
            args["graph"], args["nodes"], args["geo"] = project_init(f"{args['path']}/{project_name}", args["cost"])
            proj_series.append(pd.DataFrame({
                "num_links": [args["graph"].compact_num_links],
                "num_nodes": [args["graph"].compact_num_nodes],
                "num_zones": [args["graph"].num_zones],
                "num_centroids": [len(args["graph"].centroids)]
            }, index=[project_name]))

            for core_count in (range(cores[0], cores[1] + 1) if len(cores) == 2 else cores):
                args["cores"] = core_count

                if "aequilibrae" in libraries:
                    results.append(run_bench("aequilibrae", project_name, aequilibrae_init,
                                             aequilibrae_compute_skim, args))

                if "igraph" in libraries:
                    results.append(run_bench("igraph", project_name, igraph_init,
                                             igraph_compute_skim, args))

                if "pandana" in libraries:
                    results.append(run_bench("pandana", project_name, pandana_init,
                                             pandana_compute, args))

                if "networkit" in libraries:
                    results.append(run_bench("networkit", project_name, networkit_init,
                                             networkit_compute, args))

                if "graph-tool" in libraries and "graph_tool" in sys.modules:
                    results.append(run_bench("graph-tool", project_name, graph_tool_init,
                                             graph_tool_compute_skim, args))

                print("-" * 30)

        proj_summary = pd.concat(proj_series)
        results = pd.concat(results)
        summary = results.groupby(["project_name", "library", "cores"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        )
        print(summary)
        results.to_csv(f"{output_path}/{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}_table.csv")
        proj_summary.to_csv(f"{output_path}/project summary.csv")


if __name__ == "__main__":
    main()

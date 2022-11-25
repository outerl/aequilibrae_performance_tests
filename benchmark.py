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


def run_bench(algo, project_name, init, func, graph, cost, iters: int = 2, repeats: int = 5):
    stuff = init(graph, cost)
    t = timeit.Timer(lambda: func(*stuff))
    df = pd.DataFrame({"runtime": t.repeat(repeat=repeats, number=iters)})
    df["algorithm"] = algo
    df["project_name"] = project_name
    df["computer"] = gethostname()
    return df


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--models", dest="path", default='../models',
                        help="path to models", metavar="FILE")

    args = vars(parser.parse_args())

    projects = ["sioux_falls"]
    cost = "free_flow_time"

    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)

        # Benchmark time
        results = []
        for project_name in projects:
            graph, nodes = project_init(f"{args['path']}/{project_name}")

            print(f"Running aequilibrae on {project_name}...")
            results.append(run_bench("aeq", project_name, aequilibrae_init, aequilibrae_compute_skim, graph, cost))

            print(f'Running igraph on {project_name}...')
            results.append(run_bench("igraph", project_name, igraph_init, igraph_compute_skim, graph, cost))

            print(f"Running pandana on {project_name}...")
            results.append(run_bench("pandana", project_name, pandana_init, pandana_compute, graph, cost))

        results = pd.concat(results)
        summary = results.groupby(["project_name", "algorithm"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        )
        print(summary)


if __name__ == "__main__":
    main()

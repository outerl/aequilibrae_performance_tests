#!/usr/bin/env python3
from pathlib import Path
from socket import gethostname
import sys
import timeit
import numpy as np
import pandas as pd
import warnings

sys.path.append(str(Path(__file__).resolve().parent))
from project_utils import project_init
from aeq_testing import aequilibrae_init, aequilibrae_compute

iters = 2
repeats = 5


def run_bench(algo, project_name, init, main, graph, cost):
    stuff = init(graph, cost)
    t = timeit.Timer(lambda: main(*stuff))
    df = pd.DataFrame({"runtime": t.repeat(repeat=repeats, number=iters)})
    df["algorithm"] = algo
    df["project_name"] = project_name
    df["computer"] = gethostname()
    return df


if __name__ == "__main__":
    projects = ["sioux_falls"]
    cost = "free_flow_time"

    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)

        # Benchmark time
        results = []
        for project_name in projects:
            graph, nodes = project_init(project_name)

            print(f"Running aequilibrae on {project_name}...")

            results.append(run_bench("aeq", project_name, aequilibrae_init, aequilibrae_compute, graph, cost))
            # print(f'Running igraph on {project_name}...')
            # project_times[project_name]['igraph'] = igraph_testing(graph, nodes, cost)

        results = pd.concat(results)
        summary = results.groupby(["project_name", "algorithm"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        )
        print(summary)

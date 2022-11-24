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
from aeq import aequilibrae_testing

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
            # graph, nodes = project_init(project_name)
            graph = None

            print(f"Running aequilibrae on {project_name}...")

            def aeq_init(x, y):
                return (1, 2, 3)

            def aeq_run(x, y, z):
                w = (x + y + z)

            results.append(run_bench("aeq", project_name, aeq_init, aeq_run, graph, cost))
            results.append(run_bench("aeq", project_name, aeq_init, aeq_run, graph, cost))
            # print(f'Running igraph on {project_name}...')
            # project_times[project_name]['igraph'] = igraph_testing(graph, nodes, cost)

        results = pd.concat(results)
        summary = results.groupby(["project_name", "algorithm"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        )
        print(summary)

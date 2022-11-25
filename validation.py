#!/usr/bin/env python3
import numpy as np
from argparse import ArgumentParser
import warnings

from project_utils import project_init
from aeq_testing import aequilibrae_init, aequilibrae_compute_skim
from igraph_testing import igraph_init, igraph_compute_skim


def validate(skim1, skim2, atol: float = 1e-01):
    """
    Detect discrepencies in the provided skims with a tolerance. Prints the
    relevant locations, number of unique values, and max absolute difference.
    """
    isclose = np.isclose(skim1, skim2, atol=atol)
    if isclose.all():
        return True
    else:
        loc = np.where(~isclose)
        for x, y in zip(*loc):
            print(f"{x}, {y}: {skim1[x, y]:.2f} != {skim2[x, y]:.2f}")
        print("[x, y: value1 != value2]")
        print(f"\nThe skims differ at {len(loc[0])} points")
        print(f"There are {len(np.unique(loc[0]))} unique x values", f"and {len(np.unique(loc[1]))} unique y values")
        print(f"The max absolute difference is {np.abs(skim1 - skim2).max()}\n\n")
        return False


def validate_all_projects(proj_path: str, projects: str, cost: str, cores: int = 1):
    # Quickly test that both methods produce the same result. FIXME they don't...
    result = True
    for project_name in projects:
        print(f"Testing {project_name}")

        graph, nodes = project_init(f"{proj_path}/{project_name}")

        aeq_skim = aequilibrae_compute_skim(*aequilibrae_init(graph, cost)).get_matrix(cost)
        ig_skim = igraph_compute_skim(*igraph_init(graph, cost))

        if not validate(aeq_skim, ig_skim):
            result = False
    return result


def main():
    projects = ["sioux_falls", "chicago_sketch"]
    cost = "free_flow_time"

    parser = ArgumentParser()
    parser.add_argument("-m", "--model-path", dest="path", default='../models',
                        help="path to models", metavar="FILE")

    args = vars(parser.parse_args())

    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)
        return validate_all_projects(args["path"], projects, cost)


if __name__ == "__main__":
    main()

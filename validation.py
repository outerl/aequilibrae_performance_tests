#!/usr/bin/env python3
import numpy as np
from argparse import ArgumentParser
import warnings
import sys
from typing import List

from project_utils import project_init
from aeq_testing import aequilibrae_init, aequilibrae_compute_skim
from igraph_testing import igraph_init, igraph_compute_skim
from pandana_testing import pandana_init, pandana_compute
from networkit_testing import networkit_init, networkit_compute
from graph_tool_testing import graph_tool_init, graph_tool_compute_skim


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


def validate_projects(proj_path: str, projects: str, libraries: List[str], args):
    result = True
    for project_name in projects:
        print(f"Testing {project_name}")

        args["graph"], args["nodes"], args["geo"] = project_init(f"{args['path']}/{project_name}", args["cost"])
        args["cores"] = 0

        skims = []  # NOTE: the first element is used as the reference model

        for library in libraries:
            if "aequilibrae" == library:
                print(f"Running aequilibrae on {project_name}...")
                skims.append(aequilibrae_compute_skim(*aequilibrae_init(args)).get_matrix(args["cost"]))
            elif "igraph" == library:
                print(f'Running igraph on {project_name}...')
                skims.append(igraph_compute_skim(*igraph_init(args)))
            elif "pandana" == library:
                print(f"Running pandana on {project_name}...")
                a = np.array(pandana_compute(*pandana_init(args)))
                a_len = max(a.shape)
                a_len_sqrt = int(np.sqrt(a_len))
                skims.append(a.reshape((a_len_sqrt, a_len_sqrt)))
            elif "networkit" == library:
                print(f"Running Networkit on {project_name}...")
                skims.append(networkit_compute(*networkit_init(args)))
            elif "graph-tool" == library and "graph_tool" in sys.modules:
                print(f"Running graph-tool on {project_name}...")
                skims.append(graph_tool_compute_skim(*graph_tool_init(args)))

        print("")
        for skim, library in list(zip(skims, libraries))[1:]:
            if not validate(skims[0], skim):
                print(f"{library} differs from {libraries[0]}")
                result = False
            else:
                print(f"{library} matches {libraries[0]}")
        print("-" * 30)
    return result


def main():
    projects = ["sioux_falls", "chicago_sketch"]
    libraries = ["aequilibrae", "igraph", "pandana", "networkit", "graph-tool"]

    parser = ArgumentParser()
    parser.add_argument("-m", "--model-path", dest="path", default='../models',
                        help="path to models", metavar="FILE")
    parser.add_argument("-l", "--libraries", nargs='+', dest="libraries",
                        choices=libraries,
                        default=libraries,
                        help="libraries to validate, the first one is used as the reference")
    parser.add_argument("--cost", dest="cost", default='free_flow_time',
                        help="cost column to skim for")
    parser.add_argument("-p", "--projects", nargs='+', dest="projects",
                        default=projects,
                        help="projects to benchmark using")

    args = vars(parser.parse_args())

    with warnings.catch_warnings():
        # pandas future warnings are really annoying FIXME
        warnings.simplefilter(action="ignore", category=FutureWarning)
        if validate_projects(args["path"], args["projects"], args["libraries"], args):
            print("All models validated")
            return True
        else:
            return False


if __name__ == "__main__":
    main()

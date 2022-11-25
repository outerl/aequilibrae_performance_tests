import numpy as np
import numpy.typing as npt
from project_utils import project_init

from aeq_testing import aequilibrae_init, aequilibrae_compute_skim
from igraph_testing import igraph_init, igraph_compute_skim


def validate(skim1: npt.ArrayLike, skim2: npt.ArrayLike, atol: float = 1e-01):
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
        print(f"The max absolute difference is {np.abs(skim1 - skim2).max()}")


def validate_all_projects(proj_path: str, projects: str, cost: str):
    # Quickly test that both methods produce the same result. FIXME they don't...
    for project_name in projects:
        graph, nodes = project_init(f"{proj_path}/{project_name}")

        aeq_skim = aequilibrae_compute_skim(aequilibrae_init(graph, cost))[cost]
        ig_skim = igraph_compute_skim(*igraph_init(graph, nodes, cost), cost)
        validate(aeq_skim, ig_skim)

from aequilibrae import Project
import numpy as np


def project_init(proj_path: str, cost: str = "free_flow_time", modes: str = "c"):
    """
    Opens a aequilibrae project from `proj_path`. Builds to
    relevant graph and return the graph and nodes.
    """
    proj = Project()
    proj.open(proj_path)
    curr = proj.conn.cursor()
    curr.execute("select st_x(geometry), st_y(geometry) from nodes")
    geo = np.array(curr.fetchall())

    proj.network.build_graphs([cost], modes=modes)
    graph = proj.network.graphs["c"]
    return graph, proj.network.nodes.data, geo

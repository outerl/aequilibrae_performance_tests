from aequilibrae import Project


def project_init(proj_path: str, cost: str = "free_flow_time", modes: str = "c"):
    """
    Opens a aequilibrae project from `proj_path`. Builds to
    relevant graph and return the graph and nodes.
    """
    proj = Project()
    proj.open(proj_path)

    proj.network.build_graphs([cost], modes=modes)
    graph = proj.network.graphs["c"]
    return graph, proj.network.nodes.data

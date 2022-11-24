from aequilibrae import Project

def project_init(project_name):
    proj_path = f"../models/{project_name}/"

    proj = Project()
    proj.open(proj_path)

    proj.network.build_graphs(["free_flow_time"], modes="c")
    graph = proj.network.graphs["c"]
    return graph, proj.network.nodes.data


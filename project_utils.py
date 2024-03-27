from aequilibrae import Project
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import json

from aequilibrae.matrix import AequilibraeMatrix
from aequilibrae.paths.route_choice import RouteChoice


def project_init(proj_path: str, cost, modes: str = "c"):
    """
    Opens a aequilibrae project from `proj_path`. Builds to
    relevant graph and return the graph and nodes.
    """
    proj = Project()
    proj.open(proj_path)
    # curr = proj.conn.cursor()
    # curr.execute("select st_x(geometry), st_y(geometry) from nodes")
    # geo = np.array(curr.fetchall())

    proj.network.build_graphs([cost], modes=modes)
    graph = proj.network.graphs["c"]
    return graph, proj.network.nodes.data, None  # geo


def qfm_project_init(data):

    details = json.loads(data["details"])

    sys.path.append(details["qfm_path"])

    from qfm.preprocessing.skim_builder import SkimBuilder

    base_dir = Path(
        details["submodels_path"]
    )
    project_dir = base_dir / "00_basic_scenario"

    zones = gpd.read_parquet(project_dir / "zone_system" / "zones.parquet")
    centroids = gpd.read_parquet(
        project_dir / "zone_system" / "centroids.parquet"
    ).set_crs(4326)

    net = (
        gpd.read_parquet(project_dir / "network" / "new_network.parquet")
        .rename(columns={"geometry": "geom"})
        .set_geometry("geom")
    )
    net_nodes = (
        gpd.read_parquet(project_dir / "network" / "nodes_modified.parquet")
        .rename(columns={"geometry": "geom"})
        .set_geometry("geom")
        .set_crs(4326)
    )

    skimmer = SkimBuilder()
    skimmer.from_layers(
        network=net, zones=zones, network_nodes=net_nodes, centroids=centroids
    )

    graph = skimmer.graph

    sample_trips = pd.read_csv(base_dir / "b_03_Regional_assignment" / "compass_paths" / "estimation_choice_sets" / "extra_trips.csv")
    link_results = pd.read_csv(base_dir / "b_03_Regional_assignment" / "compass_paths" / "link_results.csv")
    link_results["links"] = link_results["links"].astype(int)
    sample_trips["trip index"] = sample_trips.index

    gb = link_results.groupby(by="trip_id")
    gb = pd.concat((gb.get_group(x) for x in sample_trips.trip_id)).groupby(by="trip_id")

    nodes = []
    for i, row in sample_trips.iterrows():
        links = gb.get_group(row.trip_id)
        a = graph.network[(graph.network.link_id == abs(links.links.values[0]))]
        a = a.a_node.values[0] if links.links.values[0] > 0 else a.b_node.values[0]

        b = graph.network[(graph.network.link_id == abs(links.links.values[-1]))]
        b = b.a_node.values[0] if links.links.values[-1] > 0 else b.b_node.values[0]
        nodes.append((a, b))

    mat = AequilibraeMatrix()
    mat.create_empty(
        memory_only=True,
        zones=graph.num_zones,
        matrix_names=["test"],
    )
    mat.index = graph.centroids[:]
    mat.computational_view()
    mat.matrix_view[:, :] = np.full((graph.num_zones, graph.num_zones), 1.0)

    graph.prepare_graph(np.unique(nodes))

    rc = RouteChoice(graph, mat)
    graph.create_compressed_link_network_mapping()

    rc.set_choice_set_generation(**details["parameters"])
    rc.set_cores(data["cores"])
    rc.prepare(nodes)

    return (rc,)

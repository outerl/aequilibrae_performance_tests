def validate(skim1, skim2, atol=1e-01):
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


def validate_all_projects(projects):
    # Quickly test that both methods produce the same result. FIXME they don't...
    for project_name in projects:
        graph, nodes = project_init(project_name)

        aeq_skim = aequilibrae_compute(aequilibrae_init(graph, cost)).free_flow_time
        ig_skim = igraph_compute_skim(*igraph_init(graph, nodes, cost), cost)
        validate(aeq_skim, ig_skim)

    del graph
    del nodes


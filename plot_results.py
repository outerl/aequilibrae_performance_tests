from plotly.subplots import make_subplots
from math import ceil
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

def benchmark_chart(summary: pd.DataFrame, projects: list, libraries: list) -> go.Figure:
    fig = make_subplots(rows=ceil(len(projects)/2), cols=2, subplot_titles=projects)
    row, col = 1, 1
    color_dict = {}
    #TODO: Make this less janky, scalable to 4+ algos
    color = ["#f00202", "#020af0", "#00d9ff",]# "fuschia"]
    for i, j in enumerate(libraries):
        color_dict[j] = color[i]

    for proj in projects:
        results = summary.loc[proj]
        trace = go.Bar(x=libraries, y=results["average"], marker_color=color)
        fig.add_trace(trace, row=row, col=col)
        if col == 2:
            col = 1
            row += 1
        else:
            col += 1

    for i in range(0, len(projects)):
        axis = 'yaxis' + str(i+1) if i != 0 else 'yaxis'
        fig['layout'][axis]['title'] = 'Average Runtime in Seconds'
    return fig

def aeq_ratios(summary: pd.DataFrame, projects: list, proj_links: list, comparison: str, target = "aeq") -> go.Figure:
    """

    :param summary: Benchmark results
    :param projects: List of projects run
    :param proj_links: Number of links in each project
    :param comparison: Package results being compared to
    :param target: Package whose performance is being tested, aequilibrae by default
    :return: go.Figure, a plot of the ratio for the target package by the number of links in each network
    """
    #ratio of performance between aeq and a designated library (comparison), based on the size of the network (num edges).
    ratios = []
    for proj in projects:
        ratios.append(summary.loc[(proj, target)]["average"]/summary.loc[(proj, comparison)]["average"])
    return px.scatter(x=proj_links, y=ratios, labels={"x": "Number of Links", "y": "Ratio of Execution Time"}, title="Perfomance ratio for skimming between " +target+" and "+comparison)

    pass

from plotly.subplots import make_subplots
from math import ceil
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
NUM_COLS=2

def benchmark_chart(summary: pd.DataFrame, projects: list, libraries: list) -> go.Figure:
    fig = make_subplots(rows=ceil(len(projects)/2), cols=NUM_COLS, subplot_titles=projects)
    row, col = 1, 1
    color_dict = {}
    #TODO: Make this less janky, scalable to 4+ algos
    color = ["#f00202", "#020af0", "#00d9ff", "#9d00ff", "#ff0084", ]
    for i, j in enumerate(libraries):
        color_dict[j] = color[i]

    for proj in projects:
        results = summary.loc[proj]
        trace = go.Bar(x=libraries, y=results["min"], marker_color=color, showlegend=False)
        fig.add_trace(trace, row=row, col=col)
        if col == 2:
            col = 1
            row += 1
        else:
            col += 1

    for i in range(0, len(projects)):
        axis = 'yaxis' + str(i+1) if i != 0 else 'yaxis'
        if i % NUM_COLS == 0:
            fig['layout'][axis]['title'] = 'Minimum Runtime in Seconds'
        fig.update_layout(title={'text': "Minimum Runtime of each Library",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
            font=dict(
                family="Courier New, monospace",
                size=16,)
            )
    return fig

#TODO: Replace lists with a second dataframe for project info
def aeq_ratios(summary: pd.DataFrame, projects: pd.DataFrame, comparison: str, algorithms: list) -> go.Figure:
    """

    :param summary: Benchmark results
    :param projects: List of projects run
    :param proj_links: Number of links in each project
    :param comparison: Package results being compared to
    :param target: Package whose performance is being tested, aequilibrae by default
    :return: go.Figure, a plot of the ratio for the target package by the number of links in each network
    """
    #ratio of performance between aeq and a designated library (comparison), based on the size of the network (num edges).

    algorithms.remove(comparison)
    fig = go.Figure()
    #Iterate through each algorithm, then for each project compute the ratio
    for alg in algorithms:
        ratios = []
        for proj, _ in projects.iterrows():
            ratios.append(summary.loc[(proj, comparison)]["min"]/summary.loc[(proj, alg)]["min"])
        trace = go.Scatter(x=projects["num_links"], y=ratios, mode="markers", name=alg)
        fig.add_trace(trace)
        #Aesthetics
    fig.update_layout(title={
        'text': "Perfomance ratio between tested packages and "+comparison,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
          xaxis_title="Number of Links in Project",
          yaxis_title="Ratio of performance",
          legend_title="Algorithms",
          font=dict(
                family="Courier New, monospace",
                size=12,)
            )
    return fig

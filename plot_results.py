from plotly.subplots import make_subplots
from math import ceil
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
NUM_COLS=3

def benchmark_chart(summary: pd.DataFrame, projects: list, libraries: list, subplot_titles =None) -> go.Figure:
    #fig = make_subplots(rows=ceil(len(projects)/2), cols=NUM_COLS, subplot_titles=projects)
    fig = make_subplots(rows=1, cols=3, subplot_titles=subplot_titles if subplot_titles is not None else projects)
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
        col+=1

    for i in range(0, len(projects)):
        axis = 'yaxis' + str(i+1) if i != 0 else 'yaxis'
        if i % NUM_COLS == 0:
            fig['layout'][axis]['title'] = 'Seconds'
        fig.update_layout(title={'text': "Minimum Runtime",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
            font=dict(
                family="Arial",
                size=16,
            ),paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
    return fig

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

    fig = go.Figure()
    #Iterate through each algorithm, then for each project compute the ratio
    for alg in algorithms:
        ratios = []
        for proj, _ in projects.iterrows():
            ratios.append(summary.loc[(proj, alg)]["min"]/summary.loc[(proj, comparison)]["min"])
        trace = go.Scatter(x=projects["num_links"], y=ratios, name=alg)
        fig.add_trace(trace)
        #Aesthetics
    fig.update_layout(title={
        'text': "Perfomance ratio between " +comparison + " and tested packages" ,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
          xaxis_title="Number of Links in Project",
          yaxis_title="Ratio of performance",
          legend_title="Algorithms",
          font=dict(
                family="Arial",
                size=16,),
          paper_bgcolor='rgba(0,0,0,0)',
          plot_bgcolor='rgba(0,0,0,0)'
            )
    return fig

def time_plot(summary: pd.DataFrame, projects: pd.DataFrame, algorithms: list) -> go.Figure:
    """

    :param summary: Benchmark results
    :param projects: List of projects run
    :param proj_links: Number of links in each project
    :param comparison: Package results being compared to
    :param target: Package whose performance is being tested, aequilibrae by default
    :return: go.Figure, a plot of the ratio for the target package by the number of links in each network
    """
    #ratio of performance between aeq and a designated library (comparison), based on the size of the network (num edges).
    fig = go.Figure()
    for alg in algorithms:
        ratios = []
        for proj, _ in projects.iterrows():
            ratios.append(summary.loc[(proj, alg)]["min"])
        trace = go.Scatter(x=projects["num_links"], y=ratios, name=alg)
        fig.add_trace(trace)
    #Iterate through each algorithm, then for each project compute the ratio
        #Aesthetics
    fig.update_layout(title={
        'text': "Minimum Runtime of Each Algorithm ",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
          xaxis_title="Number of Compressed Links in Project",
          yaxis_title="Minimum Runtime",
          legend_title="Algorithms",
          font=dict(
                family="Arial",
                size=16,),
          paper_bgcolor='rgba(0,0,0,0)',
          plot_bgcolor='rgba(0,0,0,0)'
            )
    return fig


def normalised_time_plot(summary: pd.DataFrame, projects: pd.DataFrame, algorithms: list) -> go.Figure:
    """

    :param summary: Benchmark results
    :param projects: List of projects run
    :param proj_links: Number of links in each project
    :param comparison: Package results being compared to
    :param target: Package whose performance is being tested, aequilibrae by default
    :return: go.Figure, a plot of the ratio for the target package by the number of links in each network
    """
    #ratio of performance between aeq and a designated library (comparison), based on the size of the network (num edges).
    fig = go.Figure()
    for alg in algorithms:
        ratios = []
        for proj, _ in projects.iterrows():
            ratios.append((proj, (summary.loc[(proj, alg)]["min"]/projects.loc[proj, "num_centroids"])*1000))
        #trace = go.Scatter(x=projects["num_links"], y=ratios, name=alg)
        #fig.add_trace(trace)
    #Iterate through each algorithm, then for each project compute the ratio
        #Aesthetics
        print("library: ", alg, "ratio: ", ratios)
    fig.update_layout(title={
        'text': "Minimum Runtime per 1000 Origins",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
          xaxis_title="Number of Edges in Graph",
          yaxis_title="Seconds",
          legend_title="Algorithms",
        font=dict(family="Arial", size=18,),
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
            )
    return fig

from plotly.subplots import make_subplots
from math import ceil
import plotly.graph_objects as go
import pandas as pd

def benchmark_chart(summary: pd.DataFrame, projects: list, libraries: list) -> go.Figure:
    fig = make_subplots(rows=ceil(len(projects)/2), cols=2, subplot_titles=projects)
    row, col = 1, 1
    color_dict = {}
    #TODO: Make this less janky, scalable to 4+ algos
    color = ["firebrick", "blue", "cyan",]# "fuschia"]
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

def aeq_ratios(summary: pd.DataFrame, projects: list, libraries: list) -> go.Figure:

    pass

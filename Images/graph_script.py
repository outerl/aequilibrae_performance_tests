import pandas as pd
import plotly.graph_objects as go
import math
import sqlite3 as sq

def normalised_time_plot(summary: pd.DataFrame, projects: pd.DataFrame, normalised=True) -> go.Figure:
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
    projs = list(set(summary.index.get_level_values("project_name")))
    projs.sort(key=lambda x: projects.loc[x, "num_links"])
    print(projs)
    for alg in set(summary.index.get_level_values("details")):
        norm_time = []
        for proj in projs:
            try:
                #print(proj)
                norm_time.append((summary.loc[(proj, alg)]["min"] / projects.loc[proj, "num_centroids"]) * 1000) \
                    if normalised else norm_time.append(summary.loc[(proj, alg)]["min"])
                #print(alg, proj, norm_time[-1])
            except:
                #print(proj, " failed")
                pass
        trace = go.Scatter(x=projects["num_links"], y=norm_time, name=alg)
        fig.add_trace(trace)
    #Iterate through each algorithm, then for each project compute the ratio
        #Aesthetics
        #print("library: ", alg, ", ratio: ", norm_time)
    fig.update_layout(title={
        'text': "Minimum Runtime per 1000 Origins" if normalised else "Minimum Runtime",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
          xaxis_title="Number of Edges in Graph",
          yaxis_title="Seconds",
          legend_title="Data Structure",
        font=dict(family="Arial", size=18,),
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
            )
    return fig

def core_plot(summary: pd.DataFrame, projects: pd.DataFrame, proj: str, normalised=True, transformation=None, xtransform=None):
    """Does the normalised core plot for one project"""
    # ratio of performance between aeq and a designated library (comparison), based on the size of the network (num edges).
    fig = go.Figure()
    cores = list(set(summary.index.get_level_values("cores")))
    cores.sort()
    #print([xtransform(x) for x in cores])
    for alg in set(summary.index.get_level_values("details")):
        norm_time = []
        for core in cores:
            try:
                if transformation is None:
                    norm_time.append((summary.loc[(proj, alg, core)]["min"] / projects.loc[proj, "num_centroids"]) * 1000) \
                        if normalised else norm_time.append(summary.loc[(proj, alg, core)]["min"])
                    #print(alg, core, norm_time[-1])
                else:
                    norm_time.append(transformation(summary.loc[(proj, alg, core)]["min"]))
            except:
                pass
        trace = go.Scatter(x=cores if xtransform is None else [xtransform(x) for x in cores],
                           y=norm_time, name=alg)
        fig.add_trace(trace)
        # Iterate through each algorithm, then for each project compute the ratio
        # Aesthetics
        #print("library: ", alg, ", ratio: ", norm_time)
    fig.update_layout(title={
        'text': "Minimum Runtime per 1000 Origins for "+ proj if normalised \
            else "Minimum Runtime for "+ proj,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Number of Cores",
        yaxis_title="Seconds",
        legend_title="Data Structure",
        font=dict(family="Arial", size=18, ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def csv():
    francois1 = pd.read_csv(r"C:\Users\61435\Downloads\Arkansas_francois.csv")
    francois2 = pd.read_csv(r"C:\Users\61435\Downloads\longAn_Chicago_sf_francois.csv")
    boys = pd.read_csv(r"C:\Users\61435\Downloads\longAn_Chicago_sf_boys.csv")
    all_data = pd.concat([francois1, francois2, boys])
    return all_data

def sql():
    data = sq.connect(r"C:\Users\61435\Downloads\results_threadripper.sqlite")
    cur = data.cursor()
    sql_data = pd.read_sql('SELECT * FROM results', data)
    df = pd.DataFrame(sql_data, columns=["runtime", "project_name", "cores", "details"])
    df.rename(columns={"runtime": "min"}, inplace =True)
    return df

CSV = False
if __name__ == "__main__":
    # Create the mega dataframe, link the script to the file path for the boys, francois csv
    if CSV:
        all_data = csv()
        time_data = all_data.groupby("cores").get_group(1).groupby(["project_name", "details"]).min()\
            .drop("cores", axis=1).drop("sioux_falls", axis=0)
    else:
        all_data = sql()
        time_data = all_data.groupby("cores").get_group(1).groupby(["project_name", "details"]).min().drop("sioux_falls", axis=0)

    proj_summary = pd.read_csv(r"C:\Users\61435\Downloads\project summary (1).csv", index_col=0).drop("sioux_falls",
                                                                                                      axis=0)
    # plots by Core
    core_data = all_data.groupby(["project_name", "details", "cores"]).min()
    core_plot(core_data, proj_summary, "Australia").show()

    # normalised time plot
    # normalised_time_plot(time_data, proj_summary, normalised=False).show()

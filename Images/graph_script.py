import pandas as pd
import plotly.graph_objects as go
def normalised_time_plot(summary: pd.DataFrame, projects: pd.DataFrame) -> go.Figure:
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
    for alg in set(summary.index.get_level_values("details")):
        norm_time = []
        for proj in set(summary.index.get_level_values("project_name")):
            try:
                norm_time.append((summary.loc[(proj, alg)]["min"] / projects.loc[proj, "num_centroids"]) * 1000)
                print(alg, proj, norm_time[-1])
            except:
                pass
        trace = go.Scatter(x=projects["num_links"], y=norm_time, name=alg)
        fig.add_trace(trace)
    #Iterate through each algorithm, then for each project compute the ratio
        #Aesthetics
        print("library: ", alg, ", ratio: ", norm_time)
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
#Create the mega dataframe, link the script to the file path for the boys, francois csv
francois1 = pd.read_csv(r"C:\Users\61435\Downloads\Arkansas_francois.csv")
francois2 = pd.read_csv(r"C:\Users\61435\Downloads\longAn_Chicago_sf_francois.csv")
boys = pd.read_csv(r"C:\Users\61435\Downloads\longAn_Chicago_sf_boys.csv")
all_data = pd.concat([francois1,francois2,boys])
#agg by core count
core_agg = all_data.groupby("cores")
#plots by Core

#normalised time plot
proj_summary = pd.read_csv(r"C:\Users\61435\Downloads\project summary (1).csv", index_col=0).drop("sioux_falls", axis=0)
time_data = core_agg.get_group(1).groupby(["project_name","details"]).min().drop("cores", axis=1)
normalised_time_plot(time_data, proj_summary).show()



    # df = pd.read_csv("C:\Users\61435\Downloads\heap_benchmark_combined.csv")
    # df.drop("computer", axis=1)
    # summary = df.groupby(["project_name", "library"]).agg(
    #             average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
    #         ).drop("sioux_falls")
    # proj_summary = pd.read_csv("C:\Users\61435\Downloads\project summary (1).csv", index_col=0).drop("sioux_falls", axis=0)
    # #b, c = proj_summary.iloc[1].copy(), proj_summary.iloc[2].copy()
    # #proj_summary.iloc[1],proj_summary.iloc[2] = c,b
    #
    # #    largest_proj = proj_summary["num_nodes"].idxmax()
    # #aeq_ratios(summary, proj_summary, summary.loc[largest_proj, "min"].idxmin(),
    #            #["aequilibrae", "igraph", "networkit", "graph-tool"]).write_image("C:\Users\61435\Desktop\aequilibrae_performance_tests\Images\Benchmark_ratios.png", width=1000, height=800)
    # #benchmark_chart(summary, ["chicago_sketch", "Arkansas statewide model", "LongAn"], ["aequilibrae", "graph-tool", "igraph", "networkit"],["Chicago Sketch", "Arkansas Statewide Model", "Long An"]).write_image(r"C:\Users\61435\Desktop\aequilibrae_performance_tests\Images\Benchmark_proj.png", width=1000, height=800)
    # #time_plot(summary, proj_summary, ["aequilibrae", "igraph", "networkit", "graph-tool"]).write_image("Images/link_time.png",  width=1000, height=800)
    # normalised_time_plot(summary, proj_summary, ["aequilibrae", "igraph", "networkit", "graph-tool"])#.write_image("Images/normedlink_time.png",  width=1000, height=800)
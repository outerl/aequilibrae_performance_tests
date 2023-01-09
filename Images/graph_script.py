import pandas as pd
from plot_results import *


df = pd.read_csv(r"C:\Users\61435\Downloads\heap_benchmark_combined.csv")
df.drop("computer", axis=1)
summary = df.groupby(["project_name", "library"]).agg(
            average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
        ).drop("sioux_falls")
proj_summary = pd.read_csv(r"C:\Users\61435\Downloads\project summary (1).csv", index_col=0).drop("sioux_falls", axis=0)
#b, c = proj_summary.iloc[1].copy(), proj_summary.iloc[2].copy()
#proj_summary.iloc[1],proj_summary.iloc[2] = c,b

#    largest_proj = proj_summary["num_nodes"].idxmax()
#aeq_ratios(summary, proj_summary, summary.loc[largest_proj, "min"].idxmin(),
           #["aequilibrae", "igraph", "networkit", "graph-tool"]).write_image(r"C:\Users\61435\Desktop\aequilibrae_performance_tests\Images\Benchmark_ratios.png", width=1000, height=800)
#benchmark_chart(summary, ["chicago_sketch", "Arkansas statewide model", "LongAn"], ["aequilibrae", "graph-tool", "igraph", "networkit"],["Chicago Sketch", "Arkansas Statewide Model", "Long An"]).write_image(r"C:\Users\61435\Desktop\aequilibrae_performance_tests\Images\Benchmark_proj.png", width=1000, height=800)
#time_plot(summary, proj_summary, ["aequilibrae", "igraph", "networkit", "graph-tool"]).write_image("Images/link_time.png",  width=1000, height=800)
normalised_time_plot(summary, proj_summary, ["aequilibrae", "igraph", "networkit", "graph-tool"])#.write_image("Images/normedlink_time.png",  width=1000, height=800)

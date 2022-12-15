#!/usr/bin/env python3
import os
import subprocess
from argparse import ArgumentParser
from shutil import copyfile
from os.path import join, isfile
import warnings

import pandas as pd
from jinja2 import Environment, PackageLoader


def render_template(aeq_path: str, heap_path: str, min_elem_checker):
    heap_type = heap_path.split("/")[-1]
    env = Environment(loader=PackageLoader("benchmark", "templates"))
    template = env.get_template("pathfinding_template.html.jinja")
    out = template.render(HEAP_PATH=f"'{heap_path}'", 
                          MIN_ELEM=min_elem_checker.get(heap_type, "heap.next_available_index != 0"),
                          # PARAM="include 'parameters.pxi'" if min_elem_checker.get(heap_type, None) is None else ""
                          )
    with open(os.path.join(aeq_path, 'aequilibrae/paths/basic_path_finding.pyx'), 'w') as f:
        f.write(out)


def make_results(path_to_heaps):
    csvs = [f for f in os.listdir(path_to_heaps + "/utils") if f.endswith('.csv')]
    print(csvs)
    data = []
    for csv in csvs:
        data.append(pd.read_csv(path_to_heaps + "/utils/" + csv))
    summary = pd.concat(data).groupby(["project_name", "heap"]).agg(
        average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
    )
    print(summary)


def validate(args):
    subprocess.run(["python", r"../validation.py",
                    "--model-path", args["path"],
                    "--libaries", "aequilibrae igraph"
                    "--projects", " ".join(args["projects"]),
                    "--cost", args["cost"]])


def main():
    projects = ["sioux_falls", "chicago_sketch"]
    parser = ArgumentParser()
    parser.add_argument("-a", "--aequilibrae-path", dest="source", required=True,
                        help="path to aequilibrae source", metavar="FILE")
    parser.add_argument("-m", "--model-path", dest="path", default='../models',
                        help="path to models", metavar="FILE")
    parser.add_argument("-o", "--output-path", dest="output", default='./Images',
                        help="where to place output data and images", metavar="FILE")
    parser.add_argument("-i", "--iterations", dest="iters", default=2, type=int,
                        help="number of times to run each library per sample", metavar="X")
    parser.add_argument("-r", "--repeats", dest="repeats", default=5, type=int,
                        help="number of samples", metavar="Y")
    parser.add_argument("-c", "--cores", nargs="+", dest="cores", default=0,
                        help="number of cores to use. Use 0 for all cores.",
                        type=int, metavar="N")
    parser.add_argument("-p", "--projects", nargs='+', dest="projects",
                        default=projects, help="projects to benchmark using")
    parser.add_argument("--cost", dest="cost", default='free_flow_time',
                        help="cost column to skim for")
    parser.add_argument('--no-plots', dest='plots', action='store_false')
    parser.add_argument('--plots', dest='plots', action='store_true')
    parser.set_defaults(feature=True)

    args = vars(parser.parse_args())

    path_to_heaps = "heaps/"

    heaps = [f for f in os.listdir(path_to_heaps) if isfile(os.path.join(path_to_heaps, f)) and f.endswith('.pyx')]
    min_elem_checker = {
        "fibonacci.pyx": "heap.min_node"
    }

    #validate(heaps)
    print(heaps)
    for heap in heaps:
        if "kheap.pyx" in heap and heap in "kheap.pyx":
            print(heap + " is the jinja kheap")
            env = Environment(loader=PackageLoader("benchmark", "templates"))
            template = env.get_template("k_heap.jinja")
            out = template.render(K=8)
            with open('aequilibrae/paths/heaps/kheap.pyx', 'w') as f:
                f.write(out)

        print("Rendering ", heap.split(".")[0])
        relative_heap_path = "heaps/"
        render_template(args["source"], os.path.abspath(os.path.join(relative_heap_path, heap)), min_elem_checker)
        print("Compiling...")
        subprocess.run(["python", "setup_assignment.py", "build_ext", "--inplace"],
                       cwd=os.path.join(args["source"], "aequilibrae", "paths"))
        print("Compilation complete")
        subprocess.run(["python", r"../benchmark.py",
                        "--model-path", args["path"],
                        "--output-path", args["output"],
                        "--iterations", args["iters"],
                        "--repeats", args["repeats"],
                        "--cores", " ".join(args["cores"]),
                        "--libaries", "aequilibrae"
                        "--projects", " ".join(args["projects"]),
                        "--cost", args["cost"],
                        "--no-plots", args["no-plots"],
                        "--plots", args["plots"]])
    print("made it this far")
    make_results(path_to_heaps)



if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        main()




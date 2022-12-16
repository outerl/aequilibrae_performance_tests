#!/usr/bin/env python3
import os
import subprocess
from argparse import ArgumentParser
import tempfile
import warnings

import pandas as pd
from jinja2 import Environment, PackageLoader


def render_template(aeq_path: str, heap_path: str, min_elem_checker):
    heap_type = os.path.basename(heap_path)
    if os.name == "nt":
        real_path = heap_path.replace("\\", "\\\\")
    else:
        real_path = heap_path
    env = Environment(loader=PackageLoader("heap_benchmark", "templates"))
    template = env.get_template("pathfinding_template.html.jinja")
    out = template.render(HEAP_PATH=f"""'{real_path}'""",
                          MIN_ELEM=min_elem_checker.get(heap_type, "heap.next_available_index != 0"))
    with open(os.path.join(aeq_path, 'aequilibrae/paths/basic_path_finding.pyx'), 'w') as f:
        f.write(out)


def make_results(path_to_csvs: str, save_location: str):
    csvs = [f for f in os.listdir(path_to_csvs) if f.endswith('.csv')]
    data = []
    for csv in csvs:
        df = pd.read_csv(os.path.join(path_to_csvs, csv))
        data.append(df)
    summary = pd.concat(data).groupby(["project_name", "details", "cores"]).agg(
        average=("runtime", "mean"), min=("runtime", "min"), max=("runtime", "max")
    )
    summary.to_csv(os.path.join(save_location, "summary.csv"))
    print(summary)


def validate(args):
    subprocess.run(["python", r"validation.py",
                    "--model-path", args["path"],
                    "--libaries", "aequilibrae igraph"
                    "--projects", *args["projects"],
                    "--cost", args["cost"]])


def main():
    projects = ["sioux_falls", "chicago_sketch", "LongAn"]
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
    parser.add_argument("-c", "--cores", nargs="+", dest="cores", default=[0],
                        help="number of cores to use. Use 0 for all cores.",
                        type=int, metavar="N")
    parser.add_argument("-p", "--projects", nargs='+', dest="projects",
                        default=projects, help="projects to benchmark using")
    parser.add_argument("--cost", dest="cost", default='free_flow_time',
                        help="cost column to skim for")
    parser.set_defaults(feature=True)

    args = vars(parser.parse_args())

    path_to_heaps = "heaps/"

    heaps = [f for f in os.listdir(path_to_heaps) if os.path.isfile(os.path.join(path_to_heaps, f)) and f.endswith('.pyx')]

    min_elem_checker = {
        "fibonacci.pyx": "heap.min_node"
    }
    relative_heap_path = "heaps/"

    #validate(heaps)
    print(heaps)
    with tempfile.TemporaryDirectory() as tmpdirname:
        for heap in heaps:
            if "kheap.pyx" in heap and heap in "kheap.pyx":
                env = Environment(loader=PackageLoader("heap_benchmark", "templates"))
                template = env.get_template("k_heap.jinja")
                out = template.render(K=8)
                with open(os.path.abspath(os.path.join(relative_heap_path, heap)), 'w') as f:
                    f.write(out)

            print("Rendering ", heap.split(".")[0])
            render_template(args["source"], os.path.abspath(os.path.join(relative_heap_path, heap)), min_elem_checker)
            print("Compiling...")
            compiler = subprocess.run(["python", "setup_assignment.py", "build_ext", "--inplace"],
                           cwd=os.path.join(args["source"], "aequilibrae", "paths"),  shell=(os.name == 'nt'), env=os.environ,
                                      capture_output=True)
            if compiler.returncode:
                print("-" * 30, "stdout", "-" * 30)
                print(compiler.stdout.decode("utf-8"))
                print("-" * 30, "stderr", "-" * 30)
                print(compiler.stderr.decode("utf-8"))
                print("-" * 68)
                compiler.check_returncode()
            print("Compilation complete")
            subprocess.run(["python", "benchmark.py",
                            "--model-path", args["path"],
                            "--output-path", tmpdirname,
                            "--iterations", str(args["iters"]),
                            "--repeats", str(args["repeats"]),
                            "--cores", *(str(x) for x in args["cores"]),
                            "--libraries", "aequilibrae",
                            "--projects", *args["projects"],
                            "--cost", args["cost"],
                            "--details", heap.split(".")[0]], shell=(os.name == 'nt'), env=os.environ, check=True)
            print("\n\n")
        make_results(tmpdirname, args["output"])


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        main()

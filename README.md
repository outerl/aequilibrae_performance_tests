# aequilibrae_performance_tests
This is a collection of scripts designed to benchmark AequilibraE against a variety of other Python path finding libraries in their ability to form a matrix containing the lowest cost from any one node to another, these nodes are commonly the centroids of the network. The libraries tested include
- `igraph`
- `pandana`
- `networkit`
- `graph-tool`
# Deps
All libraries are optional other than AequilibraE, but most can be installed with
```
pip install aequilibrae igraph pandana networkit jinja2
```
AequilibraE also has additional requirements such as `spatialite`.

`graph-tool` is optional due to difficulty of installation. Its recommended to use the Docker container if you are attempted to test it. Or refer to their installation guide.
# Benchmarking
The `benchmark.py` script runs the supplied libraries through the provided models and reports their results.

The `heap/heap_benchmark.py` script benchmarks AequilibraE with various different heap implementations. It requires an editable installation of AequilibraE. **WARNING `heap/heap_benchmarking.py` will overwrite any changes to the `basic_path_finding.pyx`, and `parameters.pxi`**.
## Usage
`benchmark.py`
```
usage: benchmark.py [-h] [-m FILE] [-o FILE] [-i X] [-r Y] [-c N]
                    [-l {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...]]
                    [-p PROJECTS [PROJECTS ...]] [--cost COST] [--no-plots] [--plots]

optional arguments:
  -h, --help            show this help message and exit
  -m FILE, --model-path FILE
                        path to models
  -o FILE, --output-path FILE
                        where to place output data and images
  -i X, --iterations X  number of times to run each library per sample
  -r Y, --repeats Y     number of samples
  -c N, --cores N       number of cores to use. Use 0 for all cores.
  -l {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...], --libraries {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...]
                        libraries to benchmark
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
                        projects to benchmark using
  --cost COST           cost column to skim for
  --no-plots
  --plots
  
  
./benchmark.py -m ./models -p sioux_falls -l aequilibrae igraph networkit pandana -r 1 -i 1
```

`heap/heap_benchmark.py` is intended to be run from this repositories root.
```
./heaps/heap_benchmark.py --helpusage: heap_benchmark.py [-h] -a FILE [-m FILE] [-o FILE] [-i X] [-r Y] [-c N [N ...]] [-p PROJECTS [PROJECTS ...]] [--heaps HEAPS [HEAPS ...]] [--heap-path FILE]
                         [--template FILE] [--cost COST] [--validate] [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  -a FILE, --aequilibrae-path FILE
                        path to aequilibrae source
  -m FILE, --model-path FILE
                        path to models
  -o FILE, --output-path FILE
                        where to place output data and images
  -i X, --iterations X  number of times to run each library per sample
  -r Y, --repeats Y     number of samples
  -c N [N ...], --cores N [N ...]
                        number of cores to use. Use 0 for all cores.
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
                        projects to benchmark using
  --heaps HEAPS [HEAPS ...]
                        heaps to benchmark
  --heap-path FILE      where to find heaps to benchmark
  --template FILE       jinja template to use
  --cost COST           cost column to skim for
  --validate            enable validation instead of benchmarking
  --dry-run             if enabled no benchmarking will be performed, only compilation
  
./heaps/heap_benchmark.py -a ~/Software/aequilibrae -m ./models -p sioux_falls -i 1 -r 1 --cost distance -c 4 --heaps pq_4ary --template basic_path_finding_francois.pyx.jinja --dry-run --heap-path ./heaps/francois
```

### François Pacull's heap implementation
In addition to the heaps provided in `heaps/`, some heaps written by `François Pacull` are provided in `heaps/francois`. See `heaps/francois/LICENCE` for licensing.
His heaps are also detailed in his blog post at https://aetperf.github.io/2022/11/23/A-Cython-implementation-of-a-min-priority-queue.html

# Validation
To ensure all libraries report the same cost matrix, `validation.py` was written. It detects differences between the output of the libraries and displays it to the user.
## Usage
`validation.py`
```
usage: validation.py [-h] [-m FILE]
                     [-l {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...]]
                     [--cost COST] [-p PROJECTS [PROJECTS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -m FILE, --model-path FILE
                        path to models
  -l {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...], --libraries {aequilibrae,igraph,pandana,networkit,graph-tool} [{aequilibrae,igraph,pandana,networkit,graph-tool} ...]
                        libraries to validate, the first one is used as the reference
  --cost COST           cost column to skim for
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
                        projects to benchmark using
```
# Docker
For ease of use, a `Dockerfile` was created to automate the setup and testing of the scripts.
## Usage
Here's and example of the Dockerfile that supplies, a volume for the image and csv output, the models to test, the models location, the libraries to test, the cost values name, the number of cores to use, and the number of times to repeat the testing with the specified number of iterations.
```
docker run -v ~/aequilibrae_performance_tests/Images:/aequilibrae_performance_tests/Images \
    aequilibrae_performance_tests /bin/bash -c "conda init bash &> /dev/null && \
        source '/opt/conda/bin/activate' &> /dev/null && \
        conda activate benchmarking &> /dev/null && \
        python -u ./aequilibrae_performance_tests/benchmark.py -m ./models -o /aequilibrae_performance_tests/Images \
            -p sioux_falls chicago_sketch --cost distance \
            -l aequilibrae igraph networkit graph-tool \
            -r 2 -i 2 -c 1"
```
# Models
No models are supplied. All testing was done on existing AequilibraE project files.

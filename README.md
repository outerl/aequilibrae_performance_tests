# aequilibrae_performance_tests
This is a collection of scripts designed to benchmark AequilibraE against a variety of other Python path finding libraries in their ability to form a matrix containing the lowest cost from any one node to another, these nodes are commonly the centroids of the network. The libraries tested include
- `igraph`
- `pandana`
- `networkit`
- `graph-tool`
# Deps
All libraries are optional, but most can be installed with
```
pip install aequilibrae igraph pandana networkit ploty kaleido
```
AequilibraE also has additional requirements such as `spatialite`.

`graph-tool` is optional due to difficulty of installation. Its recommended to use the Docker container if you are attempted to test it. Or refer to their installation guide.
# Benchmarking
The `benchmark.py` script runs the supplied libraries through the provided models and reports their results. Its also able to form some plots and save those to disk.
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
```
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
Heres and example of the Dockerfile that supplies, a volume for the image and csv output, the models to test, the models location, the libraries to test, the cost values name, the number of cores to use, and the number of times to repeat the testing with the specified number of iterations.
```
docker run -v ~/aequilibrae_performance_tests/Images:/aequilibrae_performance_tests/Images \
    aequilibrae_performance_tests /bin/bash -c "conda init bash &> /dev/null && \
        source '/opt/conda/bin/activate' &> /dev/null && \
        conda activate benchmarking &> /dev/null && \
        python -u ./aequilibrae_performance_tests/benchmark.py -m ./models -o /aequilibrae_performance_tests/Images \
            -p sioux_falls chicago_sketch LongAn 'Arkansas statewide model' --cost distance \
            -l aequilibrae igraph networkit graph-tool \
            -r 2 -i 2 -c 1"
```
# Models
No models are supplied. All testing was done on existing AequilibraE project files.

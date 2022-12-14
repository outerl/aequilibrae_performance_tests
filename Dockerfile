FROM continuumio/anaconda3
SHELL ["/bin/bash", "-c"]

COPY ./models/ /models/

RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda create --name benchmarking -c conda-forge graph-tool python==3.8.14

RUN apt-get update -y && \
    apt-get install -y libsqlite3-mod-spatialite && \
    apt install -y build-essential

RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    pip install plotly kaleido

# igraph, pandana, and networkit setup
RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    pip install igraph pandana networkit

RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    git clone --depth 1 https://github.com/AequilibraE/aequilibrae && \
    pip install -r ./aequilibrae/requirements.txt && \
    pip install -r ./aequilibrae/requirements_additional.txt && \
    cd ./aequilibrae/aequilibrae/paths && python setup_assignment.py build_ext --inplace && cd / && \
    pip install ./aequilibrae

RUN git clone --depth 1 https://github.com/outerl/aequilibrae_performance_tests

# COPY aeq_testing.py networkit_testing.py project_utils.py igraph_testing.py \
#     pandana_testing.py benchmark.py validation.py plot_results.py ./aequilibrae_performance_tests/

CMD conda init bash &> /dev/null && \
    source '/opt/conda/bin/activate' &> /dev/null && \
    conda activate benchmarking &> /dev/null && \
    python -u ./aequilibrae_performance_tests/benchmark.py -m ./models -o /aequilibrae_performance_tests/Images \
        -p sioux_falls chicago_sketch --cost distance \
        -l aequilibrae igraph networkit graph-tool \
        -r 2 -i 2 -c 1

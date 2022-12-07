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
    git clone --depth 1 https://github.com/AequilibraE/aequilibrae && \
    pip install -r ./aequilibrae/requirements.txt && \
    pip install -r ./aequilibrae/requirements_additional.txt && \
    cd ./aequilibrae/aequilibrae/paths && python setup_assignment.py build_ext --inplace && cd / && \
    pip install ./aequilibrae

RUN git clone --depth 1 https://github.com/outerl/aequilibrae_performance_tests
RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    pip install plotly kaleido

# igraph, pandana, and networkit setup
RUN conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    pip install igraph pandana networkit

# COPY aeq_testing.py networkit_testing.py project_utils.py igraph_testing.py \
#     pandana_testing.py benchmark.py validation.py ./aequilibrae_performance_tests/

# Run validation
CMD conda init bash && \
    source "/opt/conda/bin/activate" && \
    conda activate benchmarking && \
    python ./aequilibrae_performance_tests/validation.py -m ./models -p sioux_falls && \
    python ./aequilibrae_performance_tests/benchmark.py -m ./models --no-plots

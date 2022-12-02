from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("binary_heap.pyx", annotate=True)
)
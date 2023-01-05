import numpy as np 
from libc.math cimport INFINITY

ctypedef double DTYPE_t
cdef DTYPE_t DTYPE_INF

cdef enum ElementState:
   SCANNED
   NOT_IN_HEAP
   IN_HEAP

cdef struct Element:
    DTYPE_t key
    ElementState state
    size_t node_idx

cdef struct PriorityQueue:
    size_t length  # number of elements in the array
    size_t size  # number of elements in the heap
    size_t* A  # array storing the binary tree
    Element* Elements  # array storing the elements
    DTYPE_t* keys

cdef DTYPE = np.float64
DTYPE_INF = INFINITY
DTYPE_INF_PY = DTYPE_INF

ctypedef long long ITYPE_t

# EPS is the precision of DTYPE
cdef DTYPE_t DTYPE_EPS = 1E-15

# NULL_IDX is the index used in predecessor matrices to store a non-path
cdef ITYPE_t NULL_IDX = 18446744073709551615

VERSION = 0.7
MINOR_VRSN = 7
binary_version = "0.7.7"
release_name = "Queluz"

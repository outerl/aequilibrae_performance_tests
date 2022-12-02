import cython
cimport cython
cimport numpy

@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function

cdef DTYPE_t weight

cdef struct BinaryHeap:
    DTYPE_t[100] storage
    int last_node


cdef struct Node:
    unsigned int index
    DTYPE_t val

#Heap methods
cdef void insert_node(BinaryHeap* heap, Node* node) nogil:
    pass

cdef Node* remove_min(BinaryHeap* heap) nogil:
    pass

cdef void decrease_val(BinaryHeap* heap, Node* node) nogil:
    pass

cdef void down_heap()

#Node methods
cdef void intialise_node(Node* node, unsigned int index, double val=0) nogil:
    node.index = index
    node.val = val

cimport cython
#import cython
from libc.math cimport floor
from libc.stdlib cimport realloc, malloc



cdef struct Node:
    unsigned int index
    double val

cdef struct BinaryHeap:
    #Pre-initialised to 6 layer binary heap for no particular reason
    Node[127] heap
    unsigned int last_node

#Heap methods
@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef void insert_node(BinaryHeap* heap, Node* node) nogil:
    cdef Node* node = node
    heap.heap[heap.last_node] = node
    node.index = heap.last_node
    #Resize using doubling strategy
    #up_heap(heap, node)
    if heap.last_node + 1 > sizeof(heap.heap)/sizeof(double):
        heap.heap = realloc(heap.heap, sizeof(heap.heap)*2)
    heap.last_node += 1
"""
@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef Node* remove_min(BinaryHeap* heap) nogil:
    cdef Node* min = heap.heap[0]
    heap.heap[0] = heap.heap[heap.last_node]
    heap.heap[heap.last_node] = NULL
    down_heap(heap, heap.heap[0])
    return min

@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef void decrease_val(BinaryHeap* heap, Node* node, double val) nogil:
    if val > node.val:
        node.val = val
        down_heap(heap, node)
    else:
        node.val = val
        up_heap(heap, node)

@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef void down_heap(BinaryHeap* heap, Node* node) nogil:
    cdef int a = node.index
    cdef Node* node = node
    if node.val <= min(heap.heap[2*a+1].val, heap.heap[2*a + 2].val):
        return
    cdef int b = 2*a+1 if heap.heap[2*a+1] < heap.heap[2*a+2] else 2*a + 2
    cdef Node swapped = heap.heap[b]
    #Swapping indices around
    node.index = b
    swapped.index = a
    heap.heap[a] = swapped
    heap.heap[b] = node
    down_heap(heap, node)

@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef void up_heap(BinaryHeap* heap, Node* node) nogil:
    cdef int a = node.index
    cdef int b = floor(a/2)
    cdef Node* node = node
    if node.val >= heap.heap[b].val:
        return
    cdef Node swapped = heap.heap[b]
    #Swapping indices around
    node.index = b
    swapped.index = a
    heap.heap[a] = swapped
    heap.heap[b] = node
    up_heap(heap, node)

#Node methods
@cython.wraparound(False)
@cython.embedsignature(True)
@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef void intialize_node(Node* node, unsigned int index, double val=0) nogil:
    node.index = index
    node.val = val
"""
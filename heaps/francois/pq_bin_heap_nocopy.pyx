# cython: boundscheck=False, wraparound=False, embedsignature=False, cython: cdivision=True, initializedcheck=False


""" Priority queue based on a minimum binary heap.
    
    Binary heap implemented with a static array.

    Tree Elements also stored in a static array.
"""

from cython.parallel import prange

from libc.stdlib cimport free, malloc

include "parameters.pxi"

cdef void init_heap(
    PriorityQueue* bheap,
    size_t length) nogil:
    """Initialize the binary heap.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t length : length (maximum size) of the heap
    """
    cdef size_t i

    bheap.length = length
    bheap.size = 0
    bheap.A = <size_t*> malloc(length * sizeof(size_t))
    bheap.Elements = <Element*> malloc(length * sizeof(Element))
    bheap.keys = <DTYPE_t*> malloc(length * sizeof(DTYPE_t))

    for i in range(length):
        bheap.A[i] = length
        _initialize_element(bheap, i)


cdef void init_heap_para(
    PriorityQueue* bheap,
    size_t length,
    int num_threads) nogil:
    """Initialize the binary heap with a parallel loop.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t length : length (maximum size) of the heap
    * int num_threads :  number of threads for the parallel job
    """
    cdef: 
        size_t i

    bheap.length = length
    bheap.size = 0
    bheap.A = <size_t*> malloc(length * sizeof(size_t))
    bheap.Elements = <Element*> malloc(length * sizeof(Element))
    bheap.keys = <DTYPE_t*> malloc(length * sizeof(DTYPE_t))

    for i in prange(
        length, 
        schedule='static', 
        nogil=True, 
        num_threads=num_threads):
        bheap.A[i] = length
        _initialize_element(bheap, i)


cdef inline void _initialize_element(
    PriorityQueue* bheap,
    size_t element_idx) nogil:
    """Initialize a single element.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t element_idx : index of the element in the element array
    """
    bheap.keys[element_idx] = DTYPE_INF
    bheap.Elements[element_idx].state = NOT_IN_HEAP
    bheap.Elements[element_idx].node_idx = bheap.length


cdef void free_heap(
    PriorityQueue* bheap) nogil:
    """Free the binary heap.

    input
    =====
    * PriorityQueue* bheap : binary heap
    """
    free(bheap.A)
    free(bheap.Elements)
    free(bheap.keys)


cdef void insert(
    PriorityQueue* bheap,
    size_t element_idx,
    DTYPE_t key) nogil:
    """Insert an element into the heap and reorder the heap.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t element_idx : index of the element in the element array
    * DTYPE_t key : key value of the element

    assumptions
    ===========
    * the element bheap.Elements[element_idx] is not in the heap
    * its new key is smaller than DTYPE_INF
    """
    cdef size_t node_idx = bheap.size

    bheap.size += 1
    bheap.Elements[element_idx].state = IN_HEAP
    bheap.Elements[element_idx].node_idx = node_idx
    bheap.A[node_idx] = element_idx
    _decrease_key_from_node_index(bheap, node_idx, key)


cdef void decrease_key(
    PriorityQueue* bheap,
    size_t element_idx,
    DTYPE_t key_new) nogil:
    """Decrease the key of a element in the heap, given its element index.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t element_idx : index of the element in the element array
    * DTYPE_t key_new : new value of the element key 

    assumption
    ==========
    * bheap.Elements[idx] is in the heap
    """
    _decrease_key_from_node_index(
        bheap, 
        bheap.Elements[element_idx].node_idx,
        key_new)


cdef DTYPE_t peek(PriorityQueue* bheap) nogil:
    """Find heap min key.

    input
    =====
    * PriorityQueue* bheap : binary heap

    output
    ======
    * DTYPE_t : key value of the min element

    assumption
    ==========
    * bheap.size > 0
    * heap is heapified
    """
    return bheap.keys[bheap.A[0]]


cdef bint is_empty(PriorityQueue* bheap) nogil:
    """Check whether the heap is empty.

    input
    =====
    * PriorityQueue* bheap : binary heap
    """
    cdef bint isempty = 0

    if bheap.size == 0:
        isempty = 1

    return isempty


cdef size_t extract_min(PriorityQueue* bheap) nogil:
    """Extract element with min keay from the heap, 
    and return its element index.

    input
    =====
    * PriorityQueue* bheap : binary heap

    output
    ======
    * size_t : element index with min key

    assumption
    ==========
    * bheap.size > 0
    """
    cdef: 
        size_t element_idx = bheap.A[0]  # min element index
        size_t node_idx = bheap.size - 1  # last leaf node index

    # exchange the root node with the last leaf node
    _exchange_nodes(bheap, 0, node_idx)

    # remove this element from the heap
    bheap.Elements[element_idx].state = SCANNED
    bheap.Elements[element_idx].node_idx = bheap.length
    bheap.A[node_idx] = bheap.length
    bheap.size -= 1

    # reorder the tree Elements from the root node
    _min_heapify(bheap, 0)

    return element_idx

cdef inline void _exchange_nodes(
    PriorityQueue* bheap,
    size_t node_i,
    size_t node_j) nogil:
    """Exchange two nodes in the heap.

    input
    =====
    * PriorityQueue* bheap: binary heap
    * size_t node_i: first node index
    * size_t node_j: second node index
    """
    cdef: 
        size_t element_i = bheap.A[node_i]
        size_t element_j = bheap.A[node_j]
        DTYPE_t key_tmp
    
    # exchange element indices in the heap array
    bheap.A[node_i] = element_j
    bheap.A[node_j] = element_i

    # exchange node indices in the element array
    bheap.Elements[element_j].node_idx = node_i
    bheap.Elements[element_i].node_idx = node_j


cdef inline void _min_heapify(
    PriorityQueue* bheap,
    size_t node_idx) nogil:
    """Re-order sub-tree under a given node (given its node index) 
    until it satisfies the heap property.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t node_idx : node index
    """
    cdef: 
        size_t l, r, i = node_idx, s

    while True:

        l =  2 * i + 1
        r = l + 1

        if (
            (l < bheap.size) and 
            (bheap.keys[bheap.A[l]] < bheap.keys[bheap.A[i]])
        ):
            s = l
        else:
            s = i

        if (
            (r < bheap.size) and 
            (bheap.keys[bheap.A[r]] < bheap.keys[bheap.A[s]])
        ):
            s = r

        if s != i:
            _exchange_nodes(bheap, i, s)
            i = s
        else:
            break
        


cdef inline void _decrease_key_from_node_index(
    PriorityQueue* bheap,
    size_t node_idx,
    DTYPE_t key_new) nogil:
    """Decrease the key of an element in the heap, given its tree index.

    input
    =====
    * PriorityQueue* bheap : binary heap
    * size_t node_idx : node index
    * DTYPE_t key_new : new key value

    assumptions
    ===========
    * bheap.Elements[bheap.A[node_idx]] is in the heap (node_idx < bheap.size)
    * key_new < bheap.Elements[bheap.A[node_idx]].key
    """
    cdef:
        size_t i = node_idx, j
        DTYPE_t key_j

    bheap.keys[bheap.A[i]] = key_new
    while i > 0: 
        j = (i - 1) // 2
        key_j = bheap.keys[bheap.A[j]]
        if key_j > key_new:
            _exchange_nodes(bheap, i, j)
            i = j
        else:
            break

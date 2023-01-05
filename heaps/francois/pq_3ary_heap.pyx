# cython: boundscheck=False, wraparound=False, embedsignature=False, cdivision=True, initializedcheck=False


""" Priority queue based on a minimum 3-ary heap.
    
    3-ary heap implemented with a static array.

    Tree elements also stored in a static array.
    
author : François Pacull
email: francois.pacull@architecture-performance.fr
copyright : Architecture & Performance
license : MIT
"""

from cython.parallel import prange

from libc.stdlib cimport free, malloc

include "parameters.pxi"

cdef void init_heap(
    PriorityQueue* pqueue,
    size_t length) nogil:
    """Initialize the binary heap.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t length : length (maximum size) of the heap
    """
    cdef size_t i

    pqueue.length = length
    pqueue.size = 0
    pqueue.A = <size_t*> malloc(length * sizeof(size_t))
    pqueue.Elements = <Element*> malloc(length * sizeof(Element))

    for i in range(length):
        pqueue.A[i] = length
        _initialize_element(pqueue, i)


cdef void init_heap_para(
    PriorityQueue* pqueue,
    size_t length,
    int num_threads) nogil:
    """Initialize the binary heap with a parallel loop.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t length : length (maximum size) of the heap
    * int num_threads :  number of threads for the parallel job
    """
    cdef size_t i

    pqueue.length = length
    pqueue.size = 0
    pqueue.A = <size_t*> malloc(length * sizeof(size_t))
    pqueue.Elements = <Element*> malloc(length * sizeof(Element))

    for i in prange(
        length, 
        schedule='static', 
        nogil=True, 
        num_threads=num_threads):
        pqueue.A[i] = length
        _initialize_element(pqueue, i)


cdef void _initialize_element(
    PriorityQueue* pqueue,
    size_t element_idx) nogil:
    """Initialize a single element.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t element_idx : index of the element in the element array
    """
    pqueue.Elements[element_idx].key = DTYPE_INF
    pqueue.Elements[element_idx].state = NOT_IN_HEAP
    pqueue.Elements[element_idx].node_idx = pqueue.length


cdef void free_heap(
    PriorityQueue* pqueue) nogil:
    """Free the binary heap.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    """
    free(pqueue.A)
    free(pqueue.Elements)


cdef void insert(
    PriorityQueue* pqueue,
    size_t element_idx,
    DTYPE_t key) nogil:
    """Insert an element into the heap and reorder the heap.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t element_idx : index of the element in the element array
    * DTYPE_t key : key value of the element

    assumptions
    ===========
    * the element pqueue.Elements[element_idx] is not in the heap
    * its new key is smaller than DTYPE_INF
    """
    cdef size_t node_idx = pqueue.size

    pqueue.size += 1
    pqueue.Elements[element_idx].state = IN_HEAP
    pqueue.Elements[element_idx].node_idx = node_idx
    pqueue.A[node_idx] = element_idx
    _decrease_key_from_node_index(pqueue, node_idx, key)


cdef void decrease_key(
    PriorityQueue* pqueue, 
    size_t element_idx, 
    DTYPE_t key_new) nogil:
    """Decrease the key of a element in the heap, given its element index.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t element_idx : index of the element in the element array
    * DTYPE_t key_new : new value of the element key 

    assumption
    ==========
    * pqueue.Elements[idx] is in the heap
    """
    _decrease_key_from_node_index(
        pqueue, 
        pqueue.Elements[element_idx].node_idx, 
        key_new)


cdef DTYPE_t peek(PriorityQueue* pqueue) nogil:
    """Find heap min key.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue

    output
    ======
    * DTYPE_t : key value of the min element

    assumption
    ==========
    * pqueue.size > 0
    * heap is heapified
    """
    return pqueue.Elements[pqueue.A[0]].key


cdef bint is_empty(PriorityQueue* pqueue) nogil:
    """Check whether the heap is empty.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue 
    """
    cdef bint isempty = 0

    if pqueue.size == 0:
        isempty = 1

    return isempty


cdef size_t extract_min(PriorityQueue* pqueue) nogil:
    """Extract element with min keay from the heap, 
    and return its element index.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue

    output
    ======
    * size_t : element index with min key

    assumption
    ==========
    * pqueue.size > 0
    """
    cdef: 
        size_t element_idx = pqueue.A[0]  # min element index
        size_t node_idx = pqueue.size - 1  # last leaf node index

    # printf("%d\n", pqueue.size)

    # exchange the root node with the last leaf node
    _exchange_nodes(pqueue, 0, node_idx)

    # remove this element from the heap
    pqueue.Elements[element_idx].state = SCANNED
    pqueue.Elements[element_idx].node_idx = pqueue.length
    pqueue.A[node_idx] = pqueue.length
    pqueue.size -= 1

    # reorder the tree Elements from the root node
    _min_heapify(pqueue, 0)

    return element_idx

cdef void _exchange_nodes(
    PriorityQueue* pqueue, 
    size_t node_i,
    size_t node_j) nogil:
    """Exchange two nodes in the heap.

    input
    =====
    * PriorityQueue* pqueue: binary heap
    * size_t node_i: first node index
    * size_t node_j: second node index
    """
    cdef: 
        size_t element_i = pqueue.A[node_i]
        size_t element_j = pqueue.A[node_j]
    
    # exchange element indices in the heap array
    pqueue.A[node_i] = element_j
    pqueue.A[node_j] = element_i

    # exchange node indices in the element array
    pqueue.Elements[element_j].node_idx = node_i
    pqueue.Elements[element_i].node_idx = node_j


cdef void _min_heapify(
    PriorityQueue* pqueue,
    size_t node_idx) nogil:
    """Re-order sub-tree under a given node (given its node index) 
    until it satisfies the heap property.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t node_idx : node index
    """
    cdef: 
        size_t c1, c2, c3, i = node_idx, s
        DTYPE_t val_tmp, val_min

    while True:

        c1 = 3 * i + 1  
        c2 = c1 + 1
        c3 = c2 + 1
        
        s = i
        val_min = pqueue.Elements[pqueue.A[s]].key
        if (c3 < pqueue.size):
            val_tmp = pqueue.Elements[pqueue.A[c3]].key
            if val_tmp < val_min:
                s = c3
                val_min = val_tmp
            val_tmp = pqueue.Elements[pqueue.A[c2]].key
            if val_tmp < val_min:
                s = c2
                val_min = val_tmp
            val_tmp = pqueue.Elements[pqueue.A[c1]].key
            if val_tmp < val_min:
                s = c1
        else:
            if (c2 < pqueue.size):
                val_tmp = pqueue.Elements[pqueue.A[c2]].key
                if val_tmp < val_min:
                    s = c2
                    val_min = val_tmp
                val_tmp = pqueue.Elements[pqueue.A[c1]].key
                if val_tmp < val_min:
                    s = c1
            else:
                if (c1 < pqueue.size):
                    val_tmp = pqueue.Elements[pqueue.A[c1]].key
                    if val_tmp < val_min:
                        s = c1

        if s != i:
            _exchange_nodes(pqueue, i, s)
            i = s
        else:
            break
        

cdef void _decrease_key_from_node_index(
    PriorityQueue* pqueue,
    size_t node_idx, 
    DTYPE_t key_new) nogil:
    """Decrease the key of an element in the heap, given its tree index.

    input
    =====
    * PriorityQueue* pqueue : 3-ary heap based priority queue
    * size_t node_idx : node index
    * DTYPE_t key_new : new key value

    assumptions
    ===========
    * pqueue.Elements[pqueue.A[node_idx]] is in the heap (node_idx < pqueue.size)
    * key_new < pqueue.Elements[pqueue.A[node_idx]].key
    """
    cdef:
        size_t i = node_idx, j
        DTYPE_t key_j

    pqueue.Elements[pqueue.A[i]].key = key_new
    while i > 0: 
        j = (i - 1) // 3
        key_j = pqueue.Elements[pqueue.A[j]].key
        if key_j > key_new:
            _exchange_nodes(pqueue, i, j)
            i = j
        else:
            break

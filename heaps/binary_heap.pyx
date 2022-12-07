cimport cython
from libc.stdlib cimport realloc, malloc
from cPython cimport PyList_New
# distutils: language=c

cdef struct Node:
    unsigned int index
    double val

cdef struct BinaryHeap:

    #Pointer to the heap array of Node pointers
    Node** heap
    #The index of the last node in the heap
    int last_node
    #The number of indices that have been allocated
    int last_elem

cdef BinaryHeap* initialize_heap(int num_nodes):
    #TODO: memset as zeros
    cdef BinaryHeap* a = <BinaryHeap*> malloc(sizeof(BinaryHeap))
    a.heap = <Node**> malloc(num_nodes * sizeof(Node*))
    a.next_available_index = 0
    a.last_elem = num_nodes
    return a

#Heap methods
@cython.cdivision(True)
cdef void insert_node(BinaryHeap* heap, Node* node):# nogil:
    heap.heap[heap.last_node] = node
    node.index = heap.last_node
    #Resize using doubling strategy
    heap.last_node += 1
    up_heap(heap, node)
    if heap.last_node == heap.last_elem:
        heap.last_elem = 2*heap.last_node
        heap.heap = <Node** > realloc(heap.heap,  (heap.last_elem+2) * sizeof(Node*))


cdef void init_insert_node(BinaryHeap* heap, double val):
    cdef Node* node = <Node*> malloc(sizeof(Node))
    node.index = heap.last_node
    node.val = val
    heap.heap[heap.last_node] = node
    #Resize using doubling strategy
    heap.last_node += 1
    up_heap(heap, node)
    if heap.last_node == heap.last_elem:
        heap.last_elem = 2*heap.last_node
        heap.heap = <Node** > realloc(heap.heap,  (heap.last_elem+2) * sizeof(Node*))


cdef Node* remove_min(BinaryHeap* heap):# nogil:
    """
    
    :param heap: 
    :return: 
    """
    # cdef BinaryHeap* heap = heap
    cdef Node* minim = heap.heap[0]
    heap.heap[0] = heap.heap[heap.last_node-1]
    heap.heap[0].index = 0
    heap.heap[heap.last_node-1] = NULL
    heap.last_node -= 1
    down_heap(heap, heap.heap[0])
    return minim

cdef void decrease_val(BinaryHeap* heap, Node* node, double val):# nogil:
    """
    
    :param heap: 
    :param node: 
    :param val: 
    :return: 
    """
    if val > node.val:
        node.val = val
        down_heap(heap, node)
    else:
        node.val = val
        up_heap(heap, node)

cdef void down_heap(BinaryHeap* heap, Node* node):# nogil:
    cdef int a = node.index
    #Memory safe check to make sure we aren't venturing into unknown territory (uninitialised memory)/child checking
    if 2 * a + 1 > heap.last_node-1:
        return
    if 2 * a + 2 > heap.last_node-1:
        b = 2 * a + 1
    else:
        b = 2 * a + 1 if heap.heap[2 * a + 1].val < heap.heap[2 * a + 2].val else 2 * a + 2
    if node.val <= heap.heap[b].val:
        return
    cdef Node* swapped = heap.heap[b]
    #Swapping indices around
    node.index = b
    swapped.index = a
    heap.heap[a] = swapped
    heap.heap[b] = node
    down_heap(heap, node)

cdef void up_heap(BinaryHeap* heap, Node* node): #nogil:
    cdef int a = node.index
    cdef int b = (a-1)/2
    if a == 0 or node.val >= heap.heap[b].val:
        return
    cdef Node* swapped = heap.heap[b]
    #Swapping indices around
    node.index = b
    swapped.index = a
    heap.heap[a] = swapped
    heap.heap[b] = node
    up_heap(heap, node)

#Node methods
cdef Node* intialize_node(unsigned int index, double val=0):# nogil:
    cdef Node* node = <Node*> malloc(sizeof(Node))
    node.index = index
    node.val = val
    return node

cdef list heap_to_list(BinaryHeap* heap):
    a = PyList_New(0)
    for i in range(0, heap.last_node):
        a.append(heap.heap[i].val)
    return a

def execute_python_test(inserts: list, solns: list):
    #Use char "r" to denote remove
    #use tuple (i, new_val) to denote decrement at index i
    heap = initialize_heap(len(inserts))
    i = 0
    for elem in inserts:
        if isinstance(elem, tuple):
            print("decrement ", elem)
            index, val = elem
            decrease_val(heap, heap.heap[index], val)
        elif isinstance(elem, str):
            print("removal")
            remove_min(heap)
        else:
            print("insert", elem)
            init_insert_node(heap, elem)
        print(solns[i], "Heap is: ", heap_to_list(heap))
        i+=1

cdef death_to_nodes(BinaryHeap* heap):
    #clean out every single value
    pass

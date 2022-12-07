cimport cython
from libc.stdlib cimport realloc, malloc, free
from cPython cimport PyList_New
# distutils: language=c

cdef struct Node:
    #index of the node in the array
    unsigned int index
    #State of the node, Dijkstra implementation specific
    #   SCANNED = 1
    #   NOT_IN_HEAP = 2
    #   IN_HEAP = 3
    unsigned int state
    #The skim/distance value of the node
    double val

cdef struct BinaryHeap:
    #Pointer to the heap array of Node pointers
    Node** heap
    #The index of the last node in the heap
    int next_available_index
    #The number of indices that have been allocated, used for dynamic memory allocation
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
    """
    Inserts the input node into the binary heap.
    :param heap: the heap being inserted into
    :param node: the node being inserted
    :return: None
    """
    heap.heap[heap.next_available_index] = node
    node.index = heap.next_available_index
    #Resize using doubling strategy
    heap.next_available_index += 1
    up_heap(heap, node)
    if heap.next_available_index == heap.last_elem:
        heap.last_elem = 2*heap.next_available_index
        heap.heap = <Node** > realloc(heap.heap,  (heap.last_elem+2) * sizeof(Node*))


cdef void init_insert_node(BinaryHeap* heap, double val):
    """
    Utility method that creates and inserts a given node in one method call.
    
    :param heap: BinaryHeap pointer that the node is being inserted to 
    :param val: Value assigned to the node
    :return: None
    """
    node = initialize_node(heap.next_available_index, val)
    insert_node(heap, node)

cdef Node* remove_min(BinaryHeap* heap):# nogil:
    """
    Removes the minimum node from the heap and reorganises accordingly.
    :param heap: the heap being removed from
    :return: Pointer to the node with the smallest value currently in the heap
    """
    # cdef BinaryHeap* heap = heap
    cdef Node* minim = heap.heap[0]
    heap.heap[0] = heap.heap[heap.next_available_index - 1]
    heap.heap[0].index = 0
    heap.heap[heap.next_available_index - 1] = NULL
    heap.next_available_index -= 1
    down_heap(heap, heap.heap[0])
    return minim

cdef void decrease_val(BinaryHeap* heap, Node* node, double val):# nogil:
    """
    Changes the value stored in the input node and restructures the heap accordingly. 
    It should be noted the value can also be increased
    :param heap: BinaryHeap
    :param node: Node in question
    :param val: New value the node is being changed to
    :return: you get nothing.
    """
    if val > node.val:
        node.val = val
        down_heap(heap, node)
    else:
        node.val = val
        up_heap(heap, node)

cdef void down_heap(BinaryHeap* heap, Node* node):# nogil:
    """
    Utility method used to maintain heap order. Takes the input node and moves it down the heap (swapping with its children)
    until it is in its correct location.
    :param heap: BinaryHeap pointer
    :param node: Node being adjusted
    :return: nadda
    """
    cdef int a = node.index
    #Memory safe check to make sure we aren't venturing into unknown territory (uninitialised memory)/child checking
    if 2 * a + 1 > heap.next_available_index-1:
        return
    if 2 * a + 2 > heap.next_available_index-1:
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
    """
    Utility method used to maintain heap order. Takes the input node and moves it up the heap (swapping with its parents)
    until it is in the correct location
    :param heap: BinaryHeap pointer
    :param node: Node being adjusted
    :return: read the function definition
    """
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
cdef Node* initialize_node(unsigned int index, double val=0):# nogil:
    """
    Initialises a node with the input index and value, and returns a pointer to it
    :param index: position in the heap. 
    :param val: The value stored in the node
    :return: Pointer to the Node
    """
    cdef Node* node = <Node*> malloc(sizeof(Node))
    node.index = index
    node.val = val
    return node

cdef list heap_to_list(BinaryHeap* heap):
    """
    Utility method for testing the heap functions correctly. The method takes an input heap and returns a python list
    Since python doesn't support pointers, the values of each Node are put in the position of the node instead of the pointer.
    :param heap: BinaryHeap being checked
    :return: Array form of the BinaryHeap with its values stored in it
    """
    a = PyList_New(0)
    for i in range(0, heap.next_available_index):
        a.append(heap.heap[i].val)
    return a

def execute_python_test(inserts: list, solns: list):
    """
    Utility method for executing python based tests into the cython code. Supports insertion, removal and decrementation:
    These actions are specified in inserts with the following syntax:
    insertion: A double value, e.g "4"
    removal: char "r"
    decrementation: tuple of index, new_value, e.g. (0,3) would change the 0th element (Node) in the heap's value to 3.
    An example array could be: [2,3,4,"r", (2,5), "r", 8]
    :param inserts: List of actions the heap is required to execute
    :param solns: The correct state of the heap after each action
    :return: None
    """
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
    """
    Cleanup for all the mallocs.
    :param heap: heap being destroyed
    :return: nothing
    """
    for i in range(0, heap.next_available_index):
        free(heap.heap[i])
    free(heap)

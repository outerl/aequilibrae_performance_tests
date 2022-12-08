import cython
from binary_heap import *
from unittest import TestCase

class HeapTests(TestCase):
    def test_removal(self):
        #Use a special char to signal removal
        inserts = [8, 4, 7, 2, 3, "r", "r", "r", "r"]
        solns = [
            [8.0],
            [4.0, 8,0],
            [4.0, 8.0, 7.0],
            [2.0, 4.0, 7.0, 8.0],
            [2.0, 3.0, 7.0, 8.0, 4.0],
            [3.0, 4.0, 7.0, 8.0],
            [4.0, 8.0, 7.0],
            [7.0, 8.0],
            [8.0]
        ]
        for j, i in enumerate(execute_python_test(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "Should be: " + str(solns[j]))

    #Check correct decrement

    #Helper to check heap order

    #Assuming some variety of list return:
    def test_insert(self):
        inserts = [8.0, 4.0, 7.0, 2.0, 3.0]
        solns = [
            [8.0],
            [4.0, 8.0],
            [4.0, 8.0, 7.0],
            [2.0, 4.0, 7.0, 8.0],
            [2.0, 3.0, 7.0, 8.0, 4.0],
        ]
        for j, i in enumerate(execute_python_test(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "Should be: " + str(solns[j]))

    def test_decrement(self):
        inserts = [7, 5, 3, (1, 6), (0, 8), (1, 3)]
        solns = [
            [7.0],
            [5.0, 7.0],
            [3.0, 7.0, 5.0],
            [3.0, 6.0, 5.0],
            [5.0, 6.0, 8.0],
            [3.0, 5.0, 8.0]
        ]
        for j, i in enumerate(execute_python_test(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "Should be: " + str(solns[j]))

def validate_list(heap, soln)->bool:
    for i in range(0, len(heap)):
        if heap[i] != soln[i]:
            return False
    return True

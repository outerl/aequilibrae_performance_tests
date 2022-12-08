import cython
from binary_heap import *
from four_heap import *
from unittest import TestCase

class BinaryHeapTests(TestCase):
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
        #list of ints into list of floats
        solns = float_me(solns)
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


class FourHeapTests(TestCase):
    def test_removal(self):
        #Use a special char to signal removal
        inserts = [15, 9, 16, 19, 22, 8, 18, 13, 25, 20, 17, 2, 30, 12, 1, 4, 24, 6, 29, 3, 7, 21, 14, 10, 11,
                   "r", "r", "r", "r", "r", "r","r"]
        solns = [
            [15],
            [9, 15],
            [9, 15, 16],
            [9, 15, 16, 19],
            [9, 15, 16, 19, 22],
            [8, 9, 16, 19, 22, 15],
            [8, 9, 16, 19, 22, 15, 18],
            [8, 9, 16, 19, 22, 15, 18, 13],
            [8, 9, 16, 19, 22, 15, 18, 13, 25],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20, 17],
            [2, 9, 8, 19, 22, 15, 18, 13, 25, 20, 17, 16],
            [2, 9, 8, 19, 22, 15, 18, 13, 25, 20, 17, 16, 30],
            [2, 9, 8, 12, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24],
            [1, 9, 8, 2, 6, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22],
            [1, 9, 8, 2, 6, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21],
            [1, 9, 8, 2, 3, 14, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15],
            [1, 9, 8, 2, 3, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15, 14],
            [1, 9, 8, 2, 3, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15, 14, 11],
            [2, 9, 8, 4, 3, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 11, 24, 22, 29, 6, 7, 21, 15, 14],
            [3, 9, 8, 4, 6, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 11, 24, 22, 29, 14, 7, 21, 15],
            [4, 9, 8, 11, 6, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 15, 24, 22, 29, 14, 7, 21],
            [6, 9, 8, 11, 7, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 15, 24, 22, 29, 14, 21],
            [7, 9, 8, 11, 14, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 15, 24, 22, 29, 21],
            [8, 9, 16, 11, 14, 10, 18, 13, 25, 20, 17, 21, 30, 19, 12, 15, 24, 22, 29],
            [9, 10, 16, 11, 14, 29, 18, 13, 25, 20, 17, 21, 30, 19, 12, 15, 24, 22],
        ]
        for j, i in enumerate(execute_python_test_four(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "\n Should be: " + str(solns[j]))

    #Check correct decrement

    #Helper to check heap order

    #Assuming some variety of list return:
    def test_insert(self):
        inserts = [15,9,16,19,22,8,18,13,25,20,17,2,30,12,1,4,24,6,29,3,7,21,14,10,11]
        solns = [
            [15],
            [9,15],
            [9,15,16],
            [9,15,16,19],
            [9,15,16,19,22],
            [8,9, 16, 19, 22, 15],
            [8, 9, 16, 19, 22, 15, 18],
            [8, 9, 16, 19, 22, 15, 18, 13],
            [8, 9, 16, 19, 22, 15, 18, 13, 25],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20, 17],
            [2, 9, 8, 19, 22, 15, 18, 13, 25, 20, 17, 16],
            [2, 9, 8, 19, 22, 15, 18, 13, 25, 20, 17, 16, 30],
            [2, 9, 8, 12, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4],
            [1, 9, 8, 2, 22, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24],
            [1, 9, 8, 2, 6, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22],
            [1, 9, 8, 2, 6, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7],
            [1, 9, 8, 2, 3, 15, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21],
            [1, 9, 8, 2, 3, 14, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15],
            [1, 9, 8, 2, 3, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15, 14],
            [1, 9, 8, 2, 3, 10, 18, 13, 25, 20, 17, 16, 30, 19, 12, 4, 24, 22, 29, 6, 7, 21, 15, 14, 11],
            ]
        solns = float_me(solns)
        for j, i in enumerate(execute_python_test_four(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "Should be: " + str(solns[j]))

    def test_decrement(self):
        inserts = [15, 9, 16, 19, 22, 8, 18, 13, 25, 20, 17, 2, (9, 1), (0, 2), (1, 16)]
        solns = [
            [15],
            [9, 15],
            [9, 15, 16],
            [9, 15, 16, 19],
            [9, 15, 16, 19, 22],
            [8, 9, 16, 19, 22, 15],
            [8, 9, 16, 19, 22, 15, 18],
            [8, 9, 16, 19, 22, 15, 18, 13],
            [8, 9, 16, 19, 22, 15, 18, 13, 25],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20],
            [8, 9, 16, 19, 22, 15, 18, 13, 25, 20, 17],
            [2, 9, 8, 19, 22, 15, 18, 13, 25, 20, 17, 16],
            [1, 9, 2, 19, 22, 15, 18, 13, 25, 8, 17, 16],
            [2, 9, 2, 19, 22, 15, 18, 13, 25, 8, 17, 16],
            [2, 13, 2, 19, 22, 15, 18, 16, 25, 8, 17, 16],
        ]
        solns = float_me(solns)
        for j, i in enumerate(execute_python_test_four(inserts, solns)):
            if not validate_list(i, solns[j]):
                self.fail("Heap order failure was:" + str(i) + "Should be: " + str(solns[j]))

def float_me(solns: list):
    """
    Utility method to convert a nested list of integers into floats
    :param solns:
    :return:
    """
    return [[float(d) for d in i] for i in solns]


def validate_list(heap, soln)->bool:
    for i in range(0, len(heap)):
        if heap[i] != soln[i]:
            return False
    return True

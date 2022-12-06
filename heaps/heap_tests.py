import cython
from binary_heap import *


def set_up():
    pass


def test_heap(elems: list):
    """
    Takes an input list of elements and appends them in their inserted order to the binary heap
    :param elems:
    :return:
    """
    pass


def validate_decrement():

    pass

def validate_removal():
    #Use a special char to signal removal
    inserts = [8, 4, 7, 2, 3, "r", "r", "r", "r"]
    solns = [
        [8],
        [4, 8],
        [4, 8, 7],
        [2, 4, 7, 8],
        [2, 3, 7, 8, 4],
        [3, 4, 7, 8],
        [4, 7, 8],
        [7, 8],
        [8]
    ]
    execute_python_test(inserts, solns)

    pass
#Check correct decrement

#Helper to check heap order

#Assuming some variety of list return:
def validate_insert():
    inserts = [8, 4, 7, 2, 3]
    solns = [
        [8],
        [4, 8],
        [4, 8, 7],
        [2, 4, 7, 8],
        [2, 3, 4, 7, 8],
    ]
    execute_python_test(inserts, solns)
"""    for j, i in enumerate(execute_python_test(inserts, solns)):
        if solns[j] != i:
            print("Heap rules violated, heap returned: ", i, " should be: ", solns[j])
"""

def validate_decrement():
    inserts = [7, 5, 3, (1, 6), (0, 8), (1, 3)]
    solns = [
        [7],
        [5, 7],
        [3, 7, 5],
        [3, 6, 5],
        [5, 6, 8],
        [3, 5, 8]
    ]
    execute_python_test(inserts, solns)
"""    for j, i in enumerate(execute_python_test(inserts, solns)):
        print(i, solns[j])
        if solns[j] != i:
            print("Heap rules violated, heap returned: ", i, " should be: ", solns[j])
"""
def main():
    #validate_insert()
    #validate_decrement()
    validate_removal()

if __name__ == "__main__":
    main()

import numpy as np
import itertools


def surrounding_area(i:int , j:int, size :int = 1, include_center = False) -> set:
    """
    gets the i,js for the sorrounding are of i,j where:

    i-size > i < i+size 

    and 

    j-size > j < j+size 
    """
    i_ = np.arange(i-size, i+size+1)
    j_ = np.arange(j-size, j+size+1)
    box = set(itertools.product(i_, j_, repeat = 1))

    if not include_center:
        box.remove((i,j))
        
    return box

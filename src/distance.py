
# basics
from typing import Tuple
import numpy as np


class DistanceToObstacle:

    """
    Will calculate the (inverse?) normalized distance of a empty grid at a position (x,y)
    to a obstacle at some position (x1!=x, y1!=y).

    max_distance: decided how many grids from a wall that should be included

    If max_distance == 6 the normalized distance score is d ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}
    
    The higher the score the closer the obstacle is
    """

    def __init__(self, max_distance : int = 5) -> None:
        self.max_distance = max_distance
        

    def _find_first_one(self, values:np.ndarray) -> int:
        # finds the first 1 and return the index of the 1
        return next((i for i, x in enumerate(values, start = 1) if x == 1), 999)


    def _find_closest_axis(self, grid:np.ndarray, i:int, j:int) -> int:
        # finds the closes 1 to the left and the right of the start position j
        # will then return the min value, i.e. the closest distance to an obstacle
        left = grid[i][j-1::-1]
        right = grid[i][j+1:]
        return min(self._find_first_one(left), self._find_first_one(right))


    def _find_closest_diag(self, diag_values:np.ndarray, i:int) -> int:
        diag_up = np.flip(diag_values[:i])
        diag_down = diag_values[i+1:]
        return min(self._find_first_one(diag_up), self._find_first_one(diag_down))


    def _find_closest_diagonal(self, grid:np.ndarray, x:int, y:int) -> Tuple[int,int]:
        
        # we first pad the grid with the penalty distance
        # so that we get same same shape for each look-around
        # for each x,y coordinate.
        # this might not be the most efficient way do to it
        # as you need to go through paddings at the momment when looking
        # for the first 1. But its easier to get the diagonal and 
        # reversed diagonal
        padded_grid = np.pad(grid, self.max_distance)

        # we set the slicing indexing
        i = y
        i_ = y+(self.max_distance*2)+1
        j = x
        j_ = x+(self.max_distance*2)+1

        # get the neighbours for (y,x)
        m_neighbours = padded_grid[i:i_, j: j_]

        # get the diagonals
        diag = m_neighbours.diagonal()
        rev_diag = np.fliplr(m_neighbours).diagonal()

        # find the closest 1
        # k = n steps to the closest 1 on the diagonal
        # rk = n steps to the closest 1 on the reversed/mirrored diagonal
        k = self._find_closest_diag(diag_values = diag, i = self.max_distance)
        rk = self._find_closest_diag(diag_values = rev_diag, i = self.max_distance)

        return k, rk

        
    def _find_closest_across(self, grid:np.ndarray, x:int, y:int) -> Tuple[int,int]:   
        # given a binary grid will find for any 0 the closes 1 on the x and y axis 

        a = self._find_closest_axis(grid.T, x, y)
        b = self._find_closest_axis(grid, y, x)
        return a, b
    

    def find_closest(self,  grid:np.ndarray, x:int, y:int):
        # k = n steps to the closest 1 on the diagonal
        # rk = n steps to the closest 1 on the reversed/mirrored diagonal
        # a = n steps to the closest 1 across on axis 1
        # b = n steps to the closest 1 across on axis 0
        a, b = self._find_closest_across(grid=grid, x=x, y=y)
        k, rk = self._find_closest_diagonal(grid=grid, x=x, y=y)

        return (a, b, k, rk)

        
    def distance_score(self, a:int, b:int, k:int, rk:int) -> float:

        min_distance = min([a, b, k, rk])

        if min_distance > self.max_distance:
            return 0.0

        penalty = 1 - (min_distance * (1/self.max_distance))

        return penalty

    
    def __call__(self, grid:np.ndarray, x:int, y:int) -> float:
        return self.distance_score(*self.find_closest(grid=grid, x=x, y=y))
    

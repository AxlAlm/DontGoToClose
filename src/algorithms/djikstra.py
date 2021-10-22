

# basics
from typing import Dict, Tuple
from queue import PriorityQueue


# fastestpath
from ..map import Map


class Djikstra:


    def __init__(self):
        self.visited : set = set()


    def get_neighbours(self, x, y):
        #ugly whay to get the x, y coordinates surrounding x,y
        # if o is the x,y cell we get all the xys for the x's
        #   x x x
        #   x o x
        #   x x x
        neighbours = set([(x-1, y), (x+1, y), (x-1, y+1), (x+1, y+1),(x, y-1), (x, y+1)])

        # we filter out non existing x,ys
        filtered_neighbours = neighbours.intersection(self.possible_paths)

        # then filter out the visited / closed grids
        return filtered_neighbours.difference(self.visited)


    def run(self, map:Map) -> dict:

        # for each step we take we calcualte the distance by
        # distance + (1 * penalty)

        grid = map.grid 
        start_xy = map.start_xy
        goal_xy = map.goal_xy

        # init all the path scores to inf
        # these are the score to get to any x,y in the grid from start_x, start_y
        path_scores = {k: float("inf") for k in grid}

        self.possible_paths = set(path_scores.keys())
        self.visited = self.visited | {k for k, obj in grid.items() if obj.is_closed and not obj.is_goal}

        # we start a queue
        q = PriorityQueue()   

        # we init the queue with out start point and distance 0
        q.put((0, start_xy))

        
        # we loop until we have no items in out queue
        # 
        # ps = w on current grid block
        # c = current grid block
        # n = neighour
        # n_w = weight to the neighbour from c
        goal_found = False
        while not q.empty() and not goal_found:

            # we get the first item in out queue. Items will be picked 
            # based on the score, i.e. the fastest path
            ps, (x, y) = q.get()


            # we get all the unvisted neighbours
            neighbours = self.get_neighbours(x,y) 

            # then we loop through all neighbours
            for n_xy in neighbours:

                grid_obj = grid[n_xy]

                if grid_obj.is_goal:
                    goal_found = True
                    break

                # we get the current path score 
                current_path_score = path_scores[n_xy]

                # then we get the Object occopying that grid and get the 
                # weight to travel to that grid
                new_path_score = ps + (1 + (3 * grid[n_xy].weight))  

                # if the path score is less then before we .... 
                if new_path_score < current_path_score:
                    path_scores[n_xy] = new_path_score
                    q.put((new_path_score, n_xy))
                    grid_obj.draw_path(map.screen)


                self.visited.add(n_xy)

        #(path_scores)
        return path_scores
   




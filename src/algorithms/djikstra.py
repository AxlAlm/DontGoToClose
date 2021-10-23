

# basics
from typing import Dict, Tuple
from queue import PriorityQueue


# fastestpath
from ..map import Map


PATH_COLOR = (255,145,29) #(255,217,102)
SEARCH_COLOR = 	(35,142,142)


class Djikstra:

    def __init__(self, map:Map, penalty_cost:int = 3) -> None:

        # init some vars
        self.grid = map.grid 
        self.start_xy = map.start_xy
        self.goal_xy = map.goal_xy

        # init all the path scores to inf
        # these are the score to get to any x,y in the grid from start_x, start_y
        self.path_scores = {k: float("inf") for k in self.grid}

        # a set will all x,ys in the grid
        self.possible_paths = set(self.path_scores.keys())

        # we init our visited with the gird block which are obstacles
        self.visited = {k for k, obj in self.grid.items() if obj.btype == "wall"}

        # shortest_path
        self.backtrack_dict = {}
        
        # penalty decides the cost to travel to a new grid based on how close to the 
        # wall you the grid is. The penalty_cost * dist_to_wall (0-1) is added to 1.
        self.penalty_cost = penalty_cost
    

    def _find_shortest_path(self):
        current_xy = self.goal_xy
        while True:
            current_xy, grid_obj = self.backtrack_dict[current_xy]

            grid_obj.fill(color = PATH_COLOR, update = True)

            if grid_obj.btype == "start":
                break
            

    def get_neighbours(self, x:int, y:int) -> set:
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


    def run(self) -> None:

        # we start a queue
        q = PriorityQueue()   

        # we init the queue with out start point and distance 0
        q.put((0, self.start_xy))

        # we loop until we have no items in out queue
        goal_found = False
        while not q.empty() and not goal_found:

            # we get the first item in out queue. Items will be picked 
            # based on the score, i.e. the fastest path
            ps, (x, y) = q.get()

            # we get all the unvisted neighbours
            neighbours = self.get_neighbours(x,y) 


            # then we loop through all neighbours
            for n_xy in neighbours:

                grid_obj = self.grid[n_xy]

                if grid_obj.btype == "goal":
                    self.backtrack_dict[self.goal_xy] = ((x, y), grid_obj)
                    goal_found = True
                    break

                # we get the current path score 
                current_path_score = self.path_scores[n_xy]

                # then we get the Object occopying that grid and get the 
                # weight to travel to that grid
                new_path_score = ps + (1 + (self.penalty_cost * self.grid[n_xy].dist_from_wall))  

                # if the path score is less then before we chose the path 
                # else move to the next neighbour
                if new_path_score < current_path_score:
                    self.path_scores[n_xy] = new_path_score
                    q.put((new_path_score, n_xy))

                    if n_xy != self.start_xy and n_xy != self.goal_xy:
                        grid_obj.fill(color = SEARCH_COLOR, shape = "ellipse", update = True)

                    # we add the cells so we can backtrack the shortest path
                    self.backtrack_dict[n_xy] = ((x, y), grid_obj)

                self.visited.add(n_xy)


        self._find_shortest_path()
   




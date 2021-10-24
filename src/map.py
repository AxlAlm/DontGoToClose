

#basics
from typing import Union, Tuple, Dict, List
import numpy as np
from random import randint

# pygame
import pygame

# fastestpath
from .grid_block import GridBlock
from .distance import DistanceToObstacle
from .utils import surrounding_area



class Map:

    def __init__(self, 
                desc:str, 
                map : str = "example1",
                max_distance : int = 5,
                show_distance : bool = True,
                ):
        
        self.distance_score = DistanceToObstacle(max_distance = max_distance)
        self.show_distance = show_distance

        # set desc
        pygame.display.set_caption(desc)

        # set screen values
        self.screen_width : int = 800
        self.screen_height : int = 600
        self.block_size : int = 20
        self.max_x : int = int(self.screen_width / self.block_size)
        self.max_y : int = int(self.screen_height / self.block_size)

        # create binary grid for string information where the obstacles are
        self._binary_grid = np.zeros((self.max_y, self.max_x))

        # init screen
        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))

        # variables we will fill
        self.grid : Dict[Tuple(int,int), GridBlock] = {}
        self.__create_map(map)
        

    def __example_map1(self):

        """
        This is an example map which consists of a wall across the middel with two gaps
        one tiny in the middle and one large in the end.

        The map is to examplify that the shortest path is not allways the fastest, given
        some restrictings in speed.
        

        """

        # middle start and end
        ms = int(self.max_y * 0.4)
        me = int(self.max_y * 0.6)

        # create ys for walls
        ys = list(range(ms,me))


        #small tunnel end and start
        sms = int(self.max_x * 0.50)
        sme = int(self.max_x * 0.55)

        #large runnel start
        lms = int(self.max_x * 0.75)

        # create x for walls
        xs = list(range(0, sms)) + list(range(sme, lms))

        # we add obstacles for each x,y
        all_xys = []
        for y in ys:
            for x in xs:
                obst = GridBlock(
                                btype = "obstacle",
                                x = int(x*self.block_size),
                                y = int(y*self.block_size),
                                width = self.block_size,
                                height = self.block_size,
                                color = (51,51,51),
                                shape = "rect",
                                screen = self.screen, 
                                )

                self.grid[(x,y)] = obst
                all_xys.append((x,y))
        
        
        # then we set a goal
        x = int(self.max_x / 2)
        self.goal = GridBlock(
                                btype = "goal",
                                x = int(x*self.block_size),
                                y = 2*self.block_size,
                                width = self.block_size,
                                height = self.block_size,
                                color = (56,118,29),
                                shape = "ellipse",
                                screen = self.screen, 
                                )
        self.grid[(x, 2)] =  self.goal
        self.goal_xy = (x,2)


        # then we add start
        self.start = GridBlock(
                                btype = "start",
                                x = int(x*self.block_size),
                                y = (self.max_y-2)*self.block_size,
                                width = self.block_size,
                                height = self.block_size,
                                color = (119,164,254),
                                shape = "ellipse",
                                screen = self.screen, 
                                )
        self.grid[(x, self.max_y-2)] = self.start
        self.start_xy = (x, self.max_y-2)

        return all_xys


    def __random_map(self):

        
        goal_x = randint(0, int(self.max_x/2))
        goal_y = randint(0, 5) # we set the goal in the 5 top tiles
        self.goal = GridBlock(
                                btype = "goal",
                                x = int(goal_x*self.block_size),
                                y = goal_y*self.block_size,
                                width = self.block_size,
                                height = self.block_size,
                                color = (56,118,29),
                                shape = "ellipse",
                                screen = self.screen, 
                                )
        self.grid[(goal_x, goal_y)] =  self.goal
        self.goal_xy = (goal_x, goal_y)


        start_x = randint(int(self.max_x/2), self.max_x-1)
        start_y = randint(self.max_y - 5, self.max_y-1) # we set the start in the bottom tiles
        ## first we place start and goal
        self.start = GridBlock(
                            btype = "start",
                            x = int(start_x*self.block_size),
                            y = start_y*self.block_size,
                            width = self.block_size,
                            height = self.block_size,
                            color = (119,164,254),
                            shape = "ellipse",
                            screen = self.screen, 
                            )

        self.grid[(start_x, start_y)] =  self.start
        self.start_xy = (start_x, start_y)


        # then we 
        c = 0
        all_obst_xys = set()
        while c <= 15:

            x = randint(0, self.max_x-1)
            y = randint(0, self.max_y-1) # we set the goal in the 5 top tiles

            surroundings = surrounding_area(x, y, size = 2, include_center = True)

            for nx, ny in surroundings:

                if nx < 0 or nx >= self.max_x:
                    continue
            
                if ny < 0 or ny >= self.max_y:
                    continue

                if (nx,ny) == self.start_xy or (nx,ny) == self.goal_xy:
                    continue

                obst = GridBlock(
                                btype = "obstacle",
                                x = int(nx*self.block_size),
                                y = int(ny*self.block_size),
                                width = self.block_size,
                                height = self.block_size,
                                color = (51,51,51),
                                shape = "rect",
                                screen = self.screen, 
                                )
                self.grid[(nx, ny)] = obst
                all_obst_xys.add((nx, ny))

            c += 1
  

        return all_obst_xys


    def __create_map(self, map:str):

        # create map, which means create obstacles, goal and start
        if map == "example1":
            all_obst_xys = self.__example_map1()

        elif map == "random":
            all_obst_xys = self.__random_map()

        else:
            raise KeyError(f"'{map}' is not a supported map. try {{random, example1}}.")


        # fill the binary grid
        for x,y in all_obst_xys:
            self._binary_grid[y,x] = 1


        # then we fill all other grids with a which blocks which are set to open and 
        # are penalized based on their vicinity to an closed block, e.g. an obstacle
        for x, w in enumerate(range(0, self.screen_width, self.block_size)):
            for y, h in enumerate(range(0, self.screen_height, self.block_size)):

                if (x,y) in self.grid:
                    continue
                
                self.grid[(x,y)] = GridBlock(
                                                btype = "empty",
                                                x = w,
                                                y = h,
                                                width = self.block_size,
                                                height = self.block_size,
                                                shape = "rect",
                                                color = "white",
                                                distance = self.distance_score(grid=self._binary_grid, x=x, y=y),
                                                screen = self.screen, 
                                                )


    def draw_map(self) -> None:
        self.screen.fill("white")
        [o.fill(show_distance = self.show_distance) for o in self.grid.values()]  
        pygame.display.flip()



#basics
from typing import Union, Tuple, Dict, List
import numpy as np


# pygame
import pygame

# fastestpath
from .objects import GridBlock
from .penalizer import Penalizer


class Map:

    def __init__(self, 
                desc:str, 
                map :str = "example1",
                draw_grid : bool = True,
                draw_weights : bool = True,
                penalty_distance :int = 5,
                ):
        
        self.penalizer = Penalizer(penalty_distance = penalty_distance)
        self.draw_grid = draw_grid
        self.draw_weights = draw_weights

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
        self.obsts : List[GridBlock] = []
        self.goal : GridBlock =  None
        self.start :GridBlock  = None

        self.__create_map()
        

  
    def __example_map_1(self):

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
                                x = int(x*self.block_size),
                                y = int(y*self.block_size),
                                width = self.block_size,
                                height = self.block_size,
                                color = "black",
                                shape = "rect",
                                )

                self.grid[(x,y)] = obst
                self.obsts.append(obst)
                all_xys.append((x,y))
        
        
        # then we set a goal
        x = int(self.max_x / 2)
        self.goal = GridBlock(
                                x = int(x*self.block_size),
                                y = 2*self.block_size,
                                width = self.block_size,
                                height = self.block_size,
                                color = "green",
                                shape = "ellipse",
                                is_goal = True
                                )
        self.grid[(x, 2)] =  self.goal
        self.goal_xy = (x,2)


        # then we add start
        self.start = GridBlock(
                                x = int(x*self.block_size),
                                y = (self.max_y-2)*self.block_size,
                                width = self.block_size,
                                height = self.block_size,
                                color = "blue",
                                shape = "ellipse"
                                )
        self.grid[(x, self.max_y-2)] = self.start
        self.start_xy = (x, self.max_y-2)

        return all_xys


    def __create_map(self):

        # create map, which means create obstacles, goal and start
        all_obst_xys = self.__example_map_1()

        for x,y in all_obst_xys:
            self._binary_grid[y,x] = 1


        # then we fill all other grids with a GirdBlock GridBlock which contains information
        # about how far off the closest obstacle is. By filling the grid like this we
        # can easily traverse the grid later and always know where we are.
        # we can also use this GirdBlock to score a certain path by adding some coloring :)
        for x, w in enumerate(range(0, self.screen_width, self.block_size)):
            for y, h in enumerate(range(0, self.screen_height, self.block_size)):
                #self.xy2wh[(x,y)] = (w,h)

                if (x,y) in self.grid:
                    continue
                
                self.grid[(x,y)] = GridBlock(
                                                x = w,
                                                y = h,
                                                width = self.block_size,
                                                height = self.block_size,
                                                shape = "rect",
                                                color = "red",
                                                weight = self.penalizer(grid=self._binary_grid, x=x, y=y),
                                                is_closed = False,
                                                #n_x_to_obj = find_closest(x, xs),  #find_closest(x, xs),
                                                #n_y_to_obj = find_closest(y, ys),
                                                )


    def draw_map(self) -> None:
        self.screen.fill("white")
        [o.draw(self.screen, self.draw_weights) for o in self.grid.values()]  
        #self.goal.draw(self.screen)
        # self.draw(self.start)
        pygame.display.flip()

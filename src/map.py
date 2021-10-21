

#basics
import numpy as np


# pygame
import pygame

# fastestpath
from .objects import Object
from .objects import GridBlock



def find_closest(q, keys):
    return min(keys, key = lambda x: abs(x-q))

class Map:

    def __init__(self, desc:str, map = "example1"):
        
        pygame.display.set_caption(desc)
        self.screen_width = 800
        self.screen_height = 600
        self.block_size = 20
        self.max_x = int(self.screen_width / self.block_size)
        self.max_y = int(self.screen_height / self.block_size)
    
        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))


        self.xy2wh = {}
        self.xy2obj = {}
        self.obsts = []
        self.goal =  None
        self.player = None
        self.grid = []

        self.__create_map()
        self.draw_map()

  
    def __example_map_1(self):

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

        for y in ys:
            for x in xs:
                obst = Object(
                                            x = int(x*self.block_size),
                                            y = int(y*self.block_size),
                                            width = self.block_size,
                                            height = self.block_size
                                            )

                self.xy2obj[(x,y)] = obst
                self.obsts.append(obst)
        
        x = int(self.max_x /2)
        self.goal = Object(
                                            x = int(x*self.block_size),
                                            y = self.block_size,
                                            width = self.block_size,
                                            height = self.block_size,
                                            color = "green",
                                            shape = "ellipse"
                                            )

        self.player = Object(
                                            x = int(x*self.block_size),
                                            y = (self.max_y-2)*self.block_size,
                                            width = self.block_size,
                                            height = self.block_size,
                                            color = "black",
                                            shape = "ellipse"
                                            )
        return xs, ys


    def __create_map(self):

        # create a map
        xs, ys = self.__example_map_1()

        for x, w in enumerate(range(0, self.screen_width, self.block_size)):
            for y, h in enumerate(range(0, self.screen_height, self.block_size)):
                self.xy2wh[(x,y)] = (w,h)

                if (x,y) in self.xy2obj:
                    continue

                self.xy2obj[(x,y)] = GridBlock(
                                                n_x_to_obj = find_closest(x, xs),
                                                n_y_to_obj = find_closest(y, ys)
                                                )


    def draw_map(self) -> None:
        self.screen.fill("white")
        [self.draw(o) for o in self.obsts]
        self.draw(self.goal)
        self.draw(self.player)
        pygame.display.flip()


    def draw(self, obj:Object):
        getattr(pygame.draw, obj.shape)(self.screen, obj.color, obj.rect)







    # def __create_random_map(self):
    
    #     random_xs = np.random.random_integers(0, self.x, 50)
    #     random_ys = np.random.random_integers(0, self.y, 50)
    #     obs_codinates = zip(random_xs, random_ys)

    #     obstacles = []
    #     for x,y in obs_codinates:
    #         obst = Object(
    #                     x = x,
    #                     y = y,
    #                     width = 50,
    #                     height = 50
    #                     )
    #         obstacles.append(obst)
    #         self.draw(obst)


    #     pygame.display.flip()



    # def __create_map(self, map:str):

    #     if map == "random":
    #         self.__create_random_map()

    #     elif map == "example1":
    #         self.__create_example_1_map()

    #     else:
    #         raise KeyError(f'"{map}" is not a supported map')
          # if draw:
                #     rect = pygame.Rect(w, h, self.block_size, self.block_size)
                #     pygame.draw.rect(self.screen, "black", rect, 1)


    # def __create_example_1_map(self):

    #     y = int(self.y / 2) # middle of the map
    #     first_wall_size = int(self.x * 0.4)
    #     gap_size = int(self.x * 0.1)
    #     second_wall_size = first_wall_size + gap_size + int(self.x * 0.25)

    #     # create the x coordinates for walls
    #     walls = list(range(0, first_wall_size)) + list(range(first_wall_size+gap_size, second_wall_size))

    #     for x in walls:
    #         print(x,y)
    #         obst = Object(
    #                     x = x,
    #                     y = y,
    #                     width = self.block_size * 2,
    #                     height = self.block_size * 5
    #                     )
    #         self.obsts.append(obst)
            

    #     #set goal
    #     self.goal = Object(
    #                     x = int(self.x * 0.45),
    #                     y = 0,
    #                     width = self.block_size,
    #                     height = self.block_size,
    #                     shape = "ellipse",
    #                     color = "red"
    #                 )

    #     # set start
    #     self.player = Object(
    #                     x = int(self.x * 0.45),
    #                     y = self.y,
    #                     width = self.block_size,
    #                     height = self.block_size,
    #                     shape = "ellipse",
    #                     color = "green"
    #                 )


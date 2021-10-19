

#basics
import numpy as np
import itertools


# pygame
import pygame

#
from .obstacle import Obstacle


class Map:

    def __init__(self, desc:str, difficulty: int):

        pygame.init()
        
        # Set up the display
        pygame.display.set_caption(desc)
        x = 800
        y = 700
        screen = pygame.display.set_mode((x, y))

        random_xs = np.random.random_integers(0, x, 50)
        random_ys = np.random.random_integers(0, y, 50)
        obs_codinates = zip(random_xs, random_ys)

        obstacles = []
        for x,y in obs_codinates:
            obst = Obstacle(
                        x = x,
                        y = y,
                        width = 50,
                        height = 50
                        )
            obstacles.append(obst)
            obst.draw(screen)

        pygame.display.flip()

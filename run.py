

import pygame

from src.map import Map
from src.algorithms.djikstra import Djikstra


if __name__ == "__main__":
    pygame.init()

    map = Map(
            desc = "Fastest Path", 
            map="example1",
            penalty_distance = 7
            )

    algo = Djikstra()

    while True:
        map.draw_map()
        algo.run(map)
    
 
    while True:
        pass

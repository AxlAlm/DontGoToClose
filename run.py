

#basics
import argparse
import random
import numpy as np

# pygame
import pygame

# fastest path
from src.map import Map
from src import algorithms


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-map", type = str, default = "example1")
    parser.add_argument("-max_distance", type = int, default = 5)
    parser.add_argument("-algo", type = str, default = "Djikstra")
    parser.add_argument("-penalty_cost", type = int, default = 5)
    parser.add_argument("-show_distance",  default = False, action = "store_true")
    parser.add_argument("-random_seed",  default = None, type = int)
    args = parser.parse_args()

    if args.random_seed is not None:
        random.seed(args.random_seed)
        np.random.seed(args.random_seed)

    # init pygame
    pygame.init()

    # create and draw map
    map = Map(
            desc = "Press 'Enter' to start!", 
            map = args.map,
            max_distance = args.max_distance,
            show_distance = args.show_distance,
            )
    map.draw_map()

    # set algo
    algo_class = getattr(algorithms, args.algo)

    while True:

        for event in pygame.event.get():

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_RETURN:
                algo = algo_class(map = map, penalty_cost = args.penalty_cost)
                algo.run()

            if event.key == pygame.K_BACKSPACE:
                map.draw_map()


            if event.key == pygame.K_ESCAPE:
                pygame.quit()



#basics

import argparse


# pygame
import pygame

# fastest path
from src.map import Map
from src.algorithms.djikstra import Djikstra


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-map", type = str, default = "example1")
    parser.add_argument("-max_distance", type = int, default = 5)
    parser.add_argument("-algo", type = str, default = "djikstra")
    parser.add_argument("-penalty_cost", type = int, default = 5)
    parser.add_argument("-show_distance",  default = False, action = "store_true")
    parser.add_argument("-run",  default = False, action = "store_true")
    args = parser.parse_args()


    pygame.init()

    map = Map(
            desc = "Fastest Path", 
            map = args.map,
            max_distance = args.max_distance,
            show_distance = args.show_distance,
            )

    if args.algo == "djikstra":
        algo = Djikstra(map = map, penalty_cost = args.penalty_cost)
    else:
        raise KeyError(f'"{args.aglo}"" is not a supported algo')


    while True:
        map.draw_map()

        if args.run:
            algo.run()
 
        while True:
            pass

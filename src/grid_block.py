
# basics
from typing import Tuple
from dataclasses import dataclass

#pygame 
import pygame


@dataclass
class GridBlock:

    #name and typ
    btype :str 

    # coordinats on the pygame.display
    x : int
    y : int

    # size of block
    width : int
    height : int

    #shap, color and screen
    shape : str
    color : str
    screen : pygame.display
    
    # norm_distance_to_wall
    dist_from_wall : float = 0.0

    # init shape and placement
    def __post_init__(self) -> None:
        assert self.btype in ["empty", "wall", "goal", "start"]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def fill(self, 
            color : str = None,
            shape : str = None,
            show_distance:bool = False,
            update : bool = False,
            ) -> None:

        # if we want to overwrite the shape and color
        color = color if color else self.color
        shape = shape if shape else self.shape

        if show_distance and self.btype == "empty":
            v = 255 * (1-self.dist_from_wall)
            color = (255, v, v)
    
        getattr(pygame.draw, shape)(self.screen, color, self.rect)

        if update:
            pygame.display.update()

# basics
from typing import Tuple
from dataclasses import dataclass

#pygame 
import pygame

@dataclass
class Object:
    x : int
    y : int
    width : int
    height : int
    shape : str = "rect"
    color : str = "purple"

    def __post_init__(self) -> None:
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 


# GridBlock is a class which will give information about where the closes object is 
@dataclass
class GridBlock:
    n_x_to_obj : int
    n_y_to_obj : int 



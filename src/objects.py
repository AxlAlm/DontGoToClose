
# basics
from typing import Tuple
from dataclasses import dataclass

#pygame 
import pygame


@dataclass
class GridBlock:
    x : int
    y : int
    width : int
    height : int
    shape : str
    color : str
    is_closed : bool = True
    is_goal : bool = False
    weight : float = 0.0

    def __post_init__(self) -> None:
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, screen: pygame.display, draw_weights:bool = False) -> None:

        if draw_weights and not self.is_closed:
            v = 255 * (1-self.weight)
            self.color = (255, v, v)

        getattr(pygame.draw, self.shape)(screen, self.color, self.rect)


    def draw_path(self, screen: pygame.display) -> None:
        getattr(pygame.draw, "ellipse")(screen, "purple", self.rect)
        pygame.display.update() 

    # def draw_weight(self, screen: pygame.display):
        
    #     # we only draw weights on open grids
    #     if self.is_close:
    #         return

    #     v = 255 * (1-self.weight)
    #     self.color = (255, v, v)
    #     super().draw(screen)









# # GridBlock is a class which will give information about where the closes object is 
# @dataclass
# class GridBlock:
#     x : int
#     y : int
#     width : int
#     height : int
#     penalty : float


#     def draw_weight(self, screen: pygame.display):
#         v = 255 * (1-self.penalty)
#         self.color = (255, v, v)
#         super().draw(screen)
    

#     def draw_path(self, screen: pygame.display):
#         getattr(pygame.draw, "rect")(screen, self.color, self.rect)
    





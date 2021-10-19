

#pygame 
import pygame

class Obstacle:


    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = y
        self.y = x
        self.width = width
        self.height = height
        self.shape = "rect"
        self.color = (0, 128, 64)
        self.rect = pygame.Rect(x, y, width, height)    

    def draw(self, screen):
        getattr(pygame.draw, self.shape)(screen, self.color, self.rect)




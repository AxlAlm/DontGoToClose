

# basics
from dataclasses import dataclass


@dataclass
class Object:

    x : float 
    y : float
    speed : float = 100


    def update_position(self, x:float ,y:float) -> None:
        self.x = x
        self.y = y
    
    def update_speed(self, speed:float) -> None:
        self.speed = speed
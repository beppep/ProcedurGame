import pygame
from roomClass import Room
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.xv = 0
        self.yv = 0
        self.mask = pygame.Rect(-16,-32,32,64)
        self.moveDir = 0
        self.turnDir = 1
        self.prevPressed = []
        #Curry, Ananas, Banan

    def update(self,pressed,room):
        if pressed[pygame.K_RIGHT] and (not pressed[pygame.K_LEFT] or not self.prevPressed[pygame.K_RIGHT]):
            self.moveDir = 1
            self.turnDir = 1
        if pressed[pygame.K_LEFT] and (not pressed[pygame.K_RIGHT] or not self.prevPressed[pygame.K_LEFT]):
            self.moveDir = -1
            self.turnDir = -1
        if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
            self.moveDir = 0

        self.xv += self.moveDir
        self.xv *= 0.9


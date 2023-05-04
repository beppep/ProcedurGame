import random
import pygame



class Weapon():

    def __init__(self, player):
        self.image = pygame.image.load("res/sword.png")
        self.image.set_colorkey((255,0,255))
        self.mask = pygame.Rect(-16,-16,32,32)
        self.player = player

    def draw(self,display,cameraX,cameraY):
        pos = (self.player.x-self.image.get_width()/2-cameraX + 50, self.player.y-self.image.get_height()/2-cameraY) #+50 is temporary
        display.blit(self.image, pos)
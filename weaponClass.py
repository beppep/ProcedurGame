import random
import pygame
from projectileClass import Projectile


class Weapon():

    def __init__(self, player):
        self.image = pygame.image.load("res/weapons/cannon.png")
        self.image.set_colorkey((255,0,255))
        self.mask = pygame.Rect(-16,-16,32,32)
        self.player = player
        self.cooldown = 30
        self.cooldownTimer = 0

    def update(self,pressed,world):
        if self.cooldownTimer>0:
            self.cooldownTimer -= 1
        else:
            if pressed[pygame.K_f]:
                self.attack(world)
                self.cooldownTimer = self.cooldown

    def attack(self,world):
        world.currentRoom.projectiles.append(Projectile(self.player))
        print(world.currentRoom.projectiles)

    def draw(self,display,cameraX,cameraY):
        pos = (self.player.x-self.image.get_width()/2-cameraX + 30*self.player.turnDir, self.player.y-self.image.get_height()/2-cameraY) #+50 is temporary
        display.blit(self.image, pos)
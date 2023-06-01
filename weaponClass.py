import random
import pygame
from projectileClass import Projectile
from constants import Constants


class Weapon():

    def __init__(self, player):
        self.image = Constants.loadImageTuple("res/weapons/cannon.png")
        self.mask = pygame.Rect(-32,-32,64,64)
        self.player = player
        self.cooldown = 20 + 30*random.random()
        self.cooldownTimer = 0

        self.projType = random.randint(0,9)

    def update(self,pressed,world):
        if self.cooldownTimer>0:
            self.cooldownTimer -= 1
        else:
            if pressed[pygame.K_f]:
                self.attack(world)
                self.cooldownTimer = self.cooldown

    def attack(self,world):
        world.currentRoom.projectiles.append(Projectile(self.player, Projectile.presets[self.projType]))
        #self.projType = random.randint(0,9)
        #print(world.currentRoom.projectiles)

    def draw(self,display,cameraX,cameraY):
        pos = (self.player.x-self.mask[2]/2-cameraX + 16*self.player.turnDir, self.player.y-self.mask[3]/2-cameraY) #+30 is temporary
        display.blit(self.image[self.player.turnDir], pos)
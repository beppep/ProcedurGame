import random
import pygame
from projectileClass import Projectile
from constants import Constants


class Weapon():

    def __init__(self, player):
        self.image = Constants.loadImageTuple("res/weapons/cannon.png")
        self.mask = pygame.Rect(-32,-32,64,64)
        self.player = player
        self.projType = random.randint(0,9)
        self.cooldown = 3+3*int(Projectile.presets[self.projType]["powerLevel"])
        self.cooldownTimer = 30


    def update(self,pressed,world):
        if self.cooldownTimer>0:
            self.cooldownTimer -= 1
        else:
            self.cooldownTimer = 0
            if pressed[pygame.K_f]:
                self.attack(world)
                self.cooldownTimer = self.cooldown

    def attack(self,world):
        world.currentRoom.projectiles.append(Projectile(self.player, Projectile.presets[self.projType]))
        #self.projType = random.randint(0,9)
        #print(world.currentRoom.projectiles)

    def draw(self,display,cameraX,cameraY):
        offsetX = 16 - 32*self.player.shielding
        offsetY = 16*self.player.shielding
        pos = (self.player.x+self.mask[0]-cameraX + offsetX*self.player.turnDir, offsetY + self.player.y+self.mask[1]-cameraY) #+30 is temporary
        display.blit(self.image[self.player.turnDir], pos)
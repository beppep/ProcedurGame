import pygame
import random
from roomClass import Room
from entityClass import Entity

class Enemy(Entity):

    # create 10 random enemy types
    presets = [] 
    for i in range(10):
        preset = {}
        preset["name"] = "Enemy "+str(i)
        preset["maxHealth"] = random.randint(1,random.randint(1,5))
        preset["gravity"] = random.random() * (random.random()<0.7)
        preset["speed"] = random.random() * (random.random()<0.9)
        presets.append(preset)


    def __init__(self,x,y,preset): # create enemy instance from preset
        super().__init__()
        self.x = x
        self.y = y
        self.mask = pygame.Rect(-16,-32,32,64)
        self.turnDir = 1
        self.maxHealth = preset["maxHealth"]
        self.health = self.maxHealth
        self.gravity = preset["gravity"]
        self.speed = preset["speed"]
        self.friction = 0.95
        self.jumpspeed = (self.gravity)**0.5 * 16
        self.image = pygame.image.load("res/enemies/onding.png")
        self.image.set_colorkey((255,0,255))
        self.dead = False

    def hurt(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.dead = True

    def update(self,world, player):
        if self.dead:
            return

        dirX = player.x - self.x
        dirY = player.y - self.y
        hyp = (dirX**2 + dirY**2)**0.5
        if hyp!=0:
            dirX = dirX/hyp
            dirY = dirY/hyp

        if dirX>0:
            self.turnDir = 1
        else:
            self.turnDir = -1
        self.xv += self.speed * dirX
        self.xv *= self.friction
        if self.gravity == 0:
            self.yv += self.speed * dirY
            self.yv *= self.friction

        if world.currentRoom.checkFree(self.mask,self.x,self.y+1):
            self.yv += self.gravity
        elif random.random()<0.01 and self.yv>=0:
            self.yv = -self.jumpspeed
        
        super().update(world)
        

    def draw(self,display,cameraX,cameraY):
        display.blit(self.image,(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))
            

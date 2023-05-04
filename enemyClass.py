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
        preset["gravity"] = random.random() * (random.random()>0.5)
        preset["xspeed"] = random.random() * (random.random()>0.5)
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
        self.xSpeed = preset["xspeed"]
        self.xFriction = 0.95
        self.jumpspeed = (self.gravity)**0.5 * 16
        self.image = pygame.image.load("res/hej.png")
        self.image.set_colorkey((255,0,255))

    def update(self,world, player):

        if player.x>self.x:
            self.turnDir = 1
        else:
            self.turnDir = -1
        self.xv += self.xSpeed * self.turnDir
        self.xv *= self.xFriction

        if world.currentRoom.checkFree(self.mask,self.x,self.y+1):
            self.yv += self.gravity
        elif random.random()<0.01 and self.yv >= 0:
            self.yv = -self.jumpspeed
        
        super().update(world)
        

    def draw(self,display,cameraX,cameraY):
        display.blit(self.image,(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))
            

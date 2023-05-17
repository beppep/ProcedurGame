import random
import pygame
from entityClass import Entity
from constants import Constants


class Projectile(Entity):


    # create projectile types
    presets = [] 
    for i in range(10):
        preset = {}
        preset["gravity"] = 0.5*random.random() * (random.random()<0.7)
        preset["speed"] = 1 + 20*random.random()
        preset["damage"] = 1 #+ random.random()
        preset["knockback"] = 10*random.random()
        presets.append(preset)

    def __init__(self, player, preset):
        super().__init__()
        self.image = Constants.loadImageTuple("res/weapons/arrow.png")
        self.mask = pygame.Rect(-32,-32,64,64)
        self.hitbox = pygame.Rect(-8,-4,16,8)
        self.player = player
        self.gravity = preset["gravity"]
        self.speed = preset["speed"]
        self.x = player.x
        self.y = player.y
        self.xv = player.turnDir*self.speed
        self.yv = -self.gravity*10
        self.turnDir = player.turnDir

        self.damage = preset["damage"]
        self.knockback = preset["knockback"]

    def update(self,world, player):
        dead = False

        self.yv += self.gravity

        for enemy in world.currentRoom.enemies:
            collision = self.checkCollision(enemy, selfHitbox = self.hitbox)
            if collision:
                enemy.hurt(self.damage, self.knockback*self.turnDir)
                dead = True
        if not world.currentRoom.checkFree(self.hitbox,self.x,self.y+1):
            dead = True
        
        super().update(world)

        return dead # return True to not delete projectile


    def draw(self,display,cameraX,cameraY):

        display.blit(self.image[self.turnDir], (self.x+self.mask[0]-cameraX, self.y+self.mask[1]-cameraY))

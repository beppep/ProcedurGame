import random
import pygame
from entityClass import Entity


class Projectile(Entity):

    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("res/weapons/arrow.png")
        self.image.set_colorkey((255,0,255))
        self.mask = pygame.Rect(-16,-16,32,32)
        self.hitbox = pygame.Rect(-8,-4,16,8)
        self.player = player
        self.x = player.x
        self.y = player.y
        self.xv = player.turnDir*10
        self.yv = -2
        self.gravity = 0.2

    def update(self,world, player):
        dead = False

        self.yv += self.gravity

        for enemy in world.currentRoom.enemies:
            collision = self.checkCollision(enemy, selfHitbox = self.hitbox)
            if collision:
                enemy.hurt(1)
                dead = True
        if not world.currentRoom.checkFree(self.mask,self.x,self.y+1):
            dead = True
        
        super().update(world)

        return dead # return True to not delete projectile


    def draw(self,display,cameraX,cameraY):

        display.blit(self.image, (self.x+self.mask[0]-cameraX, self.y+self.mask[1]-cameraY))

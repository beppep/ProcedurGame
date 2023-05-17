import pygame
import random
from roomClass import Room
from entityClass import Entity
from weaponClass import Weapon
from constants import Constants

class Player(Entity):

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.mask = pygame.Rect(-32,-32,64,64)
        self.hitbox = pygame.Rect(-16,-32,32,64)
        self.moveDir = 0
        self.xSpeed = 0.5 + 0.5*random.random()
        self.xFriction = 0.9 + 0.05*random.random()
        self.gravity = 0.3+0.5*random.random()
        self.jumpspeed = (self.gravity)**0.5 * 16
        self.prevPressed = []
        self.image = Constants.loadImageTuple("res/hej.png")
        self.maxHealth = random.randint(4,5)
        self.health = self.maxHealth
        self.weapon = Weapon(self)

    def update(self,pressed,world):
        if len (self.prevPressed) > 0:
            if pressed[pygame.K_RIGHT] and (not pressed[pygame.K_LEFT] or not self.prevPressed[pygame.K_RIGHT]):
                self.moveDir = 1
                self.turnDir = 1
            if pressed[pygame.K_LEFT] and (not pressed[pygame.K_RIGHT] or not self.prevPressed[pygame.K_LEFT]):
                self.moveDir = -1
                self.turnDir = -1
            if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                self.moveDir = 0
        self.prevPressed = pressed
        self.xv += self.moveDir*self.xSpeed
        self.xv *= self.xFriction

        if world.currentRoom.checkFree(self.hitbox,self.x,self.y+1):
            self.yv += self.gravity
        elif pressed[pygame.K_SPACE] and self.yv >= 0:
            self.yv = -self.jumpspeed

        self.weapon.update(pressed,world)
        
        super().update(world)

        if self.x<0:
            success = world.tryMovePlayer(-1,0)
            if success:
                world.currentRoom.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
                self.x = world.currentRoom.width
                self.y = 100
            else:
               self.x = 0
        if self.x>world.currentRoom.width:
            success = world.tryMovePlayer(1,0)
            if success:
                world.currentRoom.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
                self.x = 0
                self.y = 100
            else:
                self.x = world.currentRoom.width
                
        if abs(self.x - world.currentRoom.width/4) < 30 and pressed[pygame.K_UP]:
            if (world.tryMovePlayer(0,-1)):
                world.currentRoom.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
                self.x += world.currentRoom.width/2
                self.y -= 96
        elif abs(self.x - 3*world.currentRoom.width/4) < 30 and pressed[pygame.K_DOWN]:
            if (world.tryMovePlayer(0,1)):
                world.currentRoom.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
                self.x -= world.currentRoom.width/2
                self.y -= 96
        
                

    def draw(self,display,cameraX,cameraY):
        display.blit(self.image[self.turnDir],(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))
        if self.weapon:
            self.weapon.draw(display,cameraX,cameraY)
            

import pygame
import random
from roomClass import Room
from entityClass import Entity
from weaponClass import Weapon
from constants import Constants

class Player(Entity):

    ISPLAYER = True

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.mask = pygame.Rect(-32,-32,64,64)
        self.hitbox = pygame.Rect(-16,-32,32,64)
        self.moveDir = 0
        self.xSpeed = 0.5 + 0.5*random.random()
        self.xFriction = 0.8 + 0.1*random.random()
        self.gravity = 0.3+0.5*random.random()
        self.jumpspeed = (self.gravity)**0.5 * 16
        self.prevPressed = []
        self.image = Constants.loadImageTuple("res/hej.png")
        self.shieldImage = Constants.loadImageTuple("res/weapons/shield.png")
        self.maxHealth = random.randint(8,10)
        self.health = self.maxHealth
        self.weapon = Weapon(self)
        self.shield = True
        self.shielding = False
        self.dashes = 0
        self.dashTime = 0

    def hurt(self, dmg, knockback=0):
        if self.shielding:
            return False
        else:
            self.health -= dmg
            self.yv = - abs(knockback)*0.3
            self.xv += knockback
            if self.health <= 0:
                self.dead = True

    def update(self,pressed,world):
        if self.dashTime>0:
            self.dashTime -= 1
            if self.dashTime<=0:
                self.xv *= 0.5
                self.yv *= 0.2
        else:
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
            else:
                self.dashes = 1
                if pressed[pygame.K_SPACE] and self.yv >= 0:
                    self.yv = -self.jumpspeed

            if pressed[pygame.K_LSHIFT] and self.dashes>0:
                dx = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
                dy = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]
                if dx != 0 or dy != 0:
                    self.dashes = 0
                    self.xv = dx * 20
                    self.yv = dy * 20
                    self.dashTime = 10
            if pressed[pygame.K_g] and not self.weapon.cooldownTimer>0:
                self.shielding = True
            else:
                self.shielding = False

        self.weapon.update(pressed,world)
            
        super().update(world)

        if self.x<0:
            success = world.tryMovePlayer(-1,0)
            if success:
                self.x = world.currentRoom.width
                self.y = 100
            else:
               self.x = 0
        if self.x>world.currentRoom.width:
            success = world.tryMovePlayer(1,0)
            if success:
                self.x = 0
                self.y = 100
            else:
                self.x = world.currentRoom.width
                
        if abs(self.x - world.currentRoom.width/4) < 30 and pressed[pygame.K_UP]:
            if (world.tryMovePlayer(0,-1)):
                self.x += world.currentRoom.width/2
                self.y -= 96
        elif abs(self.x - 3*world.currentRoom.width/4) < 30 and pressed[pygame.K_DOWN]:
            if (world.tryMovePlayer(0,1)):
                self.x -= world.currentRoom.width/2
                self.y -= 96
        
                

    def draw(self,display,cameraX,cameraY):
        w = 200
        pygame.draw.rect(display, (255, 0, 0), (20,22,int(w),20), 0)
        pygame.draw.rect(display, (0, 255, 0), (20,20,int(self.health/self.maxHealth*w),24), 0)

        display.blit(self.image[self.turnDir],(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))
        if self.weapon:
            self.weapon.draw(display,cameraX,cameraY)
        if self.shield:
            offsetX = -16 + 32*self.shielding
            offsetY = 16*(not self.shielding)
            display.blit(self.shieldImage[self.turnDir],(self.x+self.mask[0]-cameraX + self.turnDir*offsetX, offsetY + self.y+self.mask[1]-cameraY))
            

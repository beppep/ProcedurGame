import pygame
import random
from roomClass import Room
from entityClass import Entity
from constants import Constants
from projectileClass import Projectile

class Enemy(Entity):

    imagePaths = ["res/enemies/onding.png","res/enemies/enemy2.png","res/enemies/hej.png","res/enemies/wizard.png"]
    images = []
    for i in range(10):
        images.append(Constants.loadImageTuple(random.choice(imagePaths)))

    # create 10 random enemy types
    presets = [] 
    for i in range(10):
        preset = {}
        preset["name"] = "Enemy "+str(i)
        preset["maxHealth"] = random.randint(1,random.randint(1,5))
        preset["gravity"] = random.random() * (random.random()<0.7)
        preset["speed"] = 0.5*random.random()
        preset["imageNumber"] = random.randint(0,len(images)-1)
        preset["projType"] = random.randint(0,9)
        preset["morphs"] = (random.random()<0.5) # as opposed to summoner

        preset["powerLevel"] = preset["maxHealth"]*(preset["speed"]+Projectile.presets[preset["projType"]]["powerLevel"])
        print(preset["powerLevel"]) # about 3 - 100
        presets.append(preset)
    presets.sort(key = lambda x:x["powerLevel"])
    for p in range(len(presets)):
        if p>0:
            presets[p]["summonType"] = random.randint(0,9)
            while presets[p]["summonType"] >= p and presets[presets[p]["summonType"]]["morphs"]==False: # can morph into morphs powercreatures or lower level creatures
                presets[p]["summonType"] = random.randint(0,9)
        else:
            presets[p]["summonType"] = -1

    def __init__(self,x,y,preset): # create enemy instance from preset
        super().__init__()
        self.x = x
        self.y = y
        self.mask = pygame.Rect(-32,-32,64,64)
        self.hitbox = pygame.Rect(-16,-32,32,64)
        self.preset = preset
        self.maxHealth = preset["maxHealth"]
        self.health = self.maxHealth
        self.gravity = preset["gravity"]
        self.speed = preset["speed"]
        self.friction = 0.9
        self.jumpspeed = (self.gravity)**0.5 * 16
        self.imageNumber = preset["imageNumber"]
        self.cooldown = 60
        self.cooldownTimer = 60
        self.dead = False

    def hurt(self, dmg, knockback=0):
        self.health -= dmg
        self.yv = - abs(knockback)*0.3
        self.xv += knockback
        if self.health <= 0:
            self.dead = True

    def attack(self, world):
        world.currentRoom.projectiles.append(Projectile(self, Projectile.presets[self.preset["projType"]]))

    def update(self,world, player):
        if self.dead:
            return

        if self.cooldownTimer>0:
            self.cooldownTimer -= 1
        else:
            if random.random()<0.01:
                self.attack(world)
                self.cooldownTimer = self.cooldown

            elif random.random()<0.002 and len(world.currentRoom.enemies)<20 and self.preset["summonType"]>=0:
                self.dead = self.preset["morphs"]
                newEnemy = Enemy(self.x, self.y, self.presets[self.preset["summonType"]])
                if self.preset["morphs"]:
                    newEnemy.health = (self.health/self.maxHealth)*newEnemy.maxHealth
                world.currentRoom.enemies.append(newEnemy)
                self.cooldownTimer = self.cooldown*2


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

        if world.currentRoom.checkFree(self.hitbox,self.x,self.y+1):
            self.yv += self.gravity
        elif random.random()<0.01 and self.yv>=0:
            self.yv = -self.jumpspeed
        
        super().update(world)
        

    def draw(self,display,cameraX,cameraY):
        if self.health < self.maxHealth:
            w = self.maxHealth*20
            pygame.draw.rect(display, (255, 0, 0), (int(self.x-w/2-cameraX),int(self.y+self.mask[1]-cameraY +1),int(w),6), 0)
            pygame.draw.rect(display, (0, 255, 0), (int(self.x-w/2-cameraX),int(self.y+self.mask[1]-cameraY),int(self.health/self.maxHealth*w),8), 0)

        display.blit(self.images[self.imageNumber][self.turnDir],(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))
            

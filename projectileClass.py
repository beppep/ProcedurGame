import random
import pygame
from entityClass import Entity
from constants import Constants


class Projectile(Entity):


    imagePaths = ["res/projectiles/arrow.png","res/projectiles/ball.png","res/projectiles/blixt.png"]
    images = []
    for i in range(10):
        images.append(Constants.loadImageTuple(random.choice(imagePaths)))

    # create projectile types
    presets = [] 
    for i in range(10):
        preset = {}
        preset["gravity"] = 0.5*random.random() * (random.random()<0.7)
        preset["speed"] = 2 + 20*random.random()
        preset["maxAge"] = random.randint(30,300)
        preset["damage"] = 0.1 + random.random()
        preset["knockback"] = 10*random.random()
        preset["imageNumber"] = random.randint(0,len(images)-1)
        preset["sandgun"] = (random.random()<0.01)

        preset["powerLevel"] = preset["damage"]*(preset["knockback"]+preset["speed"])
        #print(preset["powerLevel"]) # about 0 - 20
        presets.append(preset)
    presets.sort(key = lambda x:x["powerLevel"])

    def __init__(self, owner, preset):
        super().__init__()
        self.mask = pygame.Rect(-32,-32,64,64)
        self.hitbox = pygame.Rect(-8,-4,16,8)
        self.owner = owner
        self.evil = not hasattr(owner, "ISPLAYER")
        self.preset = preset
        self.gravity = preset["gravity"]
        self.speed = preset["speed"]
        self.age = 0
        self.x = owner.x
        self.y = owner.y
        self.xv = owner.xv + owner.turnDir*self.speed
        self.yv = owner.yv*0.4 + -self.gravity*10
        self.turnDir = owner.turnDir
        self.damage = preset["damage"]
        self.knockback = preset["knockback"]
        self.imageNumber = preset["imageNumber"]
        self.maxAge = preset["maxAge"]

    def update(self,world, player):
        self.age += 1
        dead = False
        if self.age > self.preset["maxAge"]:
            dead = True

        self.yv += self.gravity

        if self.evil:
            collision = self.checkCollision(player, selfHitbox = self.hitbox)
            if collision and not player.dashTime>0:
                player.hurt(self.damage, self.knockback*self.turnDir)
                dead = True
        else:
            for enemy in world.currentRoom.enemies:
                collision = self.checkCollision(enemy, selfHitbox = self.hitbox)
                if collision:
                    enemy.hurt(self.damage, self.knockback*self.turnDir)
                    dead = True

        if not world.currentRoom.checkFree(self.hitbox,self.x-1,self.y+1):
            dead = True
        if not world.currentRoom.checkFree(self.hitbox,self.x+1,self.y+1):
            dead = True
        
        super().update(world)

        if dead and self.preset["sandgun"]:
            world.currentRoom.click(self.x, self.y)

        return dead # return True to not delete projectile


    def draw(self,display,cameraX,cameraY):

        display.blit(self.images[self.imageNumber][self.turnDir], (self.x+self.mask[0]-cameraX, self.y+self.mask[1]-cameraY))

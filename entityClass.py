import pygame
from roomClass import Room
from constants import Constants

class Entity:
    
    def __init__(self):
        self.x = 100
        self.y = 100
        self.xv = 0
        self.yv = 0
        self.turnDir = 1
        self.mask = pygame.Rect(-16,-32,32,64)
        self.hitbox = self.mask

    def update(self,world):

        #Kollar kollisioner i x och y led.
        #Om det finns en kollision, stega pixelvis tills vi når fram till hindret, sätt hastighet till 0
        if not world.currentRoom.checkFree(self.hitbox,self.x+self.xv,self.y+self.yv):
            # Vi bromsar hellre i y-led än i x-led
            # Om det är fritt i x-led eller blockerat i både x- och y-led, stega först i y-riktningen
            xfree = world.currentRoom.checkFree(self.hitbox,self.x+self.xv,self.y)
            if xfree or (not world.currentRoom.checkFree(self.hitbox,self.x,self.y+self.yv) and not world.currentRoom.checkFree(self.hitbox,self.x+self.xv,self.y)):
                self.y = int(self.y)
                sign = (self.yv > 0)*2 -1
                for i in range(int(abs(self.yv*1.5))):
                    if world.currentRoom.checkFree(self.hitbox,self.x+self.xv*xfree,self.y + sign):
                        self.y += sign
                    else:
                        break
                self.yv = 0
            # Om det fortfarande inte är fritt, stega nu i x-riktningen
            if not world.currentRoom.checkFree(self.hitbox,self.x + self.xv,self.y + self.yv):
                self.x = int(self.x)
                sign = (self.xv > 0)*2-1
                for i in range(int(abs(self.xv*1.5))):
                    if world.currentRoom.checkFree(self.hitbox,self.x+sign,self.y + self.yv):
                        self.x += sign
                    else:
                        break
                self.xv = 0
            
        self.x += self.xv
        self.y += self.yv

    def checkCollision(self,other, selfHitbox=None):
        if selfHitbox == None:
            selfHitbox = self.hitbox
        selfLeft, selfTop = self.x+selfHitbox[0], self.y+selfHitbox[1]
        otherLeft, otherTop = other.x+other.hitbox[0], other.y+other.hitbox[1]
        if selfLeft<otherLeft+other.hitbox[2] and selfLeft+selfHitbox[2]>otherLeft:
            if selfTop<otherTop+other.hitbox[3] and selfTop+selfHitbox[3]>otherTop:
                return True

    def draw(self,display,cameraX,cameraY):
        display.blit(self.image[self.turnDir],(self.x+self.hitbox[0]-cameraX,self.y+self.hitbox[1]-cameraY))
            

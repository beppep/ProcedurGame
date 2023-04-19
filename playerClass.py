import pygame
import random
from roomClass import Room
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.xv = 0
        self.yv = 0
        self.mask = pygame.Rect(-16,-32,32,64)
        self.moveDir = 0
        self.turnDir = 1
        self.xSpeed = 0.5 + 0.5*random.random()
        self.xFriction = 0.9 + 0.05*random.random()
        self.gravity = 0.3+0.5*random.random()
        self.jumpspeed = (self.gravity)**0.5 * 16
        #self.yFriction = 0.95 + 0.05*random.random() pls no
        self.prevPressed = []
        self.image = pygame.image.load("res/hej.png")
        self.image.set_colorkey((255,0,255))
        #Curry, Ananas, Banan

    def update(self,pressed,room):
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

        if room.checkFree(self.mask,self.x,self.y+1):
            self.yv += self.gravity
        elif pressed[pygame.K_UP] and self.yv >= 0:
            self.yv = -self.jumpspeed
        
        #self.yv *= self.yFriction pls no

        #Kollar kollisioner i x och y led.
        #Om det finns en kollision, stega pixelvis tills vi når fram till hindret, sätt hastighet till 0
        if not room.checkFree(self.mask,self.x+self.xv,self.y+self.yv):
            # Vi bromsar hellre i y-led än i x-led
            # Om det är fritt i x-led eller blockerat i både x- och y-led, stega först i y-riktningen
            if room.checkFree(self.mask,self.x+self.xv,self.y) or (not room.checkFree(self.mask,self.x,self.y+self.yv) and not room.checkFree(self.mask,self.x+self.xv,self.y)):
                self.y = int(self.y)
                sign = (self.yv > 0)*2 -1
                for i in range(int(abs(self.yv*1.5))):
                    if room.checkFree(self.mask,self.x+self.xv,self.y + sign):
                        self.y += sign
                    else:
                        break
                self.yv = 0
            # Om det fortfarande inte är fritt, stega nu i x-riktningen
            if not room.checkFree(self.mask,self.x + self.xv,self.y + self.yv):
                self.x = int(self.x)
                sign = (self.xv > 0)*2-1
                for i in range(int(abs(self.xv*1.5))):
                    if room.checkFree(self.mask,self.x+sign,self.y + self.yv):
                        self.x += sign
                    else:
                        break
                self.xv = 0
            
        self.x += self.xv
        self.y += self.yv



        if self.x<0:
            pass

    def draw(self,display,cameraX,cameraY):
        display.blit(self.image,(self.x+self.mask[0]-cameraX,self.y+self.mask[1]-cameraY))


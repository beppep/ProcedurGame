import time
import random
import pygame
import os
from roomClass import Room
clock = pygame.time.Clock()



gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Yo Game")
room = Room(100,20)

pressed = pygame.key.get_pressed()
jumpOut = False
camera = [0,0]
while jumpOut == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jumpOut = True
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        camera[1] -= 2
    if pressed[pygame.K_DOWN]:
        camera[1] += 2
    if pressed[pygame.K_LEFT]:
        camera[0] -= 2
    if pressed[pygame.K_RIGHT]:
        camera[0] += 2
    

    gameDisplay.fill((100,100,200))
    room.draw(gameDisplay,camera[0],camera[1],1000,600)
    pygame.display.update()
    clock.tick(60)
    
    
pygame.quit()
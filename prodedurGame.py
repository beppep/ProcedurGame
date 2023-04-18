import time
import random
import pygame
import os
from roomClass import Room
from playerClass import Player
clock = pygame.time.Clock()



gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Yo Game")
room = Room(100,20)

player = Player()

pressed = pygame.key.get_pressed()
jumpOut = False
camera = [0,0]
while jumpOut == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jumpOut = True
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                room.click(pos[0]+camera[0],pos[1]+ camera[1])
    if pressed[pygame.K_w]:
        camera[1] -= 2
    if pressed[pygame.K_s]:
        camera[1] += 2
    if pressed[pygame.K_a]:
        camera[0] -= 2
    if pressed[pygame.K_d]:
        camera[0] += 2
    
    player.update(pressed,room)
    gameDisplay.fill((100,100,200))
    room.draw(gameDisplay,camera[0],camera[1],1000,600)
    player.draw(gameDisplay,camera[0],camera[1])
    pygame.display.update()
    clock.tick(60)
    
    
pygame.quit()
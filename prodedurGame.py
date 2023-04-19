import time
import random
import pygame
import os
screenWidth = 1000
screenHeight = 600
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
from roomClass import Room
from playerClass import Player
from betterWorldClass import World
clock = pygame.time.Clock()


pygame.display.set_caption("Yo Game")
room = Room(100,20)

player = Player()

worldSize = 50
world = World(worldSize,worldSize)
room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
pressed = pygame.key.get_pressed()
jumpOut = False
camera = [0,0]
worldVisible = True
while jumpOut == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jumpOut = True
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                world = World(worldSize,worldSize)
                room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
            if event.key == pygame.K_t:
                worldVisible = not worldVisible

            if event.key == pygame.K_a:
                world.tryMovePlayer(-1,0)
                room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
            if event.key == pygame.K_s:
                world.tryMovePlayer(0,1)
                room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
            if event.key == pygame.K_w:
                world.tryMovePlayer(0,-1)
                room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
            if event.key == pygame.K_d:
                world.tryMovePlayer(1,0)
                room.updateBackground(world,world.playerCoords[1],world.playerCoords[0])
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                room.click(pos[0]+camera[0],pos[1]+ camera[1])
    camera = [player.x-screenWidth/2,player.y-screenHeight/2] 
    if pressed[pygame.K_w]:
        camera[1] -= 50
    if pressed[pygame.K_s]:
        camera[1] += 50
    if pressed[pygame.K_a]:
        camera[0] -= 50
    if pressed[pygame.K_d]:
        camera[0] += 50
    camera[0] = max(0,min(camera[0],room.width-screenWidth))
    camera[1] = max(0,min(camera[1],room.height-screenHeight))
    
    player.update(pressed,room)
    gameDisplay.fill((180,200,250))
    room.draw(gameDisplay,camera[0],camera[1],1000,600)
    player.draw(gameDisplay,camera[0],camera[1])
    #world.drawMap(gameDisplay)
    if worldVisible:
        world.draw(gameDisplay)
    pygame.display.update()
    clock.tick(60)
    
    
pygame.quit()
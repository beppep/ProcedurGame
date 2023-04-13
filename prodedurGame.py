import time
import random
import pygame
import os
clock = pygame.time.Clock()


gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Yo Game")


jump_out = False
while jump_out == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True

    gameDisplay.fill((100,100,200))

    pygame.display.update()
    clock.tick(60)
    
    
pygame.quit()
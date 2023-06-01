import pygame
import random


class Constants():

    water = 0
    beach = 1
    cliffs = 2
    plains = 3
    woods = 4

    colors = { water: (10,30,200) , 
              beach : (235,225,70), 
              cliffs : (70,50,50),
              plains : (70,255,70),
              woods : (30,170,30)}

    def loadImageTuple(path, colorVariation = True):
        img = pygame.image.load(path)
        img.set_colorkey((255,0,255))

        if colorVariation:
            colorVariation = random.randint(1,6)
            for i in range(64):
                for j in range(64):
                    color = img.get_at((i,j))
                    if not color == (255,0,255,255):
                        if colorVariation<3:
                            color=pygame.Color(color[(0+colorVariation)%3],color[(1+colorVariation)%3],color[(2+colorVariation)%3],color[3])
                            img.set_at((i,j),color)
                        else:
                            color=pygame.Color(color[(2+colorVariation)%3],color[(1+colorVariation)%3],color[(0+colorVariation)%3],color[3])
                            img.set_at((i,j),color)

        flippedImg = pygame.transform.flip(img,True,False)
        flippedImg.set_colorkey((255,0,255))
        return [None, img, flippedImg] # for self.turnDir indexing
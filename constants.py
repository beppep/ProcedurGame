import pygame


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

    def loadImageTuple(path):
        img = pygame.image.load(path)
        img.set_colorkey((255,0,255))
        flippedImg = pygame.transform.flip(img,True,False)
        flippedImg.set_colorkey((255,0,255))

        return [None, img, flippedImg] # for self.turnDir indexing
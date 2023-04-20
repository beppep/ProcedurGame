import pygame
import random

from constants import Constants
from roomClass import Room

class World:
    
    def __init__(self,width,height,seed = None):
        self.rand = random.Random()
        if seed != None:
            self.rand.seed(seed)
        self.seed = seed
        self.width = width
        self.height = height

        medgrid = []
        self.heightGrid = []
        self.zoneGrid = []

        ratio = 0.5
        stddev = 5

        for i in range(height):
            self.heightGrid.append([0]*width)
            self.zoneGrid.append([0]*width)
            medgrid.append([0]*width)
            for j in range(width):
                
                self.heightGrid[i][j] = self.rand.gauss(0,stddev)
                self.heightGrid[i][j] += min(120*(1/6 - (i/height - 1/2)**2 - (j/width - 1/2)**2),stddev*ratio)
                
        
        kerWidth = 3
        kerHeight = 3
        kerDiv = kerWidth*kerHeight
        for i in range(self.height-kerHeight +1):
            for j in range(self.width-kerWidth +1):
                med = 0
                for ii in range(i,i+kerHeight):
                    for jj in range(j,j+kerWidth):
                        med += self.heightGrid[ii][jj] / kerDiv
                for ii in range(i,i+kerHeight):
                    for ji in range(j,j+kerWidth):  
                        medgrid[ii][jj] += med/kerDiv
        self.heightGrid = medgrid

        for i in range(self.height):
            for j in range(self.width):
                self.heightGrid[i][j] = max(0,self.heightGrid[i][j])
                if self.heightGrid[i][j] <= 0:
                    self.zoneGrid[i][j] = Constants.water
                elif self.heightGrid[i][j] <= stddev/2:
                    count = self.countWater(i,j)
                    if count == 0:
                        self.zoneGrid[i][j] = Constants.plains
                    elif count < 3 or (count == 3 and self.rand.randint(0,1)):
                        self.zoneGrid[i][j] = Constants.beach
                        self.heightGrid[i][j] /=5
                    else:
                        self.zoneGrid[i][j] = Constants.cliffs
                        self.heightGrid[i][j] += 2  
                elif self.heightGrid[i][j] <= stddev*2/3:
                    count = self.countWater(i,j)
                    if count == 0:
                        self.zoneGrid[i][j] = Constants.woods
                    else:
                        self.zoneGrid[i][j] = Constants.cliffs
                        self.heightGrid[i][j] += 4
                else:
                    self.zoneGrid[i][j] = Constants.cliffs
                    self.heightGrid[i][j] += 4

        self.surf = pygame.Surface((width*5*2,height*5))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(self.surf,(10,max(0,min(40*self.heightGrid[i][j],255)),200*(self.heightGrid[i][j]<=0)),(j*5,i*5,5,5),0)
                pygame.draw.rect(self.surf,Constants.colors[self.zoneGrid[i][j]],((j+self.width)*5,i*5,5,5),0)
        
        done = False
        while(not done):
            self.playerCoords = (self.rand.randint(1,self.width-1),self.rand.randint(1,self.height-1))
            done = self.zoneGrid[self.playerCoords[1]][self.playerCoords[0]] == Constants.beach

        self.roomGrid = []
        for y in range(height):
            self.roomGrid.append([0]*width)
            for x in range(width):
                self.roomGrid[y][x] = Room(100,20)
        self.currentRoom = self.roomGrid[self.playerCoords[1]][self.playerCoords[0]]
        self.currentRoom.updateBackground(self,self.playerCoords[1],self.playerCoords[0])

    def countWater(self,row,col):
        checkPos = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]
        count = 0
        for pos in checkPos:
            if pos[0] < 0 or pos[0] >= self.height or pos[1] < 0 or pos[1] >= self.width:
                count += 1
            elif self.heightGrid[pos[0]][pos[1]] <= 0:
                count += 1
        return count
    
    def tryMovePlayer(self,dx,dy):
        newRow = self.playerCoords[1] + dy
        newCol = self.playerCoords[0] + dx
        if newRow < 0 or newCol < 0 or newRow >= self.height or newCol >= self.width:
            return False
        if self.zoneGrid[newRow][newCol] == Constants.water:
            return False
        self.playerCoords=(newCol,newRow)
        return True

    def draw(self,display):
        display.blit(self.surf,(0,0))
        pygame.draw.rect(display,(255,255,255),(self.playerCoords[0]*5,self.playerCoords[1]*5,5,5),1)
        

        
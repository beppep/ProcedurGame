import pygame
import random
class Room():

    hillImages = []
    hillImages.append(pygame.image.load("res/hill.png"))
    hillImages[0].set_colorkey((255,0,255))
    for i in range (3,11):
        surf = pygame.transform.scale(hillImages[0],(800/i,800/i))
        surf.set_colorkey((255,0,255))
        hillImages.append(surf)
        
    
    def __init__ (self,width,height):
        self.seed = 10234789
        self.grid = []
        self.blockWidth = 32
        """
        for i in range(height):
            self.grid.append([i == (height - 1)]*width)
        """
        self.width = width*self.blockWidth
        self.height = height*self.blockWidth
        self.rows = height
        self.cols = width
        self.generateSand()

    
    def checkFree(self,rectangle,xdisp = 0,ydisp = 0):
        startRow = max(int(rectangle[1] + ydisp)//self.blockWidth,0)
        endRow = min(int(rectangle[1] + rectangle[3]-1 + ydisp)//self.blockWidth + 1 ,len(self.grid))
        startCol = max(int(rectangle[0] + xdisp)//self.blockWidth,0)
        endCol = min(int(rectangle[0] + rectangle[2]-1 + xdisp)//self.blockWidth + 1 ,len(self.grid[0]))
        for i in range(startRow,endRow):
            for j in range(startCol,endCol):
                if self.grid[i][j]:
                    return False 
        return True
    
    def click(self,x,y):
        row = int(y//self.blockWidth)
        col = int(x//self.blockWidth)
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return
        self.grid[row][col] = not self.grid[row][col]
    
    def draw(self,display,cameraX,cameraY,cameraWidth,cameraHeight):
        #Draw ocean/horizon
        pygame.draw.rect(display, (10,10,200),(0,cameraHeight/2,cameraWidth,cameraHeight),0)

        for i in range(len(Room.hillImages)-1):
            ind = len(Room.hillImages)-1-i
            surf = Room.hillImages[ind]
            w = surf.get_width()
            offSet = (1037*i) % 159
            setX = cameraWidth/2-cameraX/(ind+2) + offSet
            startInd = -int(setX//w) - 1
            endInd = startInd + int(cameraWidth//w) + 2
            
            for j in range(startInd,endInd):
                display.blit(Room.hillImages[ind],(j*w+setX,cameraHeight/2-cameraY/(ind+2)))

        startRow = int(cameraY)//self.blockWidth 
        startCol = int(cameraX)//self.blockWidth 

        for row in range(max(0,startRow),min(startRow+cameraHeight//self.blockWidth + 2,len(self.grid))):
            gridRow = self.grid[row]
            for col in range(max(0,startCol),min(startCol+cameraWidth//self.blockWidth + 2,len(self.grid[0]))):
                if gridRow[col]:
                    pygame.draw.rect(display, (200,200,200), (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 0)
                #pygame.draw.rect(display, (0,0,0), (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 1)


    def generateSand(self):
        lo = 6
        hi = 10
        sandHeight = 8
        for row in range(self.rows):
            self.grid.append([0]*self.cols)
        for x in range(self.cols):
            if random.random()<0.1:
                downchance = (sandHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    sandHeight-=1
                else:
                    sandHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = 1*(self.rows-1-y<sandHeight)

    def updateBackground(self,world,row,col):
        visibleCells = []
        cellHeights = []


        for i in range(row):
            visibleCells.append([0]*(2*i+1))
            cellHeights.append([0]*(2*i+1))


        


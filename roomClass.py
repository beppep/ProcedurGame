import pygame
class Room():
    def __init__ (self,width,height):
        self.seed = 10234789
        self.grid = []
        self.blockWidth = 32
        for i in range(height):
            self.grid.append([i == (height - 1)]*width)
    
    def checkFree(rectangle,xdisp = 0,ydisp = 0):
        return ":)"
    
    def draw(self,display,cameraX,cameraY,cameraWidth,cameraHeight):
        startRow = cameraY//self.blockWidth 
        startCol = cameraX//self.blockWidth 

        for row in range(max(0,startRow),min(startRow+cameraHeight//self.blockWidth + 2,len(self.grid))):
            gridRow = self.grid[row]
            for col in range(max(0,startCol),min(startCol+cameraWidth//self.blockWidth + 2,len(self.grid[0]))):
                color = (200,200,200) if gridRow[col] else (255,255,255)
                pygame.draw.rect(display, color, (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 0)
                pygame.draw.rect(display, (0,0,0), (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 1)
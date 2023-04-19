import pygame
import random

from betterWorldClass import World
class Room():


    #Init some background stuff. Images in different sizes
    backStartInd = -1 # Found out through trial and error
    backGroupWidth = 4 # images at indices -1 ,0 ,1, 2 represent landscape of cell directly north of room
    #(Indices here refers to inds computed in the draw method (j))
    #Only applies if images are approximately 400 pixels wide
    #TODO(?) make these values dependent on image width. (may need one value per image :( )



    hillImages = []
    hillImages.append(pygame.image.load("res/hill.png"))
    hillImages[0].set_colorkey((255,0,255))
    w = hillImages[0].get_width()
    h = hillImages[0].get_height()

    for i in range (3,11):
        surf = pygame.transform.scale(hillImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        hillImages.append(surf)

    woodsImages = []
    woodsImages.append(pygame.image.load("res/woods.png"))
    woodsImages[0].set_colorkey((255,0,255))
    w = woodsImages[0].get_width()
    h = woodsImages[0].get_height()

    for i in range (3,11):
        surf = pygame.transform.scale(woodsImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        woodsImages.append(surf)

    cliffsImages = []
    cliffsImages.append(pygame.image.load("res/cliffs.png"))
    cliffsImages[0].set_colorkey((255,0,255))
    w = cliffsImages[0].get_width()
    h = cliffsImages[0].get_height()

    for i in range (3,11):
        surf = pygame.transform.scale(cliffsImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        cliffsImages.append(surf)

    beachImages = []
    beachImages.append(pygame.image.load("res/beach.png"))
    beachImages[0].set_colorkey((255,0,255))
    w = beachImages[0].get_width()
    h = beachImages[0].get_height()

    for i in range (3,11):
        surf = pygame.transform.scale(beachImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        beachImages.append(surf)

    waterImages = []
    waterImages.append(pygame.image.load("res/water.png"))
    waterImages[0].set_colorkey((255,0,255))
    w = waterImages[0].get_width()
    h = waterImages[0].get_height()

    for i in range (3,11):
        surf = pygame.transform.scale(waterImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        waterImages.append(surf)

    
        
    
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

        self.bgHeights = None
        self.bgZones = None
        self.heightAboveWater = 1

    
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
    
    def draw(self,display:pygame.Surface,cameraX,cameraY,cameraWidth,cameraHeight):
        #Draw ocean/horizon
        pygame.draw.rect(display, (10,10,200),(0,cameraHeight/2,cameraWidth,cameraHeight),0)

        if self.bgHeights != None:
            for i in range(min(len(Room.hillImages),len(self.bgHeights))):
                ind = min(len(Room.hillImages),len(self.bgHeights))-1-i
                surf = Room.hillImages[ind]
                w = surf.get_width()
                offSet = (1037*i) % 159 #Gives kinda random look
                setX = cameraWidth/2-cameraX/(ind+2) + offSet
                startInd = -int(setX//w) - 1
                endInd = startInd + int(cameraWidth//w) + 2
                devJs = []
                for j in range(startInd,endInd):
                    heightInd = (Room.backGroupWidth*(ind+1) + j-Room.backStartInd)//Room.backGroupWidth
                    devJs.append(j)
                    try:
                        height = self.bgHeights[ind][heightInd]
                    except:
                        print("ind: "+str(ind))
                        print("j: "+str(j))
                        print("heightInd: "+str(heightInd))
                        
                        print("len1: "+str(len(self.bgHeights)))
                        if len(self.bgHeights) > ind:
                            print("len2: "+str(len(self.bgHeights[ind])))
                        print(devJs)

                    #TODO Should potentially add extra height term for camera height above ground
                    # in in-game units.
                    imageDisp = 0
                    if self.bgZones[ind][heightInd] == World.water:
                        image = Room.waterImages[ind]
                        #imageDisp = -0.4
                    elif self.bgZones[ind][heightInd] == World.beach:
                        image = Room.beachImages[ind]
                        #imageDisp = 0
                    elif self.bgZones[ind][heightInd] == World.plains:
                        image = Room.hillImages[ind]
                        imageDisp = 70
                    elif self.bgZones[ind][heightInd] == World.woods:
                        image = Room.woodsImages[ind]
                        imageDisp = 100
                    elif self.bgZones[ind][heightInd] == World.cliffs:
                        image = Room.cliffsImages[ind]
                        imageDisp = 100
                    camCenterHeight = 0
                    drawX = j*w+setX
                    drawY = cameraHeight/2-(cameraY+100*(height-self.heightAboveWater-camCenterHeight) + imageDisp)/(ind+2)
                    if self.bgZones[ind][heightInd] != World.water:
                        display.blit(image,(drawX,drawY))
                    else:
                        pygame.draw.rect(display,(10,10,200),(drawX,drawY,800/(ind+2),800/(ind+2)),0)

        startRow = int(cameraY)//self.blockWidth 
        startCol = int(cameraX)//self.blockWidth 

        for row in range(max(0,startRow),min(startRow+cameraHeight//self.blockWidth + 2,len(self.grid))):
            gridRow = self.grid[row]
            for col in range(max(0,startCol),min(startCol+cameraWidth//self.blockWidth + 2,len(self.grid[0]))):
                if gridRow[col]:
                    color = World.colors[World.beach]
                    pygame.draw.rect(display, color, (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 0)
                    #pygame.draw.rect(display, (0,0,0), (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 1)



    def generateSand(self):
        lo = 3
        hi = 7
        sandHeight = 5
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


    def generateGrass(self):
        lo = 6
        hi = 12
        grassHeight = 8
        for row in range(self.rows):
            self.grid.append([0]*self.cols)
        for x in range(self.cols):
            if random.random()<0.1:
                downchance = (grassHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    grassHeight-=1
                else:
                    grassHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = 1*(self.rows-1-y<grassHeight)

    def updateBackground(self,world:World,row,col):
        cellZones = []
        cellHeights = []


        for i in range(row):
            cellZones.append([0]*(2*i+3))
            cellHeights.append([0]*(2*i+3))
            for j in range(len(cellHeights[i])):
                if col + j - i - 1 < 0 or col + j - i - 1 >= world.width:
                    cellHeights[i][j] = 0
                    cellZones[i][j] = World.water
                else:
                    try:
                        cellHeights[i][j] = world.heightGrid[row-i-1][col+j-i-1]
                        cellZones[i][j] = world.zoneGrid[row-i-1][col+j-i-1]
                    except:
                        print("i:"+str(i))
                        print("j:"+str(j))
                        print("row:"+str(row))
                        print("col:"+str(col))
                        assert(False)
        self.bgHeights = cellHeights
        self.bgZones = cellZones
        self.heightAboveWater = world.heightGrid[row][col]

        print(len(self.bgHeights))

                    
                    
        


        


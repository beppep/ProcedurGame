import pygame
import random

from constants import Constants

class Room():


    #Init some background stuff. Images in different sizes


    pathImage = pygame.image.load("res/path.png").convert()
    pathImage.set_colorkey((255,0,255))

    backStartInd = -1 # Found out through trial and error
    backGroupWidth = 4 # images at indices -1 ,0 ,1, 2 represent landscape of cell directly north of room
    #(Indices here refers to inds computed in the draw method (j))
    #Only applies if images are approximately 400 pixels wide
    #TODO(?) make these values dependent on image width. (may need one value per image :( )

    depth = 25

    fogSurf = pygame.Surface((1000,600))  # the size of your rect
    fogSurf.set_alpha(10)                # alpha level
    fogSurf.fill((200,200,255))           # this fills the entire surface
    

    hillImages = []
    hillImages.append(pygame.image.load("res/hill.png").convert())
    hillImages[0].set_colorkey((255,0,255))
    w = hillImages[0].get_width()
    h = hillImages[0].get_height()

    for i in range (3,3+depth):
        surf = pygame.transform.scale(hillImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        hillImages.append(surf)

    woodsImages = []
    woodsImages.append(pygame.image.load("res/woods.png"))
    woodsImages[0].set_colorkey((255,0,255))
    w = woodsImages[0].get_width()
    h = woodsImages[0].get_height()

    for i in range (3,3+depth):
        surf = pygame.transform.scale(woodsImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        woodsImages.append(surf)

    cliffsImages = []
    cliffsImages.append(pygame.image.load("res/cliffs.png"))
    cliffsImages[0].set_colorkey((255,0,255))
    w = cliffsImages[0].get_width()
    h = cliffsImages[0].get_height()

    for i in range (3,3+depth):
        surf = pygame.transform.scale(cliffsImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        cliffsImages.append(surf)

    beachImages = []
    beachImages.append(pygame.image.load("res/beach.png"))
    beachImages[0].set_colorkey((255,0,255))
    w = beachImages[0].get_width()
    h = beachImages[0].get_height()

    for i in range (3,3+depth):
        surf = pygame.transform.scale(beachImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        beachImages.append(surf)

    waterImages = []
    waterImages.append(pygame.image.load("res/water.png"))
    waterImages[0].set_colorkey((255,0,255))
    w = waterImages[0].get_width()
    h = waterImages[0].get_height()

    for i in range (3,3+depth):
        surf = pygame.transform.scale(waterImages[0],(int(2*w/i),int(2*h/i))).convert()
        surf.set_colorkey((255,0,255))
        waterImages.append(surf)

    
        
    
    def __init__ (self,width,height,row,col,world):
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
        self.row = row
        self.col = col
        self.zone = world.zoneGrid[row][col]
        self.generateBlocks(self.zone,world,row,col)

        self.bgHeights = None
        self.bgZones = None
        self.heightAboveWater = 1
        self.enemies = []
        #self.generateEnemies(self.zone,world,row,col) # circular import asså aaaaaaaaaaaa
        self.projectiles = []

    
    def checkFree(self,rectangle,xdisp = 0,ydisp = 0):
        startRow = max(int(rectangle[1] + ydisp)//self.blockWidth,0)
        endRow = min(int(rectangle[1] + rectangle[3]-1 + ydisp)//self.blockWidth + 1 ,len(self.grid))
        startCol = max(int(rectangle[0] + xdisp)//self.blockWidth,0)
        endCol = min(int(rectangle[0] + rectangle[2]-1 + xdisp)//self.blockWidth + 1 ,len(self.grid[0]))
        for i in range(startRow,endRow):
            for j in range(startCol,endCol):
                if self.grid[i][j] > 0:
                    return False 
        return True
    
    def click(self,x,y):
        row = int(y//self.blockWidth)
        col = int(x//self.blockWidth)
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return
        self.grid[row][col] = not self.grid[row][col]


    def drawBackground(self,display:pygame.Surface,cameraX,cameraY,cameraWidth,cameraHeight,world):
        #Draw ocean/horizon
        horizon = 1.3
        pygame.draw.rect(display, (10,10,200),(0,horizon*cameraHeight/2,cameraWidth,cameraHeight),0)

        #TODO Change so that the world.grid attributes are used directly when drawing the backgrounds
        if self.bgHeights != None:
            for i in range(min(len(Room.hillImages),len(self.bgHeights))):
                ind = min(len(Room.hillImages),len(self.bgHeights))-1-i
                surf = Room.hillImages[ind]
                w = surf.get_width()
                offSet = (1037*i) % 159 #Gives kinda random look
                setX = cameraWidth/2-(cameraX + offSet)/(ind+2) 
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
                    if self.bgZones[ind][heightInd] == Constants.water:
                        image = Room.waterImages[ind]
                        #imageDisp = -0.4
                    elif self.bgZones[ind][heightInd] == Constants.beach:
                        image = Room.beachImages[ind]
                        #imageDisp = 0
                    elif self.bgZones[ind][heightInd] == Constants.plains:
                        image = Room.hillImages[ind]
                        imageDisp = 90
                    elif self.bgZones[ind][heightInd] == Constants.woods:
                        image = Room.woodsImages[ind]
                        imageDisp = 130
                    elif self.bgZones[ind][heightInd] == Constants.cliffs:
                        image = Room.cliffsImages[ind]
                        imageDisp = 100
                    camCenterHeight = 1.2
                    drawX = j*w+setX
                    drawY = horizon*cameraHeight/2-(cameraY+100*(height-self.heightAboveWater-camCenterHeight) + imageDisp)/(ind+2)
                    
                    if self.bgZones[ind][heightInd] == Constants.water:
                        pygame.draw.rect(display,(10,10,200),(drawX,drawY,800/(ind+2),800/(ind+2)),0)
                    #elif self.bgZones[ind][heightInd] == Constants.cliffs:
                    #    pygame.draw.rect(display,(100,100,100),(drawX,drawY,800/(ind+2),700/(ind+2)),0)
                    else:
                        display.blit(image,(drawX,drawY))

                if i % 5 == 4: #or (ind < 9 and ind > 2):
                    display.blit(Room.fogSurf,(0,0))
        
        #Drawing closest background layer
        for i in range(8):
            l = self.width/8
            x1 = i*l -cameraX
            x2 = x1 + l 
            a = world.playerCoords[0]
            b = world.playerCoords[1]
            y1 = self.height-(a*b*i +2*a*i + b + i*i) % 7 * 10 - 80 -cameraY 
            y2 = self.height-(a*b*(i+1) +2*a*(i+1) + b + (i+1)*(i + 1)) % 7 * 10 - 80 -cameraY
            color =(min(255,Constants.colors[self.zone][0]+30),min(255,Constants.colors[self.zone][1]+30),min(255,Constants.colors[self.zone][2]+30))
            pygame.draw.polygon(display,color,[(x1,y1),(x2,y2),(x2,cameraHeight),(x1,cameraHeight)],0)


    def drawBlocks(self,display:pygame.Surface,cameraX,cameraY,cameraWidth,cameraHeight,world):
        #color =(min(255,Constants.colors[self.zone][0]+30),min(255,Constants.colors[self.zone][1]+30),min(255,Constants.colors[self.zone][2]+30))
        #pygame.draw.rect(display,color,(0,self.height-100-cameraY,cameraWidth,cameraHeight),0)             

        startRow = int(cameraY)//self.blockWidth 
        startCol = int(cameraX)//self.blockWidth 

        for row in range(max(0,startRow),min(startRow+cameraHeight//self.blockWidth + 2,len(self.grid))):
            gridRow = self.grid[row]
            for col in range(max(0,startCol),min(startCol+cameraWidth//self.blockWidth + 2,len(self.grid[0]))):
                if gridRow[col] != -1:
                    color = Constants.colors[gridRow[col]]
                    pygame.draw.rect(display, color, (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 0)
                    #pygame.draw.rect(display, (0,0,0), (col*self.blockWidth-cameraX,row*self.blockWidth-cameraY, self.blockWidth, self.blockWidth), 1)


    def drawPathFg(self,display:pygame.Surface,cameraX,cameraY,cameraWidth,cameraHeight,world):
        #Drawing path fg
        if world.playerCoords[1] < world.height - 1:
            z = world.zoneGrid[world.playerCoords[1]+1][world.playerCoords[0]]
            if z != Constants.cliffs and z != Constants.water:
                xx = 3*self.width/4 - 200 - cameraX
                yy = self.height - 400 + 250 - cameraY
                display.blit(Room.pathImage,(xx,yy))

    def drawPathBg(self,display:pygame.Surface,cameraX,cameraY,cameraWidth,cameraHeight,world):
        #Drawing path bg
        if world.playerCoords[1] > 0:
            z = world.zoneGrid[world.playerCoords[1]-1][world.playerCoords[0]]
            if z != Constants.cliffs and z != Constants.water:
                xx = self.width/4 - 200 - cameraX
                yy = self.height - 400 +200 - cameraY
                display.blit(Room.pathImage,(xx,yy))




    def generateSand(self):
        lo = 2
        hi = 4
        sandHeight = 3
        for row in range(self.rows):
            self.grid.append([-1]*self.cols)
        for x in range(self.cols):
            if random.random()<0.1:
                downchance = (sandHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    sandHeight-=1
                else:
                    sandHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = Constants.beach if self.rows-1-y<sandHeight else -1

    def generateGrass(self):
        lo = 2
        hi = 6
        grassHeight = 8
        for row in range(self.rows):
            self.grid.append([-1]*self.cols)
        for x in range(self.cols):
            if random.random()<0.2:
                downchance = (grassHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    grassHeight-=1
                else:
                    grassHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = Constants.plains if self.rows-1-y<grassHeight else -1

    def generateWoods(self):
        lo = 2
        hi = 5
        grassHeight = 8
        for row in range(self.rows):
            self.grid.append([-1]*self.cols)
        for x in range(self.cols):
            if random.random()<0.2:
                downchance = (grassHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    grassHeight-=1
                else:
                    grassHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = Constants.woods if self.rows-1-y<grassHeight else -1

    def generateCliffs(self):
        lo = 3
        hi = 10
        groundHeight = 10
        for row in range(self.rows):
            self.grid.append([-1]*self.cols)
        for x in range(self.cols):
            if random.random()<0.5:
                groundHeight += random.randint(max(lo-groundHeight, -4),0) + random.randint(0,min(hi-groundHeight, 4))
            for y in range(self.rows):
                self.grid[y][x] = Constants.cliffs*(self.rows-1-y<groundHeight)

    def generateBlocks(self,type,world,row,col): 
        lo = 2
        hi = 5
        blockHeight = 3
        for i in range(self.rows):
            self.grid.append([-1]*self.cols)
        for x in range(self.cols):
            if random.random()<0.1:
                downchance = (blockHeight-lo)/(hi-lo)
                if random.random() < downchance:
                    blockHeight-=1
                else:
                    blockHeight+=1
            for y in range(self.rows):
                self.grid[y][x] = type if self.rows-1-y<blockHeight else -1

        if (world.zoneGrid[row][col] != type):
            print("woops")
            print("type: "+str(type))
            print("self.zone: "+str(self.zone))
            print("world.zoneGrid[row][col]:" + str(world.zoneGrid[row][col]))
            print("row: "+str(row)+" col: "+str(col))
            print("self.row: "+str(self.row)+" col: "+str(self.col))

        if col < world.width - 1 and world.zoneGrid[row][col+1] == Constants.cliffs and type != Constants.cliffs:
            for i in range(self.rows):
                if self.grid[i][self.cols-1] != -1:
                    break
                self.grid[i][self.cols-1] = Constants.cliffs

        if  col > 0 and world.zoneGrid[row][col-1] == Constants.cliffs and type != Constants.cliffs:
            for i in range(self.rows):
                if self.grid[i][0] != -1:
                    break
                self.grid[i][0] = Constants.cliffs

        minLen = 2
        maxLen = 20
        if col > 0  and world.zoneGrid[row][col-1] == Constants.water and type != Constants.cliffs:
            for i in range(self.rows-hi,self.rows):
                for j in range(self.cols):
                    if self.grid[i][j] != -1 and j > minLen+(maxLen-minLen)/hi*(self.rows-1-i):
                        break
                    for ii in range(i,self.rows):
                        if self.grid[ii][j] == -1 or ii == i:
                            self.grid[ii][j] = Constants.water if i > self.rows-hi -1 else -1

        if col < world.width - 1 and world.zoneGrid[row][col+1] == Constants.water and type != Constants.cliffs:
            for i in range(self.rows-hi,self.rows):
                for j in range(self.cols):
                    if self.grid[i][self.cols-1-j] != -1 and j > minLen+(maxLen-minLen)/hi*(self.rows-1-i):
                        break
                    for ii in range(i,self.rows):
                        if self.grid[ii][self.cols-1-j] == -1 or ii == i:
                            self.grid[ii][self.cols-1-j] = Constants.water if i > self.rows-hi -1 else -1

    def generateEnemies(self,type,world,row,col): 
        for i in range(random.randint(0,20)):
            self.enemies.append(Enemy(random.randint(100,self.width-100),100,random.choice(Enemy.presets)))

    def updateBackground(self,world,row,col):
        cellZones = []
        cellHeights = []
        
        self.heightAboveWater = world.heightGrid[row][col]
        self.zone = world.zoneGrid[row][col]

        for i in range(row):
            cellZones.append([0]*(2*i+3))
            cellHeights.append([0]*(2*i+3))
            for j in range(len(cellHeights[i])):
                if col + j - i - 1 < 0 or col + j - i - 1 >= world.width:
                    cellHeights[i][j] = 0
                    cellZones[i][j] = Constants.water
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
        

        print(len(self.bgHeights))

                    
                    
        


        


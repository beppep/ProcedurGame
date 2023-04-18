import pygame 
import random

class World:
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
    
    minNbrs = { water: [2,0,0,0,0] , 
              beach : [1,2,0,0,0], 
              cliffs : [0,0,1,0,0],
              plains : [0,0,0,1,0],
              woods : [0,0,0,0,2]}
    
    maxNbrs = { water: [4,2,3,0,0] , 
              beach : [2,3,2,1,3], 
              cliffs : [4,4,4,4,4],
              plains : [0,4,2,4,3],
              woods : [0,1,1,3,4]}
    
    probWeights = [20,10,5,40,25]
    
    

    def __init__(self,width,height, seed = None):
        self.rand = random.Random()
        if seed != None:
            self.rand.seed(seed)
        self.grid = []
        self.boolGrid = []
        self.height = height
        self.width = width
        self.surf = pygame.Surface((width*5,height*5))

        #Set initial ring of water
        for i in range(self.height):
            self.grid.append([0]*self.width)
            self.boolGrid.append([True,False,False,False,False]*self.width)

        #Enable all possibilites for the remaining cells
        for i in range(1,self.height-1):
            for j in range(1,self.width-1):
                self.grid[i][j] = -1
                self.boolGrid[i][j] = [True,True,True,True,True]

        
        done = False
        while(not done):
            done = True
            for i in range(1,self.height-1):
                for j in range(1,self.width-1):
                    val = self.rand.randint(0,99)
                    for k in range(len(World.probWeights)):
                        if val < sum(World.probWeights[0:k+1]):
                            self.grid[i][j] = k
                            break
                        #self.grid[i][j] = 4
        self.drawMap(self.surf)

    def checkCompatibility(grid,row,col):
        type = grid[row][col]
        if type == -1:
            return True
        vals = [0,0,0,0,0]
        free = 0
        checkPos = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]
        for pos in checkPos:
            oType = grid[pos[0],pos[1]]
            if oType != -1:
                vals[oType] += 1
            else:
                free += 1
        

    
    def drawMap(self,display):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(display,World.colors[self.grid[i][j]],(j*5,i*5,5,5),0)
        
        
        
        
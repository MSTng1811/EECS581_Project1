import pygame
import socket
import numpy as np
import math


class BoardSetup:

    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.rotated = False
        self.submarine = pygame.image.load("pictures/submarine.png")
        self.cruiser = pygame.image.load("pictures/cruiser.png")
        self.carrier = pygame.image.load("pictures/carrier.png")
        self.battleship = pygame.image.load("pictures/battleship.png")
        self.destroyer = pygame.image.load("pictures/destroyer.png")
        self.destCount = 1
        self.crusCount = 1
        self.carrCount = 1
        self.batCount = 1
        self.subCount = 1
        self.allShipPlaced = False
        self.start = pygame.image.load("pictures/start.png")
        self.start = pygame.transform.scale(self.start, (480, 360))
        self.offset = 0

    def generateGrid(self):		#Function to generate 10x10 grid board
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for x, i in enumerate(self.board):	#x: Index, i: Value
            for y, j in enumerate(i):		#y: Index, j: Value
                if j == 0:		#Implying the grid is empty, thus creating a small box with white border and a circle in between
                    pygame.draw.rect(self.screen, (255, 255, 255), (600+(65*y), 63+self.offset, 63, 63), 1)
                    pygame.draw.circle(self.screen, (255, 255, 255), ((600+(65*y))+30, (63+self.offset)+30), 6)
                else:			#Implying the grid is not empty and a ship is placed there, thus creating a green filled box with circle in between
                    pygame.draw.rect(self.screen, (25, 209, 83), (600+(65*y), 63+self.offset, 63, 63), 1)
                    pygame.draw.circle(self.screen, (25, 209, 83), ((600+(65*y))+30, (63+self.offset)+30), 6)
            self.offset+=65		#Increasing the cell offset value to change the coordinates and thus create equal grids in different rows
        self.offset = 0		#Resetting offset value

        #After generating the grid, we will label the grids with the index values by iterating through each grid position
        for x, i in enumerate(self.board):
            font = pygame.font.SysFont("arial", 48)
            num = font.render(str(x+1), True, (255, 255, 255))
            self.screen.blit(num, (610+(x*65), 8))		#Placing the numbers on each grid horizontally
            letter = font.render(letters[x], True, (255,255,255))
            self.screen.blit(letter, (570, 60+(x*65)))		#Placing the alphabets on each grid vertically

    def shipSet(self):		#Function to place ship icons on the game screen
        font = pygame.font.SysFont("arial", 72)
        #Setting font for count value of ships
        destCount = font.render(str(self.destCount), True, (255, 255, 255))
        crusCount = font.render(str(self.crusCount), True, (255, 255, 255))
        subCount = font.render(str(self.subCount), True, (255, 255, 255))
        batCount = font.render(str(self.batCount), True, (255, 255, 255))
        carrCount = font.render(str(self.carrCount), True, (255, 255, 255))
        #Positioning the images and generated texts on the game screen
        self.screen.blit(self.submarine, (30, 425))
        self.screen.blit(self.cruiser, (30, 300))
        self.screen.blit(self.carrier, (30, 600))
        self.screen.blit(self.battleship, (30, 500))
        self.screen.blit(self.destroyer, (30, 200))
        self.screen.blit(subCount, (350, 415))
        self.screen.blit(crusCount, (325, 325))
        self.screen.blit(carrCount, (500, 615))
        self.screen.blit(batCount, (400, 515))
        self.screen.blit(destCount, (225, 215))

    def click(self, image, event):		#Function to load the image to mouse to be able to drag it around screen
        x, y = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        if image != "":			#If image is selected, then perform relevant actions
            if key[pygame.K_LEFT] and not self.rotated:
                image = pygame.transform.rotate(image, 90)
                self.rotated = True
            elif self.rotated == True:
                image = pygame.transform.rotate(image, 90)
                if key[pygame.K_LEFT]:
                    image = pygame.transform.rotate(image, -90)
                    self.rotated = False
            width, height = image.get_size()
            self.run_first()
            self.screen.blit(image, (x-width/2, y-height/2))
            pygame.display.update()

    def generatePos(self):	#Function to generate coordinate values for the grid board
        x, y = 600, 30		#Initial coordinates
        grid = np.zeros(shape=(10, 10), dtype=tuple)		#Creating a grid tuple
        cellMap = 0
        #Storing the value of each grid to be able to place the ships
        for m, i in enumerate(self.board):
            for n, j in enumerate(i):
                x += (n*65)
                y += (cellMap*65)
                pos = (x,y)
                grid[m][n] = pos
            cellMap += 1
        return grid

    def calcPos(self, ship):	#Function to calculate the position on grid and performing necessary functions
        x, y = pygame.mouse.get_pos()		#Getting mouse coordinates
        x = math.floor((x-600)/65)
        y = math.floor((y-30)/65)
        if x>= 0 and y>= 0:
	    #Positioning the ships on the board. Here we are marking the grid coordinates as 1 which will be passed to the generateGrid() function
	    #And that will color the occupied grids as green. If the ship is rotated, then vertical values will be changed, ad vice versa for horizontal
            if ship == "destroyer":	#GRID SIZE- 3
                if self.rotated:
                    self.board[y-1][x] = 1
                    self.board[y][x] = 1
                    self.board[y+1][x] = 1
                else:
                    self.board[y][x-1:x+2] = 1
                self.destCount = 0
            elif ship == "cruiser":	#GRID SIZE- 4
                if self.rotated:
                    self.board[y-2][x] = 1
                    self.board[y-1][x] = 1
                    self.board[y][x] = 1
                    self.board[y+1][x] = 1
                else:
                    self.board[y][x - 2:x + 2] = 1
                self.crusCount = 0
            elif ship == "carrier":	#GRID SIZE- 7
                if self.rotated:
                    self.board[y - 3][x] = 1
                    self.board[y - 2][x] = 1
                    self.board[y - 1][x] = 1
                    self.board[y][x] = 1
                    self.board[y + 1][x] = 1
                    self.board[y + 2][x] = 1
                    self.board[y + 3][x] = 1
                else:
                    self.board[y][x - 3:x + 4] = 1
                self.carrCount = 0
            elif ship == "submarine" or ship == "battleship":	#GRID SIZE- 5
                if self.rotated:
                    self.board[y-2][x] = 1
                    self.board[y - 1][x] = 1
                    self.board[y][x] = 1
                    self.board[y + 1][x] = 1
                    self.board[y + 2][x] = 1
                else:
                    self.board[y][x - 2:x + 3] = 1
                if ship == "submarine":
                    self.subCount = 0
                else:
                    self.batCount = 0
            return True

    def run_first(self):	#Function combining the whole class and running it together
        #Setting the screen background
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 72)
        heading = font.render("Place your ships", True, (255, 255, 255))
        self.screen.blit(heading, (30, 30))
	#Calling other defined functions
        self.generateGrid()
        self.shipSet()
        
    
	#The condition below makes sures that all the ships are positioned before the game starts
        if self.carrCount==0 and self.batCount==0 and self.subCount==0 and self.crusCount==0 and self.destCount==0:
            self.screen.blit(self.start, (-90, 70))
            self.allShipPlaced = True

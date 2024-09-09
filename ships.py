#Importing necessary files
import pygame		#Game module
import socket		#Establish connection through server
import numpy as np
import math

class Ship:
	def __init__(self, screen, board, cell=0):
		self.screen = screen
		self.cell = cell
		self.board = board
		self.rotated = False
		folder = "pictures/"
		#Image icons
		self.submarine = pygame.image.load(folder+"submarine.jpg")
		self.battleship = pygame.image.load(folder+"battleship.jpg")
		self.cruiser = pygame.image.load(folder+"cruiser.jpg")
		self.carrier = pygame.image.load(folder+"carrier.jpg")
		self.destroyer = pygame.image.load(folder+"destroyer.jpg")
		#Image icon counter
		self.submarine_count = 1
		self.battleship_count = 1
		self.carrier_count = 1
		self.cruiser_count = 1
		self.destroyer_count = 1
		#Start icon and its position
		self.start = pygame.image.load(folder+"start.jpg")
		self.start = pygame.transform.scale(self.start, (480, 360))

	def background(self):		#Background function
		self.screen.fill((146, 249, 255))		#Screen color= light blue
		font = pygame.font.SysFont('arial', 60)		#Font for the text
		head = font.render("BATTLE SHIP", True, (0, 0, 0))	#Title
		self.screen.blit(head, (30, 30))	#Title display position

	def drawgrid(self):		#Generating grid
		for n, i in enumerate(self.board):
			for m, j in enumerate(i):
				#If the value of j is 0 which means the grid is empty, we will create grey rectangles for grid
				if j==0:
					pygame.draw.rect(self.screen,(145, 145, 145), (600+(65*m), 63+self.cell, 63, 63), 1)		#Defines a rectangle in format ((color rgb value), (x coordinate, y coordinate, width, height), thickness in pixels)
                		#If the grid is occupied by a ship icon, the rectangle will turn green
				else:
                    			pygame.draw.rect(self.screen,(25, 209, 83), (600+(65*m), 63+self.cell, 63, 63), 1)
			self.cell += 65			#Moving next row down by 65 pixels to ensure vertically spaced rows
		self.cell = 0		#Resetting cell offset

	def drawnum(self):		#Function to draw numbers and alphabets on the grid board
		letters = ['A','B','C','D','E','F','G','H','I','J']
		font = pygame.font.SysFont('arial', 40)
		for n, i in enumerate(self.board):
			count = font.render(str(n+1), True, (0, 0, 0))	#Defining the number texts
			self.screen.blit(count, (610+ (n*65), 8))	#Adjusting the number position with inputs x and y coordinate using blit()
			letter = font.render(letters[n], True, (0, 0, 0))	#Defining alphabet texts
			self.screen.blit(letter, (568, 60+(n*65)))	#Adjusting the position of letters using blit()


	def ship(self):			#Function to draw ships and boats
		font = pygame.font.SysFont('arial', 70)
		#Setting the ship counter text for all the ships
		submarine_count = font.render(str(self.submarine_count), True, (0, 0, 0))
		cruiser_count = font.render(str(self.cruiser_count), True, (0, 0, 0))
		destroyer_count = font.render(str(self.destroyer_count), True, (0, 0, 0))
		battleship_count = font.render(str(self.battleship_count), True, (0, 0, 0))
		carrier_count = font.render(str(self.carrier_count), True, (0, 0, 0))
		#Adjusting the position of all the ships initialized in __init__ function
		self.screen.blit(self.submarine, (30, 425))
		self.screen.blit(self.destroyer, (30, 200))
		self.screen.blit(self.cruiser, (30, 400))
		self.screen.blit(self.battleship, (30, 500))
		self.screen.blit(self.carrier, (30, 600))
		#Adjusting the position of counter texts next to the ships images
		self.screen.blit(submarine_count, (350, 415))
		self.screen.blit(destroyer_count, (225, 215))
		self.screen.blit(cruiser_count, (325, 325))
		self.screen.blit(battleship_count, (400, 515))
		self.screen.blit(carrier_count, (500, 615))

	def drag(self, image, act):		#Function to drag the image to the grid
		x, y = pygame.mouse.get_pos()	#Get input coordinates from mouse cursor
		key = pygame.key.get_pressed()	#Find out which mouse key has been pressed
		if image!='':		#Make sure the image is selected
			if key[pygame.K_LEFT] and self.rotated==False:	#If left key is pressed and the image is not rotated, we rotate the image by 90 degrees
				image = pygame.transform.rotate(image, 90)
				self.rotated = True
			elif self.rotated==True:
				image = pygame.transform.rotate(image, 90)
				if key[pygame.K_LEFT]:
					image = pygame.transform.rotate(image, -90)
					self.rotated = False
			w, h = image.get_size()		#Finding width and height of the image
			self.generate()
			self.screen.blit(image, (x-(w/2), y-(h/2)))
			pygame.display.update()		#Update the board

	def brdpos(self):		#Generating a tuple to keep a track of grid count
		x = 600
		y = 30
		brd_tuple = np.zeros(shape=(10,10), dtype=tuple)
		cells = 0
		#Going through each grid and storing it in the board tuple
		for n, i in enumerate(brd):
			for m, j in enumerate(i):
				newx= x+(m*65)
				newy= y+ (cells*65)
				pos = (x,y)
				brd_tuple[n][m] = pos
			cells+=1
		return brd_tuple

	def calcpos(self, ship):		#Determining the position of the ship on the board
		x,y= pygame.mouse.get_pos()	#Get coordinates through mouse input
		#Adjusting position offsets
		x = math.floor((x-600)/65)
		y = math.floor((y-30)/65)
		if x>=0 and y>=0:		#Ensuring the mouse pointer is within the grid
			if ship=='destroyer':	#Size= 2 grids
				#In first condition, the destroyer ship is vertically placed, thus we will mark the grid as 1, which means grid is occupied. Refer to drawgrid() function to see the changes
				if self.rotated:
					self.board[y-1][x]=1
					self.board[y][x]=1
				else:		#Mark the horizontal grids as 1
					self.board[y][x-1:x+1]=1
				self.destroyer_count = 0	#Set counter to 0 which means no more ships available
			#Repeat for other ships
			elif ship=='cruiser':	#Size=4 grids
				if self.rotated:
					self.board[y-2][x]=1
					self.board[y-1][x]=1
					self.board[y][x]=1
					self.board[y+1][x]=1
				else:
					self.board[y][x-2:x+2]=1
				self.cruiser_count = 0
			elif ship=='carrier':	#Size=5 grids
				if self.rotated:
					self.board[y-2][x]=1
					self.board[y-1][x]=1
					self.board[y][x]=1
					self.board[y+1][x]=1
					self.board[y+2][x]=1
				else:
					self.board[y][x-2:x+3]=1
				self.carrier_count = 0
			elif ship=='submarine' or ship=='battleship':	#Size=3 grids
				if self.rotated:
					self.board[y-1][x]=1
					self.board[y][x]=1
					self.board[y+1][x]=1
				else:
					self.board[y][x-1:x+2]=1
				if ship=='submarine':
					self.submarine_count=0
				else:
					self.battleship_count=0
			return True

	def generate(self):		#Generate the board
		self.background()
		self.drawgrid()
		self.drawnum()
		self.ship()
		if self.submarine_count==0 and self.destroyer_count==0 and self.carrier_count==0 and self.cruiser_count==0 and self.battleship_count==0:
			self.screen.blit(self.start, (-90, 70))

#TEST FUNCTION

pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode([1280, 720])
brd = np.zeros(shape=(10,10), dtype=int)
game = Ship(screen=screen, board=brd)
game.generate()
pygame.display.update()
brd_tup = game.brdpos()
image=''
ship =''
clk=pygame.time.Clock()

while True:
	clk.tick(120)
	events=pygame.event.get()
	for event in events:
		if event.type==pygame.QUIT:
			break
		if event.type==pygame.MOUSEBUTTONDOWN:
			x,y=pygame.mouse.get_pos()
			folder = 'pictures/'
			if x>=36 and x<=334 and y>446 and y<=483:
				if game.submarine_count!=0:
					image=pygame.image.load(folder+'submarine.jpg')
					ship='submarine'
			elif x>28 and x<311 and y>=343 and y<=389:
				if game.cruiser_count!=0:
					image=pygame.image.load(folder+'cruiser.jpg')
					ship='cruiser'
			elif x>=33 and x<494 and y>=658 and y<=696:
				if game.carrier_count!=0:
					image = pygame.image.load(folder+'carrier.jpg')
					ship='carrier'
			elif x>=28 and x<=216 and y>=253 and y<=286:
				if game.destroyer_count!=0:
					image = pygame.image.load(folder+'destroyer.jpg')
					ship='destroyer'
			elif x>=36 and x<=382 and y>=554 and y<583:
				if game.battleship_count!=0:
					image = pygame.image.load(folder+'battleship.jpg')
					ship='battleship'

		if image!='':
			game.drag(image, event)
		if ship!='' and event.type==pygame.MOUSEBUTTONDOWN:
			chimg = game.calcpos(ship=ship)
			print(chimg)
			if chimg:
				image=''
				ship=''
				game.generate()
				pygame.display.update()

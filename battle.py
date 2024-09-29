import pygame
import socket
import numpy as np
import math
import random
import time
import sys

class Battle:

    def __init__(self, screen, board, isCl, isHost):
        self.screen = screen
        self.board = board
        self.enemyBrd = np.zeros(shape=(10, 10), dtype=int)
        self.isCl = isCl
        self.isHost = isHost
        self.myTurn = isCl
        self.offset = 0
        self.first = True
        self.initial = True
        self.server = None
        self.client = None
        self.last_hit = None #track last hit position (x, y)
        self.possible_targets = [] #possible orthogonal positions to fire upon
        self.direction = None #store direction of search

    def randomBoard(self):	#Function to generate a random board. Will be used when performing the attacking attempts
        for x, i in enumerate(self.board):
            for y, j in enumerate(i):
                self.board[x][y] = random.randint(0, 1)

    def heading(self):		#Function establishing the title and texts in the game board
        font = pygame.font.SysFont("arial", 48)
        self.screen.fill((0,0,0))
        myBoard = font.render("Friend Board", True, (255, 255, 255))
        self.screen.blit(myBoard, (200, 10))
        enemyBoard = font.render("Enemy Board", True, (255, 255, 255))
        self.screen.blit(enemyBoard, (820, 10))

    def createSocket(self, ip):		#Function establishing a network stream for both the players to play the game at once
        if self.isHost:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Generating network stream with IPv4 and TCP protocol
            self.server.bind(('', 8088))		#Binding the network stream to default port
            self.server.listen()
            self.connect, self.add=self.server.accept()
        else:		#Client
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Establushing a network stream to receive the signal from host
            time.sleep(3)
            self.client.connect((ip, 8088))		#Connecting the client using the inputted IP address

    def genMyBoard(self):		#Function to generate your board on battlescreen
        location = 20
        for x, i in enumerate(self.board):
            for y, j in enumerate(i):
                if j==0:	#Grid has not been attacked yet
                    pygame.draw.rect(self.screen, (255, 255, 255), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (255, 255, 255), ((location+(60*y))+30, (88+self.offset)+30), 6)
                elif j == 1:	#Grid has been attacked but target is missed
                    pygame.draw.rect(self.screen, (25, 209, 83), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (25, 209, 83), ((location+(60*y))+30, (88+self.offset)+30), 6)
                elif j == 2:	#Grid has been attacked and target is hit
                    pygame.draw.rect(self.screen, (255, 0, 0), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (242, 19, 19), ((location+(60*y))+30, (88+self.offset) + 30), 6)
            self.offset += 60	#Explained in board setup function
        self.offset = 0

    def genEnemyBoard(self):		#Function to generate enemy board in a similar manner as above
        location = 650
        for x, i in enumerate(self.board):
            for y, j in enumerate(i):
                if j==0:        #Grid has not been attacked yet
                    pygame.draw.rect(self.screen, (255, 255, 255), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (255, 255, 255), ((location+(60*y))+30, (88+self.offset)+30), 6)
                elif j == 1:    #Grid has been attacked but target is missed
                    pygame.draw.rect(self.screen, (25, 209, 83), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (25, 209, 83), ((location+(60*y))+30, (88+self.offset)+30), 6)
                elif j == 2:    #Grid has been attacked and target is hit
                    pygame.draw.rect(self.screen, (255, 0, 0), (location+(60*y), 90+self.offset, 58, 58), 1)
                    pygame.draw.circle(self.screen, (242, 19, 19), ((location+(60*y))+30, (88+self.offset) + 30), 6)
            self.offset += 60   #Explained in board setup function
        self.offset = 0

    def attempt(self):			#Function to setup text for attempts notification
        font = pygame.font.SysFont("arial", 36)
        if self.myTurn:
            turn = font.render("Your Turn!", True, (255, 255, 255))
            self.screen.blit(turn, (560, 20))
        else:
            turn = font.render("Oppenent's Turn!", True, (255, 255, 255))
            self.screen.blit(turn, (510, 20))

    def switchBoard(self, x, y):	#Function to switch between the boards during the battle
        self.enemyBrd[y][x] = 2
        self.first = True
        self.myTurn = False
        if self.client:
            self.client.send(bytes(str(x) + "_" + str(y), 'utf-8'))
        else:
            print("sent server")
            self.connect.send(bytes(str(x) + "_" + str(y), 'utf-8'))
        print("overall sent")

    def message(self, desc):		#Function to generate text for missed hit
        font = pygame.font.SysFont("arial", 32)
        desc = font.render(str(desc) + "!", True, (255, 255, 255))
        self.screen.blit(desc, (30, 20))
        pygame.display.update()

    def medium_ai_fire(self):
        if self.last_hit is not None:
            #if we have a hit, try orthogonally adjacent spaces
            if not self.possible_targets:
                self.possible_targets = self.get_adjacent_positions(self.last_hit)
            #fire at one of adjacent targets
            target = self.possible_targets.pop(0)
            return target
        #if no hits, fire randomly
        return self.random_fire()
        
    def random_fire(self):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            #check if spot if not alr hit
            if self.enemyBrd[y][x] == 0:
                return (x, y)
    
    def get_adjacent_positions(self, pos):
        x, y = pos
        adjacent_positions = []
        #check for valid adjacent positions
        if x > 0 and self.enemyBrd[y][x-1] == 0: #left
            adjacent_positions.append((x-1, y))
        if x < 9 and self.enemyBrd[y][x+1] == 0: #rigth
            adjacent_positions.append((x+1, y))
        if y > 0 and self.enemyBrd[y-1][x] == 0: #up
            adjacent_positions.append((x, y-1))
        if y < 9 and self.enemyBrd[y+1][x] == 0: #down
            adjacent_positions.append((x, y+1))
        return adjacent_positions
        
    def ai_turn(self):
        target = self.medium_ai_fire()
        x, y = target
        print(f"AI firing at {x}, {y}")
        #check if the ai hits a ship
        if self.enemyBrd[y][x] == 1: #ai hits a ship
            print("AI hits a ship!")
            self.enemyBrd[y][x] = 2
            self.last_hit = (x, y)
        else:
            print("AI misses")
            self.enemyBrd[y][x] = 1 #mark it as a miss

    def run(self, ip):		#Function combining all the defined functions and running the battle module
        if self.initial:
            self.createSocket(ip=ip)
            self.initial = False
        if self.first:		#Game has begun
            self.heading()
            self.genMyBoard()
            self.genEnemyBoard()
            self.attempt()
            self.pygame.display.update()
            self.first = not self.first
            if not self.myTurn:		#Opponent's turn
                #call AI turn func
                self.ai_turn()
                #switch back to player's turn
                self.myTurn = True
                self.first = True
            else:
                if self.server:		#If the opponent is host
                    arr = self.connect.recv(1024).decode().split("_")		#Receiving data from socket
                    if arr[0] == "Target Hit" or arr[0] == "Missed":
                        self.message(arr[0])		#Generating message 
                        self.first = True
                        pass
                    else:
                        print(arr)
                        x = int(arr[0])
                        y = int(arr[1])
                        print(x, y)
                        if x<0 and y<0:
                            pass
                        else:
                            if self.board[y][x] == 1:		#Target hit, sending message to client
                                self.connect.send(bytes("Target Hit", 'utf-8'))
                            else:
                                self.connect.send(bytes("Missed", 'utf-8'))	#Target missed, sending message to client
                            self.board[y][x] = 2
                            self.myTurn = True
                            self.first = True
                else:			#Opponent is client
                    arr = self.client.recv(1024).decode().split("_")
                    print("received " + str(arr[0]))
                    if arr[0] == "Target Hit" or arr[0] == "Missed":
                        self.message(arr[0])
                        self.first = True
                        pass
                    else:
                        print(arr[0] + "yo")
                        x = int(arr[0])
                        y = int(arr[1])
                        print(x, y)
                        if x<0 and y<0:
                            pass
                        else:
                            if self.board[y][x] == 1:
                                self.client.send(bytes("Target Hit", 'utf-8'))
                            else:
                                self.client.send(bytes("Missed", 'utf-8'))
                            self.board[y][x] = 2
                            self.myTurn = True
                            self.first = True

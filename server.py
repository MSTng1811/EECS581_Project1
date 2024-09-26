import base64
import os
import time
import numpy as np
import threading
import socket
import pygame

class Server:

    def __init__(self, screen, server, connect=None, add=None):
        self.screen = screen
        self.server = server
        self.connect = connect
        self.add = add
        self.start = False
        self.data = None

    def createServer(self):			#Function to establish a server in order for clients to join and connect with the game
        PORT = 8080	#Default port for web servers
	#Here we are creating a socket stream to establish a network, with AF_INET meaning IPv4 protocol, and SOCK_STREAM establishing TCP protocol
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server.bind(('localhost', PORT))	#Binding the port with the established network stream
        self.server.listen()		#listen() will help us to access this port via the communication protocol we set up
        print(self.server.getsockname())		#Server is running message
        print("Server is running...")		#Server is running message
    def getInvite(self):		#Function to generate a team invite code (IP address) to connect to the multiplayer game
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#Here we are establishing a UDP protocol for data sending
        s.connect(("8.8.8.8", 80))		#Default IP
        font = pygame.font.SysFont("arial", 72)			#CHANGE FONT HERE IF YOU WANT TO
        smallFont = pygame.font.SysFont("arial", 60)		#CHANGE FONT HERE
        IP = s.getsockname()[0]		#Socket function to get the IP address for the established connection
        enc = ""
        for i in IP:
            if i == ".":
                enc+= "#"		#Since IP address is in the form of 0.0.0.0, we are replacing . with # symbol here
            else:
                enc+= chr(98+int(i))	#In this line, we are replacing the numbers with their ASCII values
        code = smallFont.render(str(enc), True, (255, 255, 255))	#Color of generated code- White (255, 255, 255) CHANGE COLOR HERE IF YOU WANT TO
        heading = font.render("Battle Code", True, (255, 255, 255))	#Color of heading- White (255, 255, 255) CHANGE COLOR HERE IF YOU WANT TO
        self.screen.blit(heading, (900, 30))
        self.screen.blit(code, (900, 120))

    def username(self, name):		#Function to print username
        font = pygame.font.SysFont("arial", 36)		#CHANGE FONT STYLE AND SIZE HERE
        heading = font.render(name, True, (255, 255, 255))
        self.screen.blit(heading, (100, 325))

    def genVers(self):		#Generate Versus text
        font = pygame.font.SysFont("arial", 72)
        heading = font.render("VERSUS", True, (255, 255, 255))
        self.screen.blit(heading, (420, 305))

    def enemyUsername(self, data):		#Displaying enemy username
        font = pygame.font.SysFont("arial", 36)
        if not data:
            head = font.render("Pending....", True, (255, 255, 255))
        else:
            head = font.render(str(data), True, (255, 255, 255))
        self.screen.blit(head, (950, 325))

    def heading(self):		#Generating the heading of the game
        font = pygame.font.SysFont("arial", 72)
        heading = font.render("Battle-Ship", True, (255, 255, 255))
        self.screen.blit(heading, (30, 30))

    def beginBattle(self):
        button = pygame.image.load("pictures/begin.png")
        self.screen.blit(button, (210, 450))

    def run(self, username, first, second, changeLoc, sendShip):
        if first==True:
            self.screen.fill((255, 255, 255))
            self.getInvite()
            self.username(name=username)
            self.createServer()
            self.heading()
            self.beginBattle()
            self.genVers()
            self.enemyUsername(None)
            pygame.display.update()
        elif not first and second:
            self.connect, self.add = self.server.accept()
            data = self.connect.recv(1024)
            if data:
                self.screen.fill((255, 255, 255))
                self.getInvite()
                self.username(name=username)
                self.heading()
                self.beginBattle()
                self.genVers()
                self.enemyUsername(data=data.decode("utf-8"))
                pygame.display.update()
                self.start = True
                self.data = data
                return False
        if sendShip:
            print("sent")
            self.connect.send(bytes("Place Ships", "utf-8"))
        return True

import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen

    def heading(self):
        font = pygame.font.SysFont("arial", 72)
        head = font.render("BATTLE SHIP", True, (255, 255, 255))
        self.screen.blit(head, (30, 30))

    def joinButton(self):
        join = pygame.image.load("pictures/join.png")
        join = pygame.transform.scale(join, (480, 360))
        self.screen.blit(join, (900, 0))

    def createButton(self):
        create = pygame.image.load("pictures/create.png")
        create = pygame.transform.scale(create, (480, 360))
        self.screen.blit(create, (900, 550))

    def singleGameButton(self):  
        single_game = pygame.image.load("pictures/single.png")  
        single_game = pygame.transform.scale(single_game, (480, 360))
        self.screen.blit(single_game, (900, 230))  

    def run(self):
        self.screen.fill((0, 0, 0))
        self.heading()
        self.joinButton()
        self.singleGameButton()  
        self.createButton()
        pygame.display.update()

    def difficultyMenu(self):  
        self.screen.fill((0, 0, 0))
        self.heading()
        self.easyButton()
        self.mediumButton()
        self.hardButton()
        pygame.display.update()

    def easyButton(self):
        easy = pygame.image.load("pictures/easy.png")
        easy = pygame.transform.scale(easy, (480, 360))
        self.screen.blit(easy, (900, 0))

    def mediumButton(self):
        medium = pygame.image.load("pictures/medium.png")
        medium = pygame.transform.scale(medium, (480, 360))
        self.screen.blit(medium, (900, 230))

    def hardButton(self):
        hard = pygame.image.load("pictures/hard.png")
        hard = pygame.transform.scale(hard, (480, 360))
        self.screen.blit(hard, (900, 550))

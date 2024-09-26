import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen

    def heading(self):
        font = pygame.font.SysFont("arial", 72)
        head = font.render("BATTLE SHIP", True, (255, 255, 255))
        self.screen.blit(head, (30, 30))

    def vsPlayer(self):  
        single_game = pygame.image.load("pictures/single.png")  
        single_game = pygame.transform.scale(single_game, (480, 360))
        self.screen.blit(single_game, (450, 250))
        
    def vsAIButton(self):
        vs_ai = pygame.image.load("pictures/single.png")
        vs_ai = pygame.transform.scale(vs_ai, (480, 360))
        self.screen.blit(vs_ai, (450, 500))

    def run(self):
        self.screen.fill((0, 0, 0))
        self.heading()
        self.vsPlayer()
        self.vsAIButton() 
        pygame.display.update()

    def difficultyMenu(self):  
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 72)
        temp = font.render("Please select AI difficulty", True, (255, 255, 255))
        self.screen.blit(temp, (30, 90))
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


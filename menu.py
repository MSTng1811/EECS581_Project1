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

    def run(self):
        self.screen.fill((0,0,0))
        self.heading()
        self.joinButton()
        self.createButton()
        pygame.display.update()

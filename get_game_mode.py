from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text
# rgb colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

def set_mode(screen):
    # adds text 
    add_text.add_text(screen, 'Choose Number of Players')
    # start at false
    optionsChosen = False
    # return value for singleplayer or multiplayer
    gamemode = True
    # place the boxes for options
    place_options(screen)
    # while nothing has been chosen
    while not optionsChosen:
        # get the position
         pos = pygame.mouse.get_pos()
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get the box that was selected and assign ships accordingly
                    index = get_index(screen, pos) 
                    if index != -1:
                        optionsChosen = True # set optionsChosen to true so loop will end
                        screen.fill(BLACK, (0, 0, 490, 400))
                        print(index)
                        if index == 1:
                            # SinglePlayer
                            gamemode = True
                        elif index == 2:
                            # Multiplayer
                            gamemode = False
         pygame.display.update()
    # returns the gamemode
    return (gamemode)

# creates rectangles for user to click and choose num of ships
def place_options(screen):
    # used offset to move squares to center
    offset = 45
    # create rects for each choice
    rect1 = pygame.Rect(100+offset,200,50,50)
    rect2 = pygame.Rect(240+offset,200,50,50)
    # draw each rect
    pygame.draw.rect(screen, WHITE, rect1, 1)
    pygame.draw.rect(screen, WHITE, rect2, 1)
    # add text to boxes
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('1', True, RED)
    textRect = text.get_rect()
    textRect.center = (125+offset, 225)
    screen.blit(text, textRect)
    text = font.render('2', True, RED)
    textRect = text.get_rect()
    textRect.center = (265+offset, 225)
    screen.blit(text, textRect)

# gets the index of the user click so that we know what box they selected
def get_index(screen, pos):
    offset = 45
    rect1 = pygame.Rect(100+offset,200,50,50)
    rect2 = pygame.Rect(240+offset,200,50,50)
    # collide point checks if pos is within the rect object
    # based off of https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame
    if rect1.collidepoint(pos):
        return 1
    elif rect2.collidepoint(pos):
        return 2
    else:
        return -1

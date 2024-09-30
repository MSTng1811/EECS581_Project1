"""
Program Name: place_ships.py

Description:
This program handles the logic for ship placement in a Pygame-based Battleship game. It manages the process of both Player 1 and Player 2 placing their ships on the game board. It includes functionality to check the validity of ship placement, ensure ships are placed adjacent to each other, and handle ship addition to the board.

Inputs:
- screen: The Pygame screen surface.
- ships: Array of ship lengths to be placed by the player.
- placedShips: 2D array representing ships that have been placed on the game board.
- shipBoard: 2D array representing the player's ship grid.
- pos: Mouse position for determining where the player is trying to place the ship.

Output:
- Updates the Pygame screen with the ship placements.
- Returns the updated arrays for player1 and player2 ship placements and the grid.

Code Sources:
- https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python (measuring elapsed time).
- https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame (handling Pygame rectangle grids and user clicks).

Author: Zai Erb

Creation Date: September 21, 2024
"""


from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text
import time
import random

# handles placing of player 1s ships
def placePlayer1Ships(screen, ships, placedShips, shipBoard):
    player_ship_coords = []  # List to track the coordinates of placed ships
    
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    print("Length", shipsCopy[0])
    initialLength = shipLength
    startTime = time.time()  # Start tracking time

    while len(shipsCopy) > 0:
        currentTime = time.time()
        
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()

        if shipLength > 0:
            stringofint = str(initialLength)
            toDisplay = 'Player 1, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            add_text.add_labels_ships(screen)
            add_text.add_labels_middle(screen)
            
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips, [])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Attempt to place the ship
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    
                    if wasPlaced:
                        print("Player pos", pos)
                        startTime = time.time()
                        shipLength -= 1
                        
                        # Assuming that `addShip` updates the board with the ship's coordinates
                        # and `pos` is the top-left coordinate where the ship starts
                        # Get ship coordinates and append to player_ship_coords
                        player_ship_coords.append(pos)

            pygame.display.update()
        else:
            shipsCopy.pop(0)
            if len(shipsCopy) != 0:
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index += 1

    # Now you have all ship coordinates in player_ship_coords
    print("Player 1 placed ships at:", player_ship_coords)
    return player_ship_coords  # Return the list of ship coordinates

# same as above but for player 2
def placePlayer2Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    startTime = time.time()
    while len(shipsCopy) > 0:
        currentTime = time.time()
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            toDisplay = 'Player 2, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips, [])
            # createPlayer1ShipGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    if(wasPlaced):
                        startTime = time.time()
                        shipLength = shipLength - 1
                   
            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1


def placeAiShips(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    startTime = time.time()

    while len(shipsCopy) > 0:
        currentTime = time.time()
        
        # Timeout logic (if needed)
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()

        if shipLength > 0:
            # Randomly select orientation (0 for horizontal, 1 for vertical)
            orientation = random.randint(0, 1)

            # Ensure the random position is valid for the given ship length and orientation
            if orientation == 0:  # Horizontal
                row = random.randint(0, 9)
                col = random.randint(0, 9 - shipLength + 1)  # Ensure ship fits horizontally
            else:  # Vertical
                row = random.randint(0, 9 - shipLength + 1)
                col = random.randint(0, 9)  # Ensure ship fits vertically

            # Add the ship one segment at a time by calculating the positions
            valid_position = True
            temp_ship = []

            for i in range(shipLength):
                if orientation == 0:  # Horizontal placement
                    pos = shipBoard[row][col + i].topleft
                    temp_ship.append(shipBoard[row][col + i])
                else:  # Vertical placement
                    pos = shipBoard[row + i][col].topleft
                    temp_ship.append(shipBoard[row + i][col])

                # Check if any part of this ship would overlap with an existing ship
                if any(temp_rect in ship for ship in placedShips for temp_rect in temp_ship):
                    valid_position = False
                    break

            if valid_position:
                # If the ship can be placed, add it to the placedShips array
                for i in range(shipLength):
                    if orientation == 0:
                        placedShips[index].append(shipBoard[row][col + i])
                    else:
                        placedShips[index].append(shipBoard[row + i][col])

                print(f"AI placed ship {index + 1} at: {[(row, col) for _ in range(shipLength)]}")
                startTime = time.time()  # Reset the start time
                shipLength = 0  # Ship has been placed, move on to the next one
            else:
                # If placement was invalid, try again
                print(f"Invalid placement for ship at row {row}, col {col}. Retrying...")
                continue  # Skip the rest of the loop and retry

            pygame.display.update()
        else:
            # Once the ship is placed, move on to the next one
            shipsCopy.pop(0)
            if len(shipsCopy) > 0:
                index += 1
                shipLength = shipsCopy[0]
                initialLength = shipLength



# handles logic for adding ship
def addShip(shipBoard, placedShips, index, pos):
    # starts at false
    shipAdded = False
    # gets the current ship
    currentShip = placedShips[index]
    # get rectangle that was selected
    rect = battleship.getRectangle(shipBoard, pos)
    # if row is invalid, make user click new spot
    if battleship.getRow(shipBoard, rect) == -1 or battleship.getCol(shipBoard, rect) == -1:
        return(placedShips, shipAdded) 
    # otherwise if it is a new ship make sure it is not already placed
    if(len(currentShip) == 0):
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
            shipAdded = True
    else:
        # if ship already exists, check that new addition isn't already placed and check that it touches the current ship
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            touchesShipCheck = touchesShip(shipBoard, placedShips, index, pos)
            if touchesShipCheck:
                currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
                shipAdded = True
    # add current ship to placedships
    placedShips[index] = currentShip
    # return placed ships and a bool of if it was added
    return (placedShips, shipAdded)

# checks that your placement touches the part of the ship already placed
def touchesShip(shipBoard, placedShips, index, pos):
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    row = battleship.getRow(shipBoard, rect)
    col = battleship.getCol(shipBoard, rect)
    # if length is 1, it can be above, below, or either side
    if len(currentShip) == 1:
        for ship in currentShip:
            currentRow = battleship.getRow(shipBoard, ship)
            currentCol = battleship.getCol(shipBoard, ship)
            if row == currentRow:
                difference = abs(col-currentCol)
                if difference == 1:
                    return True
            elif col == currentCol:
                difference = abs(row-currentRow)
                if difference == 1:
                    return True
    else:
        # if length isn't one you need to check that it is aligned with currentship
        ship1 = currentShip[0]
        ship2 = currentShip[1]
        ship1row = battleship.getRow(shipBoard, ship1)
        ship2row = battleship.getRow(shipBoard, ship2)
        ship1col = battleship.getCol(shipBoard, ship1)
        ship2col = battleship.getCol(shipBoard, ship2)
        if ship1row == ship2row:
            for ship in currentShip:
                shiprow = battleship.getRow(shipBoard, ship)
                if row == shiprow:
                    shipcol = battleship.getCol(shipBoard, ship)
                    difference = abs(shipcol-col)
                    if difference == 1:
                        return True
        elif ship2col == ship1col:
            for ship in currentShip:
                shipcol = battleship.getCol(shipBoard, ship)
                if col == shipcol:
                    shiprow = battleship.getRow(shipBoard, ship)
                    difference = abs(shiprow-row)
                    if difference == 1:
                        return True
    return False



# checks if rect has already been placed
def inShips(placedShips, pos):
    for x in range(0, len(placedShips)):
        for y in range(0, len(placedShips[x])):
            tempRect = (placedShips[x])[y]
            if tempRect.collidepoint(pos):
                return True
    return False

# adds ship to current ship
def addToShips(placedShips, pos, currentShip, shipBoard):
    for x in range(0, 10):
        for y in range(0, 10):
            tempRect = (shipBoard[x])[y]
            if tempRect.collidepoint(pos):
                currentShip.append(tempRect)
                return currentShip
    return currentShip
    

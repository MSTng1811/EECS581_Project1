import copy
import random
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
import get_difficulty


def calculate_position_from_grid(row, col, grid_type="target"):
    # Cell size is 20x20 pixels, as defined in createPlayer1TargetGrid
    cell_size = 20

    # Starting positions for each grid type (ships or target)
    if grid_type == "ships":
        offset_x = 40  # X offset for player ships grid
        offset_y = 110  # Y offset for player ships rows
    else:  # Target grid
        offset_x = 260  # X offset for AI target grid (starts at 260)
        offset_y = 100  # Y offset for rows (starts at 100 for the target grid)

    # Calculate the top-left corner of the grid cell
    x = offset_x + col * cell_size
    y = offset_y + row * cell_size
    return (x, y)



def ai_easy(player_ships, target_board, hits, misses, valid_moves):
    """AI fires randomly in easy mode using a list of valid moves."""
    if not valid_moves:
        print("No more valid moves left for the AI.")
        return

    # Randomly select a position from valid moves
    row, col = random.choice(valid_moves)

    # Remove the selected move from valid moves so the AI doesn't shoot here again
    valid_moves.remove((row, col))

    # Calculate the top-left pixel position from the row and column
    pos = calculate_position_from_grid(row, col, grid_type="target")

    print(f"AI is attempting to shoot at grid position: ({row}, {col}) which maps to screen position {pos}")

    # Check for valid move before attempting to check for collision
    played = battleship.checkForCollision(
        battleship.player2TargetBoard,  # AI's target board (where AI shoots)
        battleship.player1ShipBoard,    # Player's ship board (Player's ships that AI is attacking)
        pos,                            # AI's randomly selected position (converted to coordinates)
        battleship.player2hits,         # AI's hit list
        battleship.player2misses,       # AI's miss list
        battleship.player1placedShips,  # Player's placed ships (being attacked by AI)
        copy.deepcopy(battleship.player1placedShips)  # Deep copy of player's ships to track state
    )

    if played:
        print(f"AI successfully played at: ({row}, {col})")
        battleship.player1Turn = True  # Add this line to switch back to player turn
    else:
        print(f"AI's move at ({row}, {col}) - ({pos}) was invalid.")
        print(f"Hits: {hits}, Misses: {misses}")

def get_adjacent_cells(row, col, valid_moves):
    """Returns valid adjacent cells around the (row, col) coordinate."""
    adjacent_cells = []
    potential_moves = [
        (row - 1, col),  # Up
        (row + 1, col),  # Down
        (row, col - 1),  # Left
        (row, col + 1),  # Right
    ]
    for move in potential_moves:
        if move in valid_moves:
            adjacent_cells.append(move)
    return adjacent_cells

def ai_medium(player_ships, target_board, hits, misses, valid_moves, last_hit=None, ship_in_progress=None, direction=None):
    """AI fires randomly until it hits, then fires adjacent cells until the ship is sunk."""
    if not valid_moves:
        print("No more moves left for the AI")
        return last_hit, ship_in_progress, direction
    if ship_in_progress:
        # If there's a ship being attacked, target adjacent cells
        row, col = ship_in_progress
        if direction == "up" and (row - 1, col) in valid_moves:
            row, col = row - 1, col
        elif direction == "down" and (row + 1, col) in valid_moves:
            row, col = row + 1, col
        elif direction == "left" and (row, col - 1) in valid_moves:
            row, col = row, col - 1
        elif direction == "right" and (row, col + 1) in valid_moves:
            row, col = row, col + 1
        else:
            # If the direction is blocked, reset and try adjacent cells from the original hit
            direction = None
        if not direction:
            # Choose a new direction from adjacent cells
            adjacent_cells = get_adjacent_cells(last_hit[0], last_hit[1], valid_moves)
            if adjacent_cells:
                row, col = random.choice(adjacent_cells)
                valid_moves.remove((row, col))
                # Set the direction based on the move
                if row < last_hit[0]:
                    direction = "up"
                elif row > last_hit[0]:
                    direction = "down"
                elif col < last_hit[1]:
                    direction = "left"
                elif col > last_hit[1]:
                    direction = "right"
            else:
                # If no adjacent cells, fire randomly
                row, col = random.choice(valid_moves)
                ship_in_progress = None
                direction = None
    else:
        # If no adjacent cells are valid, fire randomly again
        row, col = random.choice(valid_moves)
        valid_moves.remove((row, col))
    # Calculate pos from the grid
    pos = calculate_position_from_grid(row, col, grid_type="target")
    print(f"AI (medium) is attempting to shoot at grid position: ({row}, {col}) which maps to screen position {pos}")
    # Check for valid move before attempting to check for collision
    played = battleship.checkForCollision(
        battleship.player2TargetBoard,  # AI's target board (where AI shoots)
        battleship.player1ShipBoard,    # Player's ship board (Player's ships that AI is attacking)
        pos,                            # AI's randomly selected position (converted to coordinates)
        battleship.player2hits,         # AI's hit list
        battleship.player2misses,       # AI's miss list
        battleship.player1placedShips,  # Player's placed ships (being attacked by AI)
        copy.deepcopy(battleship.player1placedShips)  # Deep copy of player's ships to track state
    )
    if played:
        print(f"AI successfully played at: ({row}, {col})")
        # If the shot hit a ship, update the `ship_in_progress` to continue targeting adjacent cells
        if battleship.inShips(battleship.player1placedShips, (row, col)):
            print("AI hit a ship!")
            ship_in_progress = (row, col)
            last_hit = (row, col)
        else:
            direction = None
        # Check if a ship was sunk
        if battleship.shipSunk(battleship.copyPlayer1placedShips):
            print("AI sunk a ship!")
            ship_in_progress = None  # Reset targeting if the ship is sunk
            last_hit = None
            direction = None
        battleship.player1Turn = True  # Switch to player turn after AI finishes
    else:
        print(f"AI's move at ({row}, {col}) - ({pos}) was invalid.")
    return last_hit, ship_in_progress, direction
    
def ai_hard():
    """AI always hits a ship in hard mode by targeting known ship rectangles."""
    player_ships_rects = battleship.player1placedShips
    # Iterate through each ship (which is a list of rects)
    for ship in player_ships_rects:
        # Iterate through each rectangle (part of the ship)
        for ship_rect in ship:
            # Get the center of the rectangle (AI targets the center point of the ship's rect)
            pos = (ship_rect.centerx + 230, ship_rect.centery)

            # Call checkForCollision for the center of the ship rectangle
            played = battleship.checkForCollision(
                battleship.player2TargetBoard,  # AI's target board (where AI shoots)
                battleship.player1ShipBoard,    # Player's ship board (Player's ships that AI is attacking)
                pos,                            # AI's selected position (the center of the ship's rect)
                battleship.player2hits,         # AI's hit list
                battleship.player2misses,       # AI's miss list
                battleship.player1placedShips,  # Player's placed ships (being attacked by AI)
                battleship.copyPlayer1placedShips  # Deep copy of player's ships to track state
            )

            if played:
                print(f"AI hits at {pos}.")
                # Check if the ship was sunk
                sunkenShip = battleship.shipSunk(battleship.copyPlayer1placedShips)  # Check if player ship was sunk
                if sunkenShip:
                    add_text.add_text(battleship.SCREEN, 'The AI sunk one of your ships!')
                    pygame.display.update()

                # Check if all of the player's ships have been sunk (end game)
                if battleship.gameIsOver(battleship.copyPlayer1placedShips):
                    battleship.gameover = True
                    add_text.add_text(battleship.SCREEN, 'AI wins! All Player ships sunk.')
                    pygame.display.update()
                    return  # End the game when all player ships are sunk
                else:
                    battleship.player1Turn = True  # Switch back to player's turn after a hit
                return  # End AI's turn after a valid move

        print("SHIPS", battleship.player1placedShips)

    print(f"AI's move at ({pos}) was invalid.")





def run():

    ai_difficulty = get_difficulty.set_difficulty(battleship.SCREEN)
    print("singleplayer mode with AI difficulty:", ai_difficulty)

    # Get the number of ships that the user wants for the game and returns arrays
    arrays = get_ships_num.get_ships(
        battleship.player1ships,
        battleship.player2ships,
        battleship.SCREEN,
        battleship.player1placedShips,
        battleship.player2placedShips
    )
    
    battleship.player1ships = arrays[0]
    battleship.player2ships = arrays[1]
    battleship.player1placedShips = arrays[2]
    battleship.player2placedShips = arrays[3]

    # Calculate the total number of ship parts for Player 1
    total_player_ship_parts = sum(len(ship) for ship in battleship.player1placedShips)

    last_ai_hit = None  # Track last AI hit for medium difficulty
    ship_in_progress = None  # Track if AI is focusing on sinking a ship
    direction = None

    # Initialize list of all valid moves (positions (x, y) on the 10x10 grid)
    valid_moves = [(x, y) for x in range(10) for y in range(10)]

    # Player 1 places ships manually
    while not battleship.player1ready:
        player_ship_coords = place_ships.placePlayer1Ships(
            battleship.SCREEN,
            battleship.player1ships,
            battleship.player1placedShips,
            battleship.player1ShipBoard
        )
        battleship.player1ready = True
        battleship.copyPlayer1placedShips = battleship.createShallowCopy(battleship.player1placedShips)


    # AI places ships automatically
    if not battleship.player2ready:
        place_ships.placeAiShips(
            battleship.SCREEN,
            battleship.player2ships,
            battleship.player2placedShips,
            battleship.player2ShipBoard
        )
        battleship.player2ready = True
        battleship.copyPlayer2placedShips = battleship.createShallowCopy(battleship.player2placedShips)

    # Main game loop (Player vs AI turns)
    turn_counter = 0  # Count the turns to track progress

    while not battleship.gameover:
        pos = pygame.mouse.get_pos()

        add_text.add_text(battleship.SCREEN, 'Battleship')
        add_text.add_labels_targets(battleship.SCREEN)

        # Player 1's turn
        if battleship.player1Turn:
            add_text.add_text(battleship.SCREEN, 'Player 1 Turn')
            battleship.printAIShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits, battleship.player2misses, False)
            battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Player is attempting to shoot at mouse position: {pos}")
                    played = battleship.checkForCollision(
                        battleship.player1TargetBoard,
                        battleship.player2ShipBoard,
                        pos,
                        battleship.player1hits,
                        battleship.player1misses,
                        battleship.player2placedShips,
                        battleship.copyPlayer2placedShips
                    )
                    if played:
                        print(f"Player's shot at {pos} was valid.")
                        battleship.player1Turn = False  # Switch to AI's turn after valid move
                        pygame.time.wait(1000)

                        # Check if a ship was sunk
                        ship_sunk = battleship.shipSunk(battleship.copyPlayer2placedShips)
                        if ship_sunk:
                            print("You sunk an AI ship!")
                            add_text.add_text(battleship.SCREEN, 'You sunk an AI ship!')
                            pygame.display.update()
                            pygame.time.wait(2000)

                        # Check if all ships are sunk (end game)
                        game_over = battleship.gameIsOver(battleship.copyPlayer2placedShips)
                        if game_over:
                            print("All AI ships have been sunk. Player wins!")
                            add_text.add_text(battleship.SCREEN, 'Player wins! All AI ships sunk.')
                            pygame.display.update()
                            pygame.time.wait(3000)
                            battleship.gameover = True
                            break
                    else:
                        print(f"Player's shot at {pos} was invalid.")

        # AI's turn
        else:
            print(f"AI's turn {turn_counter}: AI is thinking...")
            # print(f"Valid moves: {valid_moves}")

            print("player 2 misses", battleship.player2misses)
            print("player 2 hits", battleship.player2hits)
            # Display AI's board showing hits and misses during the AI's turn
            add_text.add_text(battleship.SCREEN, 'AI Turn')
            battleship.printAIShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits, battleship.player1misses, True)
            battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)


            # Let the AI make its move based on the difficulty
            if ai_difficulty == "easy":
                ai_easy(
                    battleship.player1placedShips,
                    battleship.player2TargetBoard,
                    battleship.player2hits,
                    battleship.player2misses,
                    valid_moves  # Pass the valid moves list to the AI
                )
            elif ai_difficulty == "medium":
                last_ai_hit, ship_in_progress, direction = ai_medium(
                    battleship.player1placedShips,
                    battleship.player2TargetBoard,
                    battleship.player2hits,
                    battleship.player2misses,
                    valid_moves,
                    last_hit=last_ai_hit,
                    ship_in_progress=ship_in_progress,
                    direction=direction
                )
            elif ai_difficulty == "hard":
                ai_hard()
                battleship.player1Turn = 1

            # Check if the AI sunk a ship after its move
            sunkenShip = battleship.shipSunk(battleship.copyPlayer1placedShips)  # Player's ships
            if(sunkenShip):
                add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                pygame.display.update()
                ended = battleship.gameIsOver(battleship.copyPlayer2placedShips)
                if ended:
                    battleship.gameover = True
                    add_text.add_text(battleship.SCREEN, 'Player 1 won!')
                    pygame.display.update()


        turn_counter += 1  # Increment turn counter
        pygame.display.update()






import copy
import random
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship

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
    else:
        print(f"AI's move at ({row}, {col}) - ({pos}) was invalid.")
        print(f"Hits: {hits}, Misses: {misses}")








def ai_medium(player_ships, target_board, hits, misses, last_hit=None):
    """AI fires randomly until it hits, then fires adjacent cells to sink ships."""
    if last_hit:
        x, y = last_hit
        # Check adjacent cells
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and target_board[nx][ny] == 0:
                pos = target_board[nx][ny].topleft
                if battleship.checkForCollision(target_board, player_ships, pos, hits, misses, player_ships, copy.deepcopy(player_ships)):
                    return (nx, ny)
    # If no hit, fire randomly
    ai_easy(player_ships, target_board, hits, misses)

def ai_hard(player_ships, target_board, hits, misses):
    """AI always hits a ship in hard mode."""
    for x in range(10):
        for y in range(10):
            if(player_ships[x][y] > 0 and target_board[x][y] == 0):
                pos = target_board[x][y].topleft
                battleship.checkForCollision(target_board, player_ships, pos, hits, misses, player_ships, copy.deepcopy(player_ships))
                return



def run(ai_difficulty="easy"):
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

    last_ai_hit = None  # Track last AI hit for medium difficulty

    # Initialize list of all valid moves (positions (x, y) on the 10x10 grid)
    valid_moves = [(x, y) for x in range(10) for y in range(10)]

    # Player 1 places ships manually
    while not battleship.player1ready:
        place_ships.placePlayer1Ships(
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
            battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
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
            print(f"Valid moves: {valid_moves}")

            # Display AI's board showing hits and misses during the AI's turn
            add_text.add_text(battleship.SCREEN, 'AI Turn')
            battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits)
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

            # Check if the player sunk a ship after their move
            ship_sunk = battleship.shipSunk(battleship.copyPlayer2placedShips)  # AI's ships
            if ship_sunk:
                print("You sunk an AI ship!")
                add_text.add_text(battleship.SCREEN, 'You sunk an AI ship!')
                pygame.display.update()
                pygame.time.wait(2000)  # Pause for 2 seconds to show the message

            # Check if all AI ships are sunk to end the game
            game_over = battleship.gameIsOver(battleship.copyPlayer2placedShips)
            if game_over:
                print("All AI ships have been sunk. Player wins!")
                add_text.add_text(battleship.SCREEN, 'Player wins! All AI ships sunk.')
                pygame.display.update()
                pygame.time.wait(3000)
                battleship.gameover = True  # End the game
                break  # Exit the game loop

        turn_counter += 1  # Increment turn counter
        pygame.display.update()





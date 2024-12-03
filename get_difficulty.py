import pygame
import sys
import add_text

# RGB colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

# Function to handle difficulty selection
def set_difficulty(screen):
    add_text.add_text(screen, 'Choose Difficulty')
    optionsChosen = False
    
    # Place the options and save the rects
    rects = place_options(screen)  # Get the list of rects (rect1, rect2, rect3)
    
    # Update the display to render the options
    pygame.display.update()

    while not optionsChosen:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the index for difficulty
                for i, rect in enumerate(rects):  # Loop through rects and check clicks
                    if rect.collidepoint(pos):
                        optionsChosen = True
                        screen.fill(BLACK, (0, 0, 490, 400))
                        pygame.display.update()
                        if i == 0:
                            return "easy"
                        elif i == 1:
                            return "medium"
                        elif i == 2:
                            return "hard"



# Function to place the difficulty options on the screen
def place_options(screen):
    screen_width = 490  # Assuming the screen width is 490
    screen_height = 400  # Assuming the screen height is 400
    button_width = 100  # Width of each button
    button_height = 50  # Height of each button
    spacing = 20  # Space between buttons

    # Calculate the total width of all buttons plus spacing for horizontal alignment
    total_width = (button_width * 3) + (spacing * 2)

    # Calculate starting x position to center the buttons horizontally
    start_x = (screen_width - total_width) // 2

    # Calculate y position to center the buttons vertically
    start_y = (screen_height - button_height) // 2  # Vertically centered

    # Create the button rects, spaced evenly
    rect1 = pygame.Rect(start_x, start_y, button_width, button_height)
    rect2 = pygame.Rect(start_x + button_width + spacing, start_y, button_width, button_height)
    rect3 = pygame.Rect(start_x + (button_width + spacing) * 2, start_y, button_width, button_height)

    # Draw the buttons
    pygame.draw.rect(screen, WHITE, rect1, 1)
    pygame.draw.rect(screen, WHITE, rect2, 1)
    pygame.draw.rect(screen, WHITE, rect3, 1)

    # Add text to the buttons for difficulty
    font = pygame.font.Font('freesansbold.ttf', 16)

    text = font.render('Easy', True, RED)
    textRect = text.get_rect()
    textRect.center = rect1.center
    screen.blit(text, textRect)

    text = font.render('Medium', True, RED)
    textRect = text.get_rect()
    textRect.center = rect2.center
    screen.blit(text, textRect)

    text = font.render('Hard', True, RED)
    textRect = text.get_rect()
    textRect.center = rect3.center
    screen.blit(text, textRect)

    # Return the rects for collision detection
    return [rect1, rect2, rect3]




# Function to get which difficulty option was selected
def get_index(screen, pos):
    offset = 45
    # Create rects for difficulty levels
    rect1 = pygame.Rect(100 + offset, 150, 100, 50)
    rect2 = pygame.Rect(240 + offset, 150, 100, 50)
    rect3 = pygame.Rect(160 + offset, 220, 100, 50)


    # Check which button was clicked
    if rect1.collidepoint(pos):
        print(f"Button 1 clicked")
        return 1
    elif rect2.collidepoint(pos):
        print(f"Button 2 clicked")
        return 2
    elif rect3.collidepoint(pos):
        print(f"Button 3 clicked")
        return 3
    return -1

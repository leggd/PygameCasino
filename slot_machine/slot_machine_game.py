import pygame
import os
import sys
import subprocess
import random

# Import functions from card_deck and player modules from game assets folder
current_script_path = os.path.abspath(__file__)

# Get the directory of the current game
game_dir = os.path.dirname(current_script_path)

# Get the parent directory of the game directory
parent_dir = os.path.dirname(game_dir)
game_assets = os.path.join(parent_dir, "game_assets")

# Construct the path to player.py in the parent directory
player_script_path = os.path.join(game_assets, "player.py")

# Construct the path to font file in the parent directory
font_path = os.path.join(game_assets, "gnu.ttf")

# Ensure the player module is saving to root game folder
sys.path.append(game_assets)

# Import module from game_assets folder
from player import load, save, get_info

# Initialise Pygame
pygame.init()

# Initialise Screen Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Initialise Slot Constants
SLOT_ROWS = 3
SLOT_COLS = 5

# Initialise Slot Box Sizes
BOX_WIDTH = 1000 // SLOT_COLS
BOX_HEIGHT = 600 // SLOT_ROWS

# Initialise Colour Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (28, 21, 105)

# Initialise Pygame Screen and Caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine")

# Initialise font variable
font = pygame.font.Font(font_path, 24)

# Change working directory for proper loading of graphics in game folder
os.chdir(game_dir)

#  Initialise all image variables with try/except in case game is ran standalone
try:
    grid = pygame.image.load('graphics/grid_white_bg.png')
except:
    grid = pygame.image.load('slot_machine/graphics/grid_white_bg.png')

# Initialise Slot Grid X and Y size variables
grid_x = (SCREEN_WIDTH - grid.get_width()) // 2
grid_y = (SCREEN_HEIGHT - grid.get_height()) // 2

try:
    background = pygame.image.load('graphics/background.png')
except:
    background = pygame.image.load('slot_machine/graphics/background.png')

try:
    menu_background = pygame.image.load("graphics/menu_background.png").convert()
except:
    menu_background = pygame.image.load("slot_machine/graphics/menu_background.png").convert()

# Transform Menu Background Image to fit game screen resolution
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  Initialise all image variables with try/except in case game is ran standalone
try:
    ELEPHANT = pygame.image.load('graphics/symbols/elephant.png')
    GIRAFFE = pygame.image.load('graphics/symbols/giraffe.png')
    LION = pygame.image.load('graphics/symbols/lion.png')
    ZEBRA = pygame.image.load('graphics/symbols/zebra.png')
    FLAMINGO = pygame.image.load('graphics/symbols/flamingo.png')
    BOAR = pygame.image.load('graphics/symbols/boar.png')
    PAWS = pygame.image.load('graphics/symbols/paws.png')
    TIGER = pygame.image.load('graphics/symbols/tiger.png')
    TREE = pygame.image.load('graphics/symbols/tree.png')
    TURTLE = pygame.image.load('graphics/symbols/turtle.png')
except:
    ELEPHANT = pygame.image.load('slot_machine/graphics/symbols/elephant.png')
    GIRAFFE = pygame.image.load('slot_machine/graphics/symbols/giraffe.png')
    LION = pygame.image.load('slot_machine/graphics/symbols/lion.png')
    ZEBRA = pygame.image.load('slot_machine/graphics/symbols/zebra.png')
    FLAMINGO = pygame.image.load('slot_machine/graphics/symbols/flamingo.png')
    BOAR = pygame.image.load('slot_machine/graphics/symbols/boar.png')
    PAWS = pygame.image.load('slot_machine/graphics/symbols/paws.png')
    TIGER = pygame.image.load('slot_machine/graphics/symbols/tiger.png')
    TREE = pygame.image.load('slot_machine/graphics/symbols/tree.png')
    TURTLE = pygame.image.load('slot_machine/graphics/symbols/turtle.png')

# Initialise tuple of symbol pygame objects 
SYMBOLS = (
    ELEPHANT,
    GIRAFFE,
    LION,
    ZEBRA,
    FLAMINGO,
    BOAR,
    PAWS,
    TIGER,
    TREE,
    TURTLE)

# Initialise dictionary of reel symbol frequencies
FREQUENCY = {
    ELEPHANT: 50,
    GIRAFFE: 30,
    LION: 20,
    ZEBRA: 40,
    FLAMINGO: 35,
    BOAR: 45,
    PAWS: 35,
    TIGER: 25,
    TREE: 45,
    TURTLE: 30}

# Initialise dictionary of reel symbol values
SYMBOL_VALUES = {
    ELEPHANT: 0.4, 
    GIRAFFE: 0.9, 
    LION: 6, 
    ZEBRA: 1, 
    FLAMINGO: 1.2, 
    BOAR: 0.7, 
    PAWS: 0.8, 
    TIGER: 3, 
    TREE: 0.9, 
    TURTLE: 1.3} 

# Initialise Game Variables
game_state = ''
player_name = ""
player_bet = 0
current_player = None
paused = False
how_to = False
valid_rebet = None
current_delay = 0
delay_increment = 40
spinning = False
stop_reel = 0
autoplay_mode = False
win_line = 0
symbol_value = 0
win = False
winnings = 0

# Function to toggle autoplay mode
def toggle_autoplay():
    global autoplay_mode
    autoplay_mode = not autoplay_mode
    if autoplay_mode:
        toggle_spin()  # Start spinning when autoplay is enabled

# Function to generate text standard
def draw_text(text, color, x, y, font_size=None, bold=False):
    # Use the global font size if no specific size is provided
    if font_size is None:
        used_font = font
    else:
        # Create a new font object with the specified size
        used_font = pygame.font.Font(font_path, font_size)

    # Set bold attribute
    used_font.set_bold(bold)

    # Render text
    text_surface = used_font.render(text, True, color)
    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()

    # Set the position of the text
    text_rect.center = (x, y)
    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)

# Function to generate text with additional customisation
def draw_more_text(text, color, x, y, font_size=None, bold=False):
    # Use the global font size if no specific size is provided
    if font_size is None:
        used_font = font
    else:
        # Create a new font object with the specified size
        used_font = pygame.font.Font(font_path, font_size)

    # Set bold attribute
    used_font.set_bold(bold)

    # Render text
    text_surface = used_font.render(text, True, color)
    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()
    # Set the position of the text
    text_rect.topleft = (x, y)
    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)

# Function to draw buttons on the screen
def draw_button(text, colour, rect, action):
    # Draw button rectangle
    pygame.draw.rect(screen, colour, rect)
    # Draw text on button
    draw_more_text(text, BLACK, rect.x + 10, rect.y + 10)

    # Get mouse position
    mouse = pygame.mouse.get_pos()

    # Check if mouse is hovering over button
    if rect.x + rect.width > mouse[0] > rect.x and rect.y + rect.height > mouse[1] > rect.y:
        # Highlight button if mouse is over it
        pygame.draw.rect(screen, WHITE, rect)
        # Check for mouse click on button
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # Execute action associated with the button
                action()

# Function to quit the game gracefully
def quit_game():
    pygame.quit()
    sys.exit()

# Function to toggle pause menu boolean
def toggle_pause():
    global paused
    if paused == True:
        paused = False  # Resume the game
    else:
        paused = True   # Pause the game

# Function to reset slot machine variables
def reset_machine():
    global boxes, spinning_reels, slot_symbols, symbol_indexes, autoplay_mode
    boxes = []
    spinning_reels = []
    slot_symbols = []
    symbol_indexes = []
    autoplay_mode = False

    # Populate lists with placeholders for boxes to be filled with symbols
    for _ in range(SLOT_ROWS):
        row = []
        for _ in range(SLOT_COLS):
            row.append(None)
        boxes.append(row)

    # Populate list which tracks spinning state of all reels, spinning by default
    for _ in range(SLOT_COLS):
        spinning_reels.append(True)

    # Populate each box with symbols and shuffle the slot reels
    for _ in range(SLOT_COLS):
        reel_symbols = []
        for symbol, freq in FREQUENCY.items():
            for _ in range(freq):
                reel_symbols.append(symbol)
        random.shuffle(reel_symbols)
        slot_symbols.append(reel_symbols)

    # Populate symbol index list with placeholders
    for _ in range(SLOT_COLS):
        symbol_indexes.append(0)

# Function to start game
def start_game():
    global current_player, player_bet, player_name, balance
    # Resets reels and values
    reset_machine()
    # Initialises player and player bet if not already initialised
    if current_player is None:
        player_name = get_name()
        # Change working directory for access/create save_file.txt in game_assets folder
        os.chdir(game_assets)
        current_player = load(player_name)
    if player_bet == 0:
        # Change working directory for access/create save_file.txt in game_assets folder
        os.chdir(game_assets)
        balance = get_info(current_player)[1]
        player_bet = get_bet(balance)
    # Adjust balances and ensure balance is current
    balance_adjustment = -player_bet
    # Change working directory for access/create save_file.txt in game_assets folder
    os.chdir(game_assets)
    save(current_player, balance_adjustment)
    current_player = load(player_name)
    balance = get_info(current_player)[1]
    return

# Function to rebet and play another round
def play_again():
    global game_state
    # Check if rebet will exceed player balance
    if player_bet > balance:
        return False
    else:
    # If rebet doesn't exceed player balance, run the game again, resetting game state
        game_state = ''
        main()

# Function to handle name input
def get_name():
        empty_input = None
        invalid_input = None
        # Initialise input box for the player's name
        input_box = pygame.Rect((SCREEN_WIDTH - 200) // 2, 200, 200, 50)
        # Initialise empty string to store the player's name
        player_name = ''
        # Set the active flag to True
        active = True

        # Infinite loop to check for events
        while True:
            # Iterate over all the events
            for event in pygame.event.get():
                # If the event is QUIT, call the quit_game function
                if event.type == pygame.QUIT:
                    quit_game()
                # If the event is a key press
                if event.type == pygame.KEYDOWN:
                    # If the input box is active
                    if active:
                        # If the key pressed is RETURN, return the player's name
                        if event.key == pygame.K_RETURN:
                            player_name = player_name.strip()
                            if not player_name:
                                empty_input = True
                                invalid_input = None
                            elif any(char.isdigit() for char in player_name):
                                invalid_input = True
                                empty_input = None
                            else:
                                empty_input = None
                                invalid_input = None
                                player_name = player_name.capitalize()
                                return player_name
                        # If the key pressed is BACKSPACE, remove the last character from the player's name
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        # Otherwise, add the key pressed to the player's name
                        else:
                            player_name += event.unicode
            # Fill the screen with the background image
            screen.blit(menu_background, (0, 0))
            # Draw the text "Enter your name:" on the screen
            draw_more_text("Enter your name:", BLACK, (SCREEN_WIDTH - 200) // 2, 150)
            # Draw the input box on the screen
            pygame.draw.rect(screen, BLACK, input_box, 2)
            # Draw the player's name inside the input box as its being entered
            draw_more_text(player_name, BLACK, input_box.x + 5, input_box.y + 5)
            if empty_input:
                draw_more_text("You didn't enter anything!", BLACK, 450, 275)
            if invalid_input:
                draw_more_text("You can't have numbers in your name!", BLACK, 390, 275)
            # Update the display
            pygame.display.flip()

# Function to handle bet input
def get_bet(balance):
    # Initialise input box for the player's bet
    input_box = pygame.Rect((SCREEN_WIDTH - 200) // 2, 200, 200, 50)
    # Initialise empty string to store the bet
    text = ''
    # Initialise input flags
    active = True
    insufficient_balance = None
    invalid_bet = None

    # Infinite loop to check for events
    while True:
        # Iterate over all the events
        for event in pygame.event.get():
            # If the event is QUIT, call the quit_game function
            if event.type == pygame.QUIT:
                quit_game()
            # If the event is a key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    toggle_pause()
                # If the input box is active
                if active:
                    # If the key pressed is RETURN
                    if event.key == pygame.K_RETURN:
                        try:
                            # Try to convert the text to an integer and assign it to bet
                            bet = int(text)
                            # If the bet is greater than 0 and less than or equal to the balance
                            if bet > 0 and bet <= balance:
                                return bet
                            else:
                                insufficient_balance = True
                                invalid_bet = False
                        except ValueError:
                            invalid_bet = True
                            insufficient_balance = False
                    # If the key pressed is BACKSPACE, remove the last character from the text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    # Otherwise, add the key pressed to the text
                    else:
                        # This try/except catches an AttributeError crashing the program that I could not debug
                        # I think it is an issue with pygame itself. If this is removed, it gives error upon new_bet():
                        #    text += event.unicode
                        #            ^^^^^^^^^^^^^
                        # AttributeError: 'pygame.event.Event' object has no attribute 'unicode'
                        try:
                            text += event.unicode
                        except:
                            continue
        
        # Fill the screen with the background image
        screen.blit(menu_background, (0, 0))
        # Input Error Handling Messages
        if insufficient_balance:
            draw_more_text("Insufficient Balance", BLACK, 480, 275)
        if invalid_bet:
            draw_more_text("Invalid Bet", BLACK, 530, 275)
        # Draw the balance on the screen
        draw_more_text("Balance: " + str(balance), BLACK, (SCREEN_WIDTH - 200) // 2, 100)
        # Draw the text "Place your bet:" on the screen
        draw_more_text("Place your bet:", BLACK, (SCREEN_WIDTH - 200) // 2, 150)
        # Draw the input box on the screen
        pygame.draw.rect(screen, BLACK, input_box, 2)
        # Draw the text inside the input box
        draw_more_text(text, BLACK, input_box.x + 5, input_box.y + 5)
        # Update the display
        pygame.display.flip()

# Function to initiate a new bet with the same player after round ends
def new_bet():
    global player_bet
    player_bet = 0
    play_again()

# Function to iterate through slot reel lists
def spin_reels():
    # Iterate through each column in the slot machine
    for col in range(SLOT_COLS):
        # Check if reel in current column is spinning
        if spinning_reels[col]:
            # Iterate through each row in the reel column
            for row in range(SLOT_ROWS):
                # Calculate and store the index of the symbol to be displayed in the box
                # Using modulo to create a circluar reel affect and ensure it doesn't go out of bounds
                symbol_index = (symbol_indexes[col] - row) % len(SYMBOLS)
                # Initialise symbol variable with symbol from slot_symbols list using col and index
                symbol = slot_symbols[col][symbol_index]
                # Assign symbol variable to the current box
                boxes[row][col] = symbol
            # Update the symbol index for the next spin, modulo ensure it doesn't go out of bounds
            symbol_indexes[col] = (symbol_indexes[col] + 1) % len(SYMBOLS)

# Function to check for 3, 4 or 5 in a row horizontal          
def check_rows():
    global win_line, symbol_value
    # Iterate over each row in box list
    for row in boxes:
        # Checking for 3 symbols in a row match
        for i in range(len(row) - 2):
            if row[i] == row[i+1] == row[i+2]:
                win_line = 3
                symbol_value = SYMBOL_VALUES[row[i]]
                return True, win_line, symbol_value
        # Checking for 4 symbols in a row match
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3]:
                win_line = 4
                symbol_value = SYMBOL_VALUES[row[i]]
                return True, win_line, symbol_value
        # Checking for 4 symbols in a row match
        for i in range(len(row) - 4):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == row[i+4]:
                win_line = 5
                symbol_value = SYMBOL_VALUES[row[i]]
                return True, win_line, symbol_value
    # If no winning combination found
    return False, None, None

# Function to press toggle spin key for clicking responsiveness (Ungraceful)
def toggle_spin_key():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))
    return

# Function to stop individual reels from spinning
def toggle_spin():
    global spinning, stop_reel, current_delay, game_state, autoplay_interval
    # Check if reels currently spinning
    if spinning:
        # Check if stopped reel index is less than the amount of spinning reels
        if stop_reel < len(spinning_reels):
            # Stop the reel at the current index
            spinning_reels[stop_reel] = False
            # Increment the stopped reel index by 1
            stop_reel += 1
            # Increase the current delay to slow down reels each time prev stopped
            current_delay += delay_increment
            # Increase the autoplay interval
            autoplay_interval += 350
        # Check if all reels have stopped spinning
        if all(not spinning for spinning in spinning_reels):
            # Set spinning boolean to False, logging the machine isn't spinning
            spinning = False
            # Reset delay
            current_delay = 0
            # Update game state
            game_state = "SPIN_OVER"
    else:
        # If the reels aren't currently spinning, start spinning
        spinning = True
        # Reset the stopped reel index
        stop_reel = 0
        # Start all reels spinning
        for i in range(len(spinning_reels)):
            spinning_reels[i] = True

# Funciton to toggle how to play page boolean
def how_to_toggle():
    global how_to, paused
    if how_to == True:
        paused = True
        how_to = False
    else:
        how_to = True

# Function to call home menu
def call_home():
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)
    
    # Get the parent directory of the current script
    slot_machine_dir = os.path.dirname(current_script_path)
    
    # Get the parent directory of the blackjack_dir
    parent_dir = os.path.dirname(slot_machine_dir)
    
    # Construct the path to home.py in the parent directory
    home_script_path = os.path.join(parent_dir, "main.py")
    
    # Ensure working directory is reset to prevent issues with games launching from main.py
    os.chdir(parent_dir)

    # Start a new subprocess to run the home.py script
    subprocess.Popen([sys.executable, home_script_path])

    # Quit the current game
    quit_game()
    

# Function to update screen based on game state
def update_screen():
    global spinning, win, winnings, win_line
    # Display savannah background all the time
    screen.blit(background, (0, 0))
    # Overlay partially transparent grid
    screen.blit(grid, (grid_x, grid_y))
    # Check if spinning, call spin_reels() function
    if spinning:
        spin_reels()
        # Slow down reel spin by defined amount
        pygame.time.wait(current_delay)
    # Iterate through boxes and display symbol inside each box
    for row in range(SLOT_ROWS):
        for col in range(SLOT_COLS):
            box_x = col * BOX_WIDTH + grid_x
            box_y = row * BOX_HEIGHT + grid_y
            symbol = boxes[row][col]
            if symbol is not None:
                screen.blit(symbol, (box_x + 4, box_y))
    
    # Constantly show current balance and current bet
    text = "Balance:" + str(balance)
    draw_text(text, BLACK, 1100, 30)
    text = "Current Bet:" + str(player_bet)
    draw_text(text, BLACK, 120, 30)
    
    # Check if reels are spinning, if they are, show Stop Reel button
    if spinning:
        draw_button("Stop Reel(Space)", WHITE, pygame.Rect((SCREEN_WIDTH - 150) // 2, 800, 210, 50), toggle_autoplay)
    # Check if reels are not spinning and that game_state is correct, show spin button
    if not spinning and not autoplay_mode and game_state != "SPIN_OVER":
        draw_button("Spin(Space)", WHITE, pygame.Rect((SCREEN_WIDTH - 150) // 2, 800, 150, 50), toggle_autoplay)
    
    # Draw rebet and new bet buttons if game state is "SPIN_OVER"
    if game_state == "SPIN_OVER":
        draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(((SCREEN_WIDTH - 150) // 2) - 125, 800, 140, 50), play_again)
        draw_button("New Bet(N)", WHITE, pygame.Rect(((SCREEN_WIDTH - 150) // 2) + 125, 800, 140, 50), new_bet)
    # Display win message at the top if player win detected
    if win and game_state == "SPIN_OVER":
        text = "You won: " + str(winnings) +"!"
        draw_more_text(text, BLACK, (SCREEN_WIDTH // 2) - 130, 30, font_size=36, bold=True)
    # Draw pause menu if paused boolean True
    if paused:
        screen.blit(background, (0, 0))
        title = "Paused"
        draw_more_text(title, BLACK, ((SCREEN_WIDTH - 110) // 2), 50, font_size=36, bold=True)
        draw_button("Resume", WHITE, pygame.Rect(((SCREEN_WIDTH - 93) // 2), 113, 93, 45),toggle_pause)
        draw_button("Change Game", WHITE, pygame.Rect(((SCREEN_WIDTH - 150) // 2), 212, 150, 45),call_home)
        draw_button("How to Play", WHITE, pygame.Rect(((SCREEN_WIDTH - 150) // 2), 313, 150, 45),how_to_toggle)
        draw_button("Quit Game", WHITE, pygame.Rect(((SCREEN_WIDTH - 125) // 2), 413, 125, 45),quit_game)
    # Draw how to play page is how_to boolean True
    if how_to:
        screen.blit(background, (0, 0))
        title = "How to play Slot Machine"
        draw_more_text(title, BLACK, 400, 35, font_size=30, bold=True)
        
        text = "Aim:"
        draw_more_text(text, BLACK, 360, 85, font_size=18, bold=True)
        text = "Match symbols across the reels to win prizes."
        draw_more_text(text, BLACK, 390, 105, font_size=18)

        text = "Gameplay:"
        draw_more_text(text, BLACK, 360, 160, font_size=18, bold=True)
        text = "Place your bet and spin the reels."
        draw_more_text(text, BLACK, 390, 180, font_size=18)
        text = "The reels will stop randomly, but you can also stop them manually."
        draw_more_text(text, BLACK, 390, 200, font_size=18)
        text = "Win by matching symbols in horizontal patterns of 3, 4, or 5."
        draw_more_text(text, BLACK, 390, 220, font_size=18)
        
        text = "Winning:"
        draw_more_text(text, BLACK, 360, 270, font_size=18, bold=True)
        text = "Win amounts based on your bet and symbol combinations."
        draw_more_text(text, BLACK, 390, 290, font_size=18)
        text = "The least valuable to most valuable symbols are:"
        draw_more_text(text, BLACK, 390, 310, font_size=18)
        
        text = "1. Lion  2. Turtle"
        draw_more_text(text, BLACK, 390, 330, font_size=18)
        text = "3. Tiger  4. Flamingo"
        draw_more_text(text, BLACK, 390, 350, font_size=18)
        text = "5. Zebra  6. Paws"
        draw_more_text(text, BLACK, 390, 370, font_size=18)
        text = "7. Tree  8. Giraffe"
        draw_more_text(text, BLACK, 390, 390, font_size=18)
        text = "9. Boar  10. Elephant"
        draw_more_text(text, BLACK, 390, 410, font_size=18)
        
        draw_button("Back", WHITE, pygame.Rect(SCREEN_WIDTH // 2, 475, 70, 50), how_to_toggle)
    pygame.display.flip()

# Main Game Loop
def main():
    global autoplay_mode, game_state, win, winnings, balance, current_player, paused, autoplay_interval
    start_game()
    spin_reels()
    winnings_saved = False
     # Initialize Pygame clock
    clock = pygame.time.Clock() 
     # Set the autoplay reel stopping interval
    autoplay_interval = random.randint(750,1500) 
    # Initialise autoplay timer
    autoplay_timer = 0

    #Pygame loop
    while True:
        for event in pygame.event.get():
            # Check if game as been quit and gracefully exit the program with quit_game() function
            if event.type == pygame.QUIT:
                quit_game()
            # Listen for keys being pressed
            elif event.type == pygame.KEYDOWN:
                # Toggle pause menu if 'Escape' is detected as being pressed
                if event.key == pygame.K_ESCAPE:
                    toggle_pause()
                # Check if space bar has been pressed
                if event.key == pygame.K_SPACE:
                    # Check if reels are not stopped after a spin and game not paused
                    if game_state != "SPIN_OVER" and not paused:
                        # Spin the reels
                        toggle_autoplay()
                        # Check if any reels are spinning
                        if any(spinning_reels):
                            # Toggle reel spin
                            toggle_spin()
                elif event.key == pygame.K_r:
                    if game_state == "SPIN_OVER" and not paused:
                        play_again()
                elif event.key == pygame.K_n:
                    if game_state == "SPIN_OVER" and not paused:
                        new_bet()

        # If autoplay mode is enabled and no reels are spinning, trigger reel spin based on interval
        if autoplay_mode and any(spinning_reels):
            # Update autoplay timer
            autoplay_timer += clock.get_rawtime()  
            # Check if timer is greater than interval and stop reel spinning
            if autoplay_timer >= autoplay_interval:
                toggle_spin()
                # Reset autoplay timer after triggering reel spin
                autoplay_timer = 0  
        # Check that all reels have stopped spinning
        if not any(spinning_reels):
            # Check for a winning combination of 3,4 or 5
            win = check_rows()
            # Extract boolean from check_rows() returned tuple
            win = win[0]
            # If win determined, pay out winning credits accordingly
            if win:
                if not winnings_saved:
                    winnings = player_bet + (player_bet * symbol_value)
                    # Change working directory for access/create save_file.txt in game_assets folder
                    os.chdir(game_assets)
                    save(current_player, winnings)
                    current_player = load(player_name)
                    balance = get_info(current_player)[1]
                    winnings_saved = True
                    update_screen()

        update_screen()
        # Capped FPS to 30
        clock.tick(30)

if __name__ == "__main__":
    main()


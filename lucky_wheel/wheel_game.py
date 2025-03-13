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
card_deck_script_path = os.path.join(game_assets, "card_deck.py")
font_path = os.path.join(game_assets, "gnu.ttf")

# Ensure the player module is saving to root game folder
sys.path.append(game_assets)

# Import modules from game_assets folder
from player import load, save, get_info

# Initialise Pygame
pygame.init()

# Initialise Screen Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Lucky Wheel")

# Initialise Colour Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (28, 21, 105)

# Initialise Font Variable
font = pygame.font.Font(font_path, 24)

# Initialise Game Variables
game_state = ''
player_name = ""
player_bet = 0
current_player = None
paused = False
how_to = False
multiplier = 0
valid_rebet = None
span = False
winnings = 0
numbers = {0: 3, 36: 0, 72: 10, 108: 0, 144: 2, 180: 0, 216: 0.5, 252: 0, 288: 2, 324: 0}

os.chdir(game_dir)

#  Initialise wheel image variable with try/except in case game is ran standalone
try:
    wheel = pygame.image.load('lucky_wheel/graphics/wheel.png')
except:
    wheel = pygame.image.load('graphics/wheel.png')

# Initialise wheel rectangle variables
wheel_rect = wheel.get_rect()

#  Initialise background image variable with try/except in case game is ran standalone
try:
    game_background = pygame.image.load("lucky_wheel/graphics/lucky_wheel_background.png").convert()
except:
    game_background = pygame.image.load("graphics/lucky_wheel_background.png").convert()

# Transform Background Image to fit game screen resolution
game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  Initialise pause background image variable with try/except in case game is ran standalone
try:
    pause_menu_background = pygame.image.load("lucky_wheel/graphics/lw_pause_background.png").convert()
except:
    pause_menu_background = pygame.image.load("graphics/lw_pause_background.png").convert()

# Transform Background Image to fit game screen resolution
pause_menu_background = pygame.transform.scale(pause_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  Initialise pause background image variable with try/except in case game is ran standalone
try:
    menu_background = pygame.image.load("lucky_wheel/graphics/lw_background.png").convert()
except:
    menu_background = pygame.image.load("graphics/lw_background.png").convert()

# Transform Background Image to fit game screen resolution
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

# Function to toggle pause menu
def toggle_pause():
    global paused
    if paused == True:
        paused = False  # Resume the game
    else:
        paused = True   # Pause the game

# Funciton to toggle how to play page
def how_to_toggle():
    global how_to, paused
    if how_to == True:
        paused = True
        how_to = False
    else:
        how_to = True

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

# Function to call home menu
def call_home():
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)
    
    # Get the parent directory of the current script
    wheel_dir = os.path.dirname(current_script_path)
    
    # Get the parent directory
    parent_dir = os.path.dirname(wheel_dir)
    
    # Construct the path to home.py in the parent directory
    home_script_path = os.path.join(parent_dir, "main.py")

    # Ensure working directory is reset to prevent issues with games launching from main.py
    os.chdir(parent_dir)

    # Start a new subprocess to run the home.py script
    subprocess.Popen([sys.executable, home_script_path])
    
    # Quit the current game
    quit_game()

# Function to reset game variables
def reset_round():
    global multiplier, game_state, valid_rebet, span
    multiplier = 0
    game_state = 'ROUND_ACTIVE'
    valid_rebet = None
    span = False
    return

# Function to handle name input
def get_name():
    empty_input = None
    invalid_input = None
    # Initialise input box for the player's name
    input_box = pygame.Rect(300, 200, 200, 50)
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
                    # If the key pressed is RETURN, returns the player's name if not invalid
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
        draw_more_text("Enter your name:", WHITE, 300, 150)
        # Draw the input box on the screen
        pygame.draw.rect(screen, WHITE, input_box, 2)
        # Draw the player's name inside the input box as its being entered
        draw_more_text(player_name, WHITE, input_box.x + 5, input_box.y + 5)
        # Draw error messages depending on issue
        if empty_input:
            draw_more_text("You didn't enter anything!", WHITE, 250, 275)
        if invalid_input:
            draw_more_text("You can't have numbers in your name!", WHITE, 200, 275)
        # Update the display
        pygame.display.flip()

# Function to handle bet input
def get_bet(balance):
    # Initialise input box for the player's bet
    input_box = pygame.Rect(300, 200, 200, 50)
    # Initialise empty string to store the bet
    text = ''
    # Set the active flag to True
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
                # If the input box is active
                if active:
                    # If the key pressed is RETURN
                    if event.key == pygame.K_RETURN:
                        try:
                            # Try to convert the text to an integer and assign it to bet
                            bet = int(text)
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
        # Draw the balance on the screen
        if insufficient_balance:
            draw_more_text("Insufficient Balance",WHITE, 280, 275)
        if invalid_bet:
            draw_more_text("Invalid Bet",WHITE, 320, 275)
        draw_more_text("Balance: " + str(balance),WHITE, 300, 100)
        # Draw the text "Place your bet:" on the screen
        draw_more_text("Place your bet:", WHITE, 300, 150)
        # Draw the input box on the screen
        pygame.draw.rect(screen, WHITE, input_box, 2)
        # Draw the text inside the input box
        draw_more_text(text, WHITE, input_box.x + 5, input_box.y + 5)
        # Update the display
        pygame.display.flip()

# Function to start game
def start_game():
    global current_player, player_bet, player_name, balance
    # Reset values
    reset_round()
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

# Function to initiate a new bet with the same player after round ends
def new_bet():
    global player_bet
    player_bet = 0
    play_again()

# Function to update the screen based on game state
def update_screen():
    global game_state, valid_rebet, player_bet, paused, how_to, span, winnings, rotated_wheel, rotated_rect, wheel_x, wheel_y

    # Display game background and static wheel in default position if not paused
    if not span and not paused:
        screen.blit(game_background, (0, 0))
        screen.blit(wheel, (SCREEN_WIDTH // 2 - wheel_rect.width // 2, SCREEN_HEIGHT // 2 - wheel_rect.height // 2))
    
    # Display game background and wheel in last landing position if not paused
    if span and not paused:
        screen.blit(game_background, (0, 0))
        screen.blit(rotated_wheel, (wheel_x, wheel_y))
    # Draw player balance, current bet and Spin button when not paused and round active
    if game_state == "ROUND_ACTIVE" and not paused:
        text = "Balance:" + str(balance)
        draw_text(text,WHITE,700,30)
        text = "Current Bet:" + str(player_bet)
        draw_text(text, WHITE, 120, 30)
        draw_button("Spin(Space)", WHITE, pygame.Rect(328, 530, 150, 50),execute_spin)
    # Draw player balance, current bet and winnings if appropriate
    if game_state == "ROUND_OVER" and not paused:
        text = "Balance:" + str(balance)
        draw_text(text,WHITE,700,30)
        text = "Current Bet:" + str(player_bet)
        draw_text(text, WHITE, 120, 30)
        if winnings > 0:
            text = "You won: " + str(winnings)
            draw_text(text, WHITE, 400, 540)
            if player_bet < 10:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 132, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet >= 10 and player_bet < 100:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 145, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet > 99 and player_bet < 999:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 160, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet > 999:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 170, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)

        elif winnings == 0:
            text = "Better luck next time"
            draw_text(text, WHITE, 400, 540)
            if player_bet < 10:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 125, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet >= 10 and player_bet < 100:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 145, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet > 99 and player_bet < 999:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 160, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
            if player_bet > 999:
                draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(35, 510, 170, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(620, 510, 140, 50), new_bet)
    # Draw pause menu and action buttons if game is paused
    if paused:
        screen.blit(pause_menu_background, (0, 0))
        text = "Paused"
        draw_more_text(text, WHITE, 343, 50, font_size=36, bold=True)
        draw_button("Resume", WHITE, pygame.Rect(353.5, 113, 93, 45),toggle_pause)
        draw_button("Change Game", WHITE, pygame.Rect(325, 212, 150, 45),call_home)
        draw_button("How to Play", WHITE, pygame.Rect(325, 313, 150, 45),how_to_toggle)
        draw_button("Quit Game", WHITE, pygame.Rect(337.5, 413, 125, 45),quit_game)

    # Draw how to play page if how to play button is pressed
    if how_to:
        screen.blit(pause_menu_background, (0, 0))
        text = "How to play Lucky Wheel"
        draw_more_text(text, WHITE, 260, 35, font_size=30, bold=True)
        text = "Aim:"
        draw_more_text(text, WHITE, 160, 85, font_size=18, bold=True)
        text = "Guess where the lucky wheel will stop and place your bet."
        draw_more_text(text, WHITE, 190, 105, font_size=18)

        text = "Gameplay:"
        draw_more_text(text, WHITE, 160, 140, font_size=18, bold=True)
        text = "Place your bet and spin the wheel."
        draw_more_text(text, WHITE, 190, 160, font_size=18)
        text = "The wheel will stop on a random segment, determining the outcome."
        draw_more_text(text, WHITE, 190, 180, font_size=18)
        text = "If the wheel stops on a multiplier, your bet is multiplied and paid."
        draw_more_text(text, WHITE, 190, 200, font_size=18)
        text = "If it lands on 0x, you lose your bet."
        draw_more_text(text, WHITE, 190, 220, font_size=18)

        text = "Winning:"
        draw_more_text(text, WHITE, 160, 255, font_size=18, bold=True)
        text = "Win an amount based on your bet and the multiplier."
        draw_more_text(text, WHITE, 190, 275, font_size=18)
        draw_button("Back", WHITE, pygame.Rect(365, 530, 70, 50), how_to_toggle)
            
    pygame.display.flip()

# Function to execute spin by simulating spacebar press
def execute_spin():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))
    return

# Function to handle spinning wheel animation and obtaining landing multiplier
def spin_wheel():
    global rotated_wheel, rotated_rect, wheel_x, wheel_y
    # Define angle landed/multiplier value
    numbers = {0: 3, 36: 0, 72: 10, 108: 0, 144: 2, 180: 0, 216: 0.5, 252: 0, 288: 2, 324: 0}
    # Initialse starting angle
    angle = 0
    # Initialise rotating boolean
    rotating = True
    # Initialise random spin speed variable
    speed = random.randint(random.randint(5,10),random.randint(11,20))
    """Assisted by ChatGPT 3.5 - START"""
    # While rotation is happening, slowely reduce the speed to 0 before stopping
    while rotating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        speed -= 0.02
        if speed <= 0:
            speed = 0
            rotating = False

        angle = (angle + speed) % 360

        screen.blit(game_background, (0, 0))

        rotated_wheel = pygame.transform.rotate(wheel, angle)
        rotated_rect = rotated_wheel.get_rect(center=wheel_rect.center)

        wheel_x = SCREEN_WIDTH // 2 - rotated_rect.width // 2
        wheel_y = SCREEN_HEIGHT // 2 - rotated_rect.height // 2
        screen.blit(rotated_wheel, (wheel_x, wheel_y))
        """Assisted with ChatGPT 3.5 - END"""

        text = "Balance:" + str(balance)
        draw_text(text,WHITE,700,30)
        text = "Current Bet:" + str(player_bet)
        draw_text(text, WHITE, 120, 30)

        pygame.display.flip()

    """Assisted by ChatGPT 3.5 - START"""
    # Generate the closest angle in numbers dictionary
    closest_angle = min(numbers.keys(), key=lambda x: abs(x - angle))
    """Assisted with ChatGPT 3.5 - END"""
    if angle > 342 and angle < 359:
        closest_angle = 0

    return closest_angle

# Main game loop
def main():
    global current_player, game_state, valid_rebet, player_bet, paused, how_to, multiplier, span, winnings, balance
    # Initialise or reuse current_player and player_bet variables
    start_game()
    winnings_saved = False

    # Pygame loop
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
                # Listen and responde to 'Spacebar' being pressed and spin wheel if game in correct state
                if event.key == pygame.K_SPACE:
                    if game_state == "ROUND_ACTIVE" and not paused:
                        closest_angle = spin_wheel()
                        multiplier = numbers.get(closest_angle)
                        span = True
                        game_state = "ROUND_OVER"
                # Listen and respond to 'N' being pressed and run new_bet() if game in correct state
                elif event.key == pygame.K_n:
                    if game_state != "ROUND_ACTIVE" and not paused:
                        new_bet()
                # Listen and respond to 'R' being pressed and run play_again() if game in correct state
                elif event.key == pygame.K_r:
                    if game_state != "ROUND_ACTIVE" and not paused:
                        valid_rebet = play_again()
                        if valid_rebet:
                            play_again()
                        else:
                            pass
        # When round is over, save winnings if appropriate
        if game_state == 'ROUND_OVER':
            if not winnings_saved:
                if multiplier == 0:
                    winnings = 0
                    pass
                else:
                    winnings = player_bet * multiplier
                    # Change working directory for access/create save_file.txt in game_assets folder
                    os.chdir(game_assets)
                    save(current_player, winnings)
                    current_player = load(player_name)
                    balance = get_info(current_player)[1]
                    winnings_saved = True
                    update_screen()
        
        update_screen()

if __name__ == "__main__":
    main()
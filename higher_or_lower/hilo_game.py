# Import necessary libraries and modules
import pygame
import os
import sys
import subprocess

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


# Now you can import functions from player.py
from player import load, save, get_info
from card_deck import create, shuffle, deal, value

# Initialise Pygame
pygame.init()

# Screen Dimension Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Higher or Lower")

# Define Colours    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (9, 31, 90)

# Define font
font = pygame.font.Font(font_path, 24)

# Initialse Game Variables
game_state = ''
player_name = ""
player_bet = 0
current_player = None
paused = False
how_to = False
winnings_pot = 0
bet_multiplier = 0
card_history = []
valid_rebet = None

#  Initialise background image variable with try/except in case game is ran standalone
try:
    background_image = pygame.image.load("higher_or_lower/graphics/Hilo_Background.png").convert()
except:
    background_image = pygame.image.load("graphics/Hilo_Background.png").convert()

# Transform Background Image to fit game screen resolution
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  Initialise pause background image variable with try/except in case game is ran standalone
try:
    pause_background_image = pygame.image.load("higher_or_lower/graphics/Pause_Background.png").convert()
except:
    pause_background_image = pygame.image.load("graphics/Pause_Background.png").convert()

#  Initialise pause background image variable with try/except in case game is ran standalone    
pause_background_image = pygame.transform.scale(pause_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

# Function to draw text on buttons properly
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

# Function to draw text with more customisation
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

# Function to draw big card on screen
def draw_card(hand, x, y):
    # Dictionary for card suit symbols
    suit_symbols = {'hearts': (str(chr(9829))), 'diamonds': (str(chr(9830))), 'spades': (str(chr(9824))), 'clubs': (str(chr(9827)))}

    # Card dimensions and padding
    card_width, card_height = 160, 200
    padding = 30
    index = 0

    # Loop through cards in the hand
    for card in hand:
        # Create a surface for the card
        card_surface = pygame.Surface((card_width, card_height))
        card_surface.fill((WHITE))
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height), 2)

        # Get face and suit of the card
        face = card.get('face')
        suit = card.get('suit')

        # Render face and suit symbols on the card
        face_text = font.render(face, True, BLACK)
        suit_text = font.render(suit_symbols[suit], True, BLACK)

        # Calculate positions to center text within the card
        face_x = (card_width - face_text.get_width()) // 2
        face_y = (card_height - face_text.get_height() - suit_text.get_height() - padding) // 2
        suit_x = (card_width - suit_text.get_width()) // 2
        suit_y = face_y + face_text.get_height() + padding

        # Blit text onto the card surface
        card_surface.blit(face_text, (face_x, face_y))
        card_surface.blit(suit_text, (suit_x, suit_y))

        # Blit card surface onto the screen
        screen.blit(card_surface, (x + index * (card_width + padding), y))
        index += 1

# Function to draw card history on screen
def draw_history(hand, x, y):
    # Dictionary for card suit symbols
    suit_symbols = {'hearts': (str(chr(9829))), 'diamonds': (str(chr(9830))), 'spades': (str(chr(9824))), 'clubs': (str(chr(9827)))}

    # Card dimensions and padding
    card_width, card_height = 80, 120
    padding = 15
    index = 0

    # Loop through cards in the hand
    for card in hand:
        # Create a surface for the card
        card_surface = pygame.Surface((card_width, card_height))
        card_surface.fill((WHITE))
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height), 2)

        # Get face and suit of the card
        face = card.get('face')
        suit = card.get('suit')

        # Render face and suit symbols on the card
        face_text = font.render(face, True, BLACK)
        suit_text = font.render(suit_symbols[suit], True, BLACK)

        # Calculate positions to center text within the card
        face_x = (card_width - face_text.get_width()) // 2
        face_y = (card_height - face_text.get_height() - suit_text.get_height() - padding) // 2
        suit_x = (card_width - suit_text.get_width()) // 2
        suit_y = face_y + face_text.get_height() + padding

        # Blit text onto the card surface
        card_surface.blit(face_text, (face_x, face_y))
        card_surface.blit(suit_text, (suit_x, suit_y))

        # Blit card surface onto the screen
        screen.blit(card_surface, (x + index * (card_width + padding), y))
        index += 1

# Function to toggle pause menu boolean
def toggle_pause():
    global paused
    if paused == True:
        paused = False  # Resume the game
    else:
        paused = True   # Pause the game

# Function to update the screen based on game state
def update_screen(card, card_history, winnings_pot):
    global game_state, bet_multiplier, valid_rebet, player_bet, paused, how_to
    # Fill screen with blue color if game is not paused
    if not paused and not how_to:
        screen.fill(BLUE)
    # Draw game elements if game isn't paused
    if not paused:
        # Draw game elements of round in progress
        if game_state == 'ROUND_ACTIVE':
            x = (SCREEN_WIDTH - 160) // 2
            # Draw big card on screen
            draw_card(card,x,50)
            # Draw action buttons
            draw_button("Higher or Same(H)", WHITE, pygame.Rect(87, 325, 220, 50), execute_higher)
            draw_button("Cashout(C)", WHITE, pygame.Rect(335, 325, 135, 50), cashout)
            draw_button("Lower or Same(L)", WHITE, pygame.Rect(496, 325, 205, 50), execute_lower)
            # Draw card history heading and cards
            x = SCREEN_WIDTH // 2
            text = "History"
            draw_text(text, WHITE, x, 425)
            draw_history(card_history, 30, 450)
            # Draw player credit balance in top right
            text = "Balance:" + str(balance)
            draw_text(text,WHITE,700,30)
            # Draw current round winnings center
            x = SCREEN_WIDTH // 2
            text = "Winnings Pot: " + str(winnings_pot)
            draw_text(text,WHITE,x,280)
            # Draw current round multiplier in top left
            text = "Multiplier: " + str(bet_multiplier) +'x'
            draw_text(text, WHITE, 130, 30)
        # Draw game elements of round that has ended
        elif game_state == 'ROUND_OVER':
            x = (SCREEN_WIDTH - 160) // 2
            # Draw the most recent card drawn
            draw_card(card,x,50)
            # Draw action buttons based on bet amount to ensure button background is wider if needed
            if player_bet < 10:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(240, 325, 132, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet < 100 and player_bet > 9:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(227, 325, 145, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet > 99 and player_bet < 999:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(212, 325, 160, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet > 999 and player_bet < 9999:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(200, 325, 172, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            x = SCREEN_WIDTH // 2
            # Draw card history heading and cards
            text = "History"
            draw_text(text, WHITE, x, 425)
            draw_history(card_history, 30, 450)
            # Draw current player balance in top right
            text = "Balance:" + str(balance)
            draw_text(text,WHITE,700,30)
            # Give error message is player tries to re-bet and doesn't have enough credits
            if valid_rebet == False:
                x = SCREEN_WIDTH // 2
                text = "Insufficient Balance"
                draw_text(text,WHITE,x,280)
            else:
            # Give game over message by default
                x = SCREEN_WIDTH // 2
                text = "Game Over"
                draw_text(text,WHITE,x,280)
        # Draw game elements if player cashes out
        elif game_state == 'CASH_OUT':
            x = (SCREEN_WIDTH - 160) // 2
            # Draw most recent big card
            draw_card(card,x,50)
            # Draw action buttons based on bet amount to ensure button background is wider if needed
            if player_bet < 10:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(240, 325, 132, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet < 100 and player_bet > 9:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(227, 325, 145, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet > 99 and player_bet < 999:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(212, 325, 160, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            if player_bet > 999 and player_bet < 9999:
                draw_button("Rebet:" + str(player_bet) +"(R)", WHITE, pygame.Rect(200, 325, 172, 50), play_again)
                draw_button("New Bet(N)", WHITE, pygame.Rect(430, 325, 132, 50), new_bet)
            # Draw card history heading and cards            
            x = SCREEN_WIDTH // 2
            text = "History"
            draw_text(text, WHITE, x, 425)
            draw_history(card_history, 30, 450)
            # Draw current player balance in top right
            text = "Balance:" + str(balance)
            draw_text(text,WHITE,700,30)
            # Give error message is player tries to re-bet and doesn't have enough credits
            if valid_rebet == False:
                x = SCREEN_WIDTH // 2
                text = "Insufficient Balance"
                draw_text(text,WHITE,x,280)
            else:
            # Draw message informing of total amount of credits gained
                x = SCREEN_WIDTH // 2
                text = "You cashed out: "+str(int(winnings_pot))
                draw_text(text,WHITE,x,280)
    # Draw pause menu and action buttons if game is paused
    if paused:
        screen.blit(pause_background_image, (0, 0))
        text = "Paused"
        draw_more_text(text, WHITE, 343, 50, font_size=36, bold=True)
        draw_button("Resume", WHITE, pygame.Rect(353.5, 113, 93, 45),toggle_pause)
        draw_button("Change Game", WHITE, pygame.Rect(325, 212, 150, 45),call_home)
        draw_button("How to Play", WHITE, pygame.Rect(325, 313, 150, 45),how_to_toggle)
        draw_button("Quit Game", WHITE, pygame.Rect(337.5, 413, 125, 45),quit_game)
    # Draw how to play page if how to play button is pressed
    if how_to:
        screen.blit(pause_background_image, (0, 0))
        text = "How to play Higher or Lower"
        draw_more_text(text, WHITE, 260, 35, font_size=30, bold=True)
        text = "Aim:"
        draw_more_text(text, WHITE, 160, 85, font_size=18, bold=True)
        text = "Guess if the next card is higher or lower than the previous."
        draw_more_text(text, WHITE, 190, 105, font_size=18)
        text = "Card Values:"
        draw_more_text(text, WHITE, 160, 140, font_size=18, bold=True)
        text = "Ace has the lowest value, face cards have their own value."
        draw_more_text(text, WHITE, 190, 160, font_size=18)
        text = "Jack has a lower value than Queen, Queen has a lower value King."
        draw_more_text(text, WHITE, 190, 180, font_size=18)

        text = "Gameplay:"
        draw_more_text(text, WHITE, 160, 215, font_size=18, bold=True)
        text = "Predict if the next card will be higher or lower in value."
        draw_more_text(text, WHITE, 190, 235, font_size=18)
        text = "If your prediction is correct, your winnings are multiplied by 25%."
        draw_more_text(text, WHITE, 190, 255, font_size=18)
        text = "For each correct guess, the multiplier increases by 25%."
        draw_more_text(text, WHITE, 190, 275, font_size=18)
        text = "If the next card is the same value as the current card, you win."
        draw_more_text(text, WHITE, 190, 295, font_size=18)
        text = "If your prediction is incorrect, the round ends and bet is lost."
        draw_more_text(text, WHITE, 190, 315, font_size=18)

        text = "Winning:"
        draw_more_text(text, WHITE, 160, 350, font_size=18, bold=True)
        text = "Continue playing rounds until you decide to cash out or lose."
        draw_more_text(text, WHITE, 190, 370, font_size=18)
        draw_button("Back", WHITE, pygame.Rect(365, 530, 70, 50), how_to_toggle)
    
    # Update game display each time function is called
    pygame.display.flip()

# Function to toggle how to page boolean
def how_to_toggle():
    global how_to, paused
    if how_to == True:
        paused = True
        how_to = False
    else:
        how_to = True

# Function to quit the game gracefully
def quit_game():
    pygame.quit()
    sys.exit()

# Function to call home menu
def call_home():
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)
    
    # Get the parent directory of the current script
    hilo_dir = os.path.dirname(current_script_path)
    
    # Get the parent directory of the blackjack_dir
    parent_dir = os.path.dirname(hilo_dir)
    
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
    global card_history, bet_multiplier, winnings_pot, game_state, valid_rebet
    card_history = []
    bet_multiplier = 1.25
    winnings_pot = 0
    game_state = 'ROUND_ACTIVE'
    valid_rebet = None
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
        screen.blit(background_image, (0, 0))
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
        screen.blit(background_image, (0, 0))
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

# Function to set up the game
def start_round():
    global bet_multiplier
    # Set up the starting bet multiplier
    bet_multiplier = 1.25
    # Create the card deck
    deck = create()
    for i in range(52):
        deck.append(deal(deck))
    # Shuffle the card deck
    shuffle(deck)
    # Initialise game hand
    game_hand = []
    # Issue 2 cards from card deck
    for i in range(2):
        game_hand.append(deal(deck))
    # Initialise current card
    card = []
    card.append(game_hand[0])
    # Set game state
    game_state = "ROUND_ACTIVE"
    return deck, game_hand, card, game_state

# Function to compare cards
def compare_cards(game_hand):
    # Temporary hands used to ensure compatibility with card_deck value() function
    temp_hand_1 = []
    temp_hand_1.append(game_hand[0])

    temp_hand_2 = []
    temp_hand_2.append(game_hand[1])
    # Obtain values of current card and next card
    temp_hand_1_value = value(temp_hand_1)
    temp_hand_2_value = value(temp_hand_2)
    # Adjust value of hand if J,Q,K present to make cards work more/less
    for card in temp_hand_1:
        face = card.get('face')
        if face == 'J':
            temp_hand_1_value += 1
        if face == 'Q':
            temp_hand_1_value += 2
        if face == 'K':
            temp_hand_1_value += 3

    for card in temp_hand_2:
        face = card.get('face')
        if face == 'J':
            temp_hand_2_value += 1
        if face == 'Q':
            temp_hand_2_value += 2
        if face == 'K':
            temp_hand_2_value += 3
    # Obtain the correct state before the player knows so player input can be compared to this
    if temp_hand_1_value > temp_hand_2_value:
        return 'lower'
    elif temp_hand_1_value == temp_hand_2_value:
        return 'same'
    else:
        return 'higher'

# Function to start game
def start_game():
    global current_player, player_bet, player_name, balance
    # Resets hands and values
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

# Function to carry out user selection of guessing if next card will be higher
def is_higher(deck, game_hand):
    global card_history, player_bet, bet_multiplier, winnings_pot, game_state
    # Obtain result of next card (higher/lower/same)
    result = compare_cards(game_hand)
    # Log which option user has selected
    user_sel = 'higher'
    # Compare user selection to the result, if correct, carry out winning actions
    if user_sel == result or result == 'same':
        # Increase winnings by current round multiplier
        winnings = player_bet * bet_multiplier
        # Add winnings to game winnings pot
        winnings_pot += winnings
        # Add previous card to game history
        card_history.append(game_hand[0])
        # Remove the oldest card in history so only 8 cards show on screen
        if len(card_history) > 8:
            card_history.pop(0)
        # Store previous card
        prev_card = []
        prev_card.append(game_hand[1])
        # Incrementally increase bet multiplier
        bet_multiplier += 0.25
        # Clear the game hand, add the previous card back and get a new card from shuffled deck
        game_hand.clear()
        game_hand.append(prev_card[0])
        game_hand.append(deal(deck))
        card = []
        card.append(game_hand[0])
        return card
    else:
        # If the player guess was wrong, update the history still but end the game
        card_history.append(game_hand[0])
        if len(card_history) > 8:
            card_history.pop(0)
        prev_card = []
        prev_card.append(game_hand[1])
        card = prev_card
        game_state = 'ROUND_OVER'
        return card

# Function to carry out is lower
def is_lower(deck, game_hand):
    global card_history, player_bet, bet_multiplier, winnings_pot, game_state, bet_multiplier
    # Obtain result of next card (higher/lower/same)
    result = compare_cards(game_hand)
    user_sel = 'lower'
    # Compare user selection to the result, if correct, carry out winning actions
    if user_sel == result or result == 'same':
        # Increase winnings by current round multiplier
        winnings = player_bet * bet_multiplier
        # Add winnings to game winnings pot
        winnings_pot += winnings
        # Add previous card to game history
        card_history.append(game_hand[0])
        # Remove the oldest card in history so only 8 cards show on screen
        if len(card_history) > 8:
            card_history.pop(0)
        # Store previous card
        prev_card = []
        prev_card.append(game_hand[1])
        # Incrementally increase bet multiplier
        bet_multiplier += 0.25
        # Clear the game hand, add the previous card back and get a new card from shuffled deck
        game_hand.clear()
        game_hand.append(prev_card[0])
        game_hand.append(deal(deck))
        card = []
        card.append(game_hand[0])
        return card
    else:
        # If the player guess was wrong, update the history still but end the game
        card_history.append(game_hand[0])
        if len(card_history) > 8:
            card_history.pop(0)
        prev_card = []
        prev_card.append(game_hand[1])
        card = prev_card
        game_state = 'ROUND_OVER'
        return card

# Function to execute is_higher when button pressed
def execute_higher():
    # Ungraceful solution to button unresponsivesness. Struggled to debug
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_h}))
    return

# Function to execute is_lower when button pressed
def execute_lower():
    # Ungraceful solution to button unresponsivesness. Struggled to debug
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_l}))
    return

# Function to allow player to make a new bet
def new_bet():
    global player_bet
    player_bet = 0
    play_again()

# Function to cash out winnings
def cashout():
    global current_player, winnings_pot, game_state, player_name, balance
    # Change working directory for access/create save_file.txt in game_assets folder
    os.chdir(game_assets)
    save(current_player, int(winnings_pot))
    load(player_name)
    balance = int(get_info(current_player)[1])
    game_state = 'CASH_OUT'
    return

# Function to toggle pause menu boolean
def toggle_pause():
    global paused
    if paused == True:
        paused = False  # Resume the game
    else:
        paused = True   # Pause the game

# Main Game Loop
def main():
    global current_player, player_bet, player_name, balance, card_history, game_state, valid_rebet, paused
    # Initialise or reuse current_player and player_bet variables
    start_game()
    # Initialise deck, game hand, card and game state
    deck, game_hand, card, game_state = start_round()

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
                # Listen and respond to 'H' being pressed and run is_higher() if game in correct state
                elif event.key == pygame.K_h:
                    if game_state == 'ROUND_ACTIVE' and not paused:
                        card = is_higher(deck, game_hand)
                elif event.key == pygame.K_l:
                # Listen and respond to 'L' being pressed and run is_lower() if game in correct state
                    if game_state == 'ROUND_ACTIVE' and not paused:
                        card = is_lower(deck, game_hand)
                elif event.key == pygame.K_c:
                # Listen and respond to 'C' being pressed and run cashout() if game in correct state
                    if game_state == 'ROUND_ACTIVE' and not paused:
                        cashout()
                # Listen and respond to 'R' being pressed and run play_again() if game in correct state
                elif event.key == pygame.K_r:
                    if game_state != 'ROUND_ACTIVE' and not paused:
                        valid_rebet = play_again()
                        if valid_rebet:
                            play_again()
                        else:
                            pass
                # Listen and respond to 'N' being pressed and run new_bet() if game in correct state
                elif event.key == pygame.K_n and not paused:
                    new_bet()
        # Update screen each loop iteration
        update_screen(card, card_history, winnings_pot)

if __name__ == "__main__":
    main()

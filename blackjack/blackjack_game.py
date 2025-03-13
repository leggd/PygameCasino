import pygame
import os
import sys
import subprocess
import time

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

# Ensure program is getting game assets from right location
sys.path.append(game_assets)

# Import modules from game_assets folder
from player import load, save, get_info
from card_deck import create, shuffle, deal, value


# Initialise Pygame
pygame.init()

# Initialise Screen Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Initialise Colour Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (9, 31, 90)

# Initialise Font Variable
font = pygame.font.Font(font_path, 24)

# Initialise Game Variables
is_dealer = False
game_state = ''
player_name = ""
player_bet = 0
current_player = None
paused = False
how_to = False
valid_rebet = False

#  Initialise background image variable with try/except in case game is ran standalone
try:
    background_image = pygame.image.load("blackjack/graphics/Blackjack_Background.png").convert()
except:
    background_image = pygame.image.load("graphics/Blackjack_Background.png").convert()

# Transform Background Image to fit game screen resolution
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))     

#  Initialise pause background image variable with try/except in case game is ran standalone
try:
    pause_background_image = pygame.image.load("blackjack/graphics/Pause_Background.png").convert()
except:
    pause_background_image = pygame.image.load("graphics/Pause_Background.png").convert()

# Transform Background Image to fit game screen resolution
pause_background_image = pygame.transform.scale(pause_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))     

# Function to generate text standard
def draw_text(text, color, x, y):
    # Render text argument
    text_surface = font.render(text, True, color)
    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()
    # Set the position of the text
    text_rect.topleft = (x, y)
    # Blit the text surface
    screen.blit(text_surface, text_rect)

# Function to draw text with more customisation
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
    # Draw text on button using draw_text()
    draw_text(text, BLACK, rect.x + 10, rect.y + 10)
    # Get mouse position
    mouse = pygame.mouse.get_pos()
    # Check if mouse is hovering over button
    if rect.x + rect.width > mouse[0] > rect.x and rect.y + rect.height > mouse[1] > rect.y:
        # Highlight button if mouse is over it
        pygame.draw.rect(screen, WHITE, rect)
        # Check for mouse click on button
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Execute action argument
                action()
                time.sleep(0.1)

# Function to generate the cards to be drawn
def draw_cards(hand, x, y, game_state, is_dealer=False):
    # Dictionary for card suit symbols
    suit_symbols = {'hearts': (str(chr(9829))), 'diamonds': (str(chr(9830))), 'spades': (str(chr(9824))), 'clubs': (str(chr(9827)))}

    # Card dimensions and padding, initialise index variable to track card
    card_width, card_height = 80, 120
    padding = 20
    index = 0

    # Loop through cards in the hand
    for card in hand:
        # Create a surface for the card
        card_surface = pygame.Surface((card_width, card_height))
        card_surface.fill((WHITE))
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height), 2)

        # Check if blank card should be drawn as 2nd card for dealer, generate and blit if true
        if is_dealer and index == 1 and game_state not in ['DEALER_TURN', 'ROUND_OVER']:
            # Draw a blank card with a question mark
            question_mark = font.render('?', True, BLACK)
            question_mark_x = (card_width - question_mark.get_width()) // 2
            question_mark_y = (card_height - question_mark.get_height()) // 2
            card_surface.blit(question_mark, (question_mark_x, question_mark_y))
        else:
            # Get face and suit of the card
            face = card.get('face')
            suit = card.get('suit')

            # Render face and suit symbols onto the card
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

        # Blit card surface onto the screen, add '1' to index to track card
        screen.blit(card_surface, (x + index * (card_width + padding), y))
        index += 1

# Function to update the screen based on game states
def update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message="", player_bet=0):
    # Fill screen with blue color if game is not paused
    if not paused:
        screen.fill(BLUE)
    # Draw dealer's hand with value displayed if round is over, otherwise just show the cards
    if game_state == 'ROUND_OVER':
        draw_text("Dealer's Hand: " + str(dealer_hand_value), WHITE, 50, 50)
        draw_cards(dealer_hand, 50, 100, game_state, is_dealer)
    else:
        draw_text("Dealer's Hand: ", WHITE, 50, 50)
        draw_cards(dealer_hand, 50, 100, game_state, is_dealer)
    # Constantly display player balance, player hand value and player hand if game is not paused
    if not paused:
        draw_text("Balance: " + str(balance), WHITE, 600, 50)
        # Draw player's hand
        draw_text("Your Hand: " + str(player_hand_value) , WHITE, 50, 250)
        draw_cards(player_hand, 50, 300, game_state)

    # Draw action buttons based on game state and bet amount
    if game_state != 'ROUND_OVER' or game_state == 'DEALER_TURN':
        draw_button("Hit (H)", WHITE, pygame.Rect(300, 500, 100, 50), execute_hit)
        draw_button("Stand (S)", WHITE, pygame.Rect(450, 500, 120, 50), stand_action)
    if game_state == 'ROUND_OVER':
        if player_bet < 100:
            draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(175, 500, 145, 50), play_again)
            draw_button("New Bet(N)", WHITE, pygame.Rect(350, 500, 135, 50), new_bet)
        if player_bet > 99 and player_bet < 999:
            draw_button("Rebet:" + str(player_bet) + "(R)", WHITE, pygame.Rect(175, 500, 160, 50), play_again)
            draw_button("New Bet(N)", WHITE, pygame.Rect(350, 500, 135, 50), new_bet)
        if player_bet > 999:
            draw_button("Rebet:" + str(player_bet)  + "(R)" , WHITE, pygame.Rect(175, 500, 170, 50), play_again)
            draw_button("New Bet(N)", WHITE, pygame.Rect(375, 500, 135, 50), new_bet)

    # Draw pause menu and action buttons if game is paused
    if paused:
        screen.blit(pause_background_image, (0, 0))
        text = "Paused"
        draw_more_text(text, WHITE, 343, 50, font_size=36, bold=True)
        draw_button("Resume", WHITE, pygame.Rect(353.5, 113, 93, 45),toggle_pause)
        draw_button("Change Game", WHITE, pygame.Rect(325, 212, 150, 45),call_home)
        draw_button("How to Play", WHITE, pygame.Rect(325, 313, 150, 45),how_to_toggle)
        draw_button("Quit Game", WHITE, pygame.Rect(337.5, 413, 125, 45),quit_game)

    # Draw current message on screen if game isn't paused and how to page isn't being displayed
    if not paused and not how_to:    
        draw_text(message, WHITE, 50, 435)

    # Draw how to play page if how to play button is pressed
    if how_to:
        screen.blit(pause_background_image, (0, 0))
        text = "How to play Blackjack"
        draw_more_text(text, WHITE, 260, 25, font_size=30, bold=True)
        text = "Aim:"
        draw_more_text(text, WHITE, 160, 75, font_size=18, bold=True)
        text = "The goal is to beat the dealer's hand without going over 21."
        draw_more_text(text, WHITE, 190, 95, font_size=18)
        text = "Card Values:"
        draw_more_text(text, WHITE, 160, 130, font_size=18, bold=True)
        text = "Number cards are face value, face cards are 10,"
        draw_more_text(text, WHITE, 190, 150, font_size=18)
        text = "Aces are 11 if dealt as part of initial hand, otherwise worth 1."
        draw_more_text(text, WHITE, 190, 170, font_size=18)

        text = "Deal:"
        draw_more_text(text, WHITE, 160, 210, font_size=18, bold=True)
        text = "Each player gets 2 cards, dealer 1 up, 1 down."
        draw_more_text(text, WHITE, 190, 230, font_size=18)

        text = "Player's Turn:"
        draw_more_text(text, WHITE, 160, 270, font_size=18, bold=True)
        text = "Hit (take card) or stand (keep hand)."
        draw_more_text(text, WHITE, 190, 290, font_size=18)

        text = "Dealer's Turn:"
        draw_more_text(text, WHITE, 160, 330, font_size=18, bold=True)
        text = "Dealer reveals face-down card, hits until 17 or higher."
        draw_more_text(text, WHITE, 190, 350, font_size=18)

        text = "Winning:"
        draw_more_text(text, WHITE, 160, 390, font_size=18, bold=True)
        text = "Closer to 21 than dealer without going over wins."
        draw_more_text(text, WHITE, 190, 410, font_size=18)
        text = "Going over 21 busts, ties result in a push."
        draw_more_text(text, WHITE, 190, 430, font_size=18)

        text = "Blackjack:"
        draw_more_text(text, WHITE, 160, 470, font_size=18, bold=True)
        text = "Ace and a card worth 10 on first two cards is blackjack, pays 3:2"
        draw_more_text(text, WHITE, 190, 490, font_size=18)
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
    blackjack_dir = os.path.dirname(current_script_path)
    
    # Get the parent directory of the blackjack_dir
    parent_dir = os.path.dirname(blackjack_dir)
    
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
    # Reset all game variables
    card_shoe = []
    player_hand = []
    dealer_hand = []
    player_hand_value = 0
    dealer_hand_value = 0
    return card_shoe, player_hand, dealer_hand, player_hand_value, dealer_hand_value

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
        draw_text("Enter your name:", WHITE, 300, 150)
        # Draw the input box on the screen
        pygame.draw.rect(screen, WHITE, input_box, 2)
        # Draw the player's name inside the input box as its being entered
        draw_text(player_name, WHITE, input_box.x + 5, input_box.y + 5)
        # Draw error messages depending on issue
        if empty_input:
            draw_text("You didn't enter anything!", WHITE, 250, 275)
        if invalid_input:
            draw_text("You can't have numbers in your name!", WHITE, 200, 275)
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
            draw_text("Insufficient Balance",WHITE, 280, 275)
        if invalid_bet:
            draw_text("Invalid Bet",WHITE, 320, 275)
        draw_text("Balance: " + str(balance),WHITE, 300, 100)
        # Draw the text "Place your bet:" on the screen
        draw_text("Place your bet:", WHITE, 300, 150)
        # Draw the input box on the screen
        pygame.draw.rect(screen, WHITE, input_box, 2)
        # Draw the text inside the input box
        draw_text(text, WHITE, input_box.x + 5, input_box.y + 5)
        # Update the display
        pygame.display.flip()
        
# Function to deal the initial hand of cards to dealer/player
def first_hand(card_shoe, player_hand, dealer_hand):
    # Create and shuffle deck
    for i in range(8):
        deck = create()
        for i in range(52):
            card_shoe.append(deal(deck))
    shuffle(card_shoe)

    # Deal two cards each to player and dealer
    for i in range(2):
        dealer_hand.append(deal(card_shoe))
        player_hand.append(deal(card_shoe))
    
    # Calculate initial hand values
    dealer_hand_value = value(dealer_hand)
    player_hand_value = value(player_hand)

    # Check for Aces and adjust hand value if necessary
    dealer_ace = False
    for card in dealer_hand:
        if card.get('face') == 'A':
            dealer_ace = True
    if dealer_ace:
        if dealer_hand_value <= 11:
            dealer_hand_value += 10

    player_ace = False
    for card in player_hand:
        if card.get('face') == 'A':
            player_ace = True
    if player_ace:
        if player_hand_value <= 11:
            player_hand_value += 10
    
    return player_hand_value, dealer_hand_value

# Function to handle player 'hit' action
def hit_action(card_shoe, player_hand, player_hand_value):
    # Deal a new card to the player and calculate value
    temp_hand = []
    new_card = deal(card_shoe)
    temp_hand.append(new_card)
    new_card_value = value(temp_hand)
    player_hand.append(new_card)
    player_hand_value += new_card_value

    return player_hand, player_hand_value

# Function to execute 'hit' action when button clicked
def execute_hit():
    # Ungraceful line to make hit button work better when clicked
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_h}))
    return

# Function to handle player 'stand' action button clicked
def stand_action():
    # Ungraceful line to make stand button work better when clicked
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s}))
    return

# Function to handle dealer turn
def dealer_turn(card_shoe, dealer_hand, dealer_hand_value):    
    # Dealer hits until hand value is at least 17
    while dealer_hand_value < 17:
        temp_hand = []
        new_card = deal(card_shoe)
        temp_hand.append(new_card)
        new_card_value = value(temp_hand)
        dealer_hand.append(new_card)
        dealer_hand_value += new_card_value
    return dealer_hand, dealer_hand_value

# Function to check round winner
def check_winner(player_hand_value, dealer_hand_value):    
    # Determine winner based on hand values
    if player_hand_value > 21 or dealer_hand_value > 21:
        if player_hand_value > 21:
            return 'dealer'
        else:
            return 'player'
    if player_hand_value == dealer_hand_value:
        return 'tie'
    if player_hand_value > dealer_hand_value:
        return 'player'
    else:
        return 'dealer'

# Function to check for Blackjack after hands dealt
def check_blackjack(player_hand_value, dealer_hand_value):   
    # Check if either player or dealer has Blackjack
    if player_hand_value == 21 and dealer_hand_value == 21:
        return 'tie'
    if player_hand_value == 21:
        return 'player'
    if dealer_hand_value == 21:
        return 'dealer'
    return None

# Function to toggle pause menu boolean
def toggle_pause():
    global paused
    if paused == True:
        paused = False  # Resume the game
    else:
        paused = True   # Pause the game

# Function to start the game
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

# Function to play again
def play_again():
    global game_state, is_dealer
    # Check if rebet will exceed player balance
    if player_bet > balance:
        return False
    else:
    # If rebet doesn't exceed player balance, run the game again, resetting game state
        is_dealer = True
        game_state = ''
        main()

# Function to allow player to make a new bet
def new_bet():
    global player_bet
    player_bet = 0
    play_again()

# Main Game Loop
def main():
    global current_player, player_bet, game_state, is_dealer, paused, how_to, valid_rebet, player_name, balance
    # Initialise or reuse current_player and player_bet variables
    start_game()
    # Reset the round and get the initial hands and their values
    card_shoe, player_hand, dealer_hand, player_hand_value, dealer_hand_value = reset_round()
    # Deal the first hand for player and dealer and get the updated hand values
    player_hand_value, dealer_hand_value = first_hand(card_shoe, player_hand, dealer_hand)
    # Initialise the message to be displayed
    message = 'Good Luck ' + player_name + '!'
    # Update the screen with the initial state
    update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message, player_bet)
    # Set the dealer flag to True to ensure their 2nd card is hidden
    is_dealer = True
    # Initialise the flag for tracking if winnings have been saved for the round
    winnings_saved = False
    # Check if either the player or the dealer has a blackjack
    blackjack_result = check_blackjack(player_hand_value, dealer_hand_value)
    # If either the player or the dealer has a blackjack
    if blackjack_result is not None:
        # If the player has a blackjack
        if blackjack_result == 'player':
            # Update the message to congratulate the player
            message = "Congratulations! You got a Blackjack!"
            # Calculate the winnings as 2.5 times the player's bet
            winnings = int(player_bet * 2.5)
            # Save the winnings
            # Change working directory for access/create save_file.txt in game_assets folder
            os.chdir(game_assets)
            save(current_player, winnings)
            current_player = load(player_name)
            balance = get_info(current_player)[1]
            # Set the game state to indicate the round is over
            game_state = 'ROUND_OVER'
            # Update the screen with the final state
            update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message, player_bet)
        # If the dealer has a blackjack
        elif blackjack_result == 'dealer':
            # Update the message to inform the player that the dealer has a blackjack
            message = "Dealer got a Blackjack! Better luck next time."
            # Set the game state to indicate the round is over
            game_state = 'ROUND_OVER'
        # If both the player and the dealer have a blackjack
        else:
            # Update the message to inform the player that it's a push
            message = "Both you and the dealer got a Blackjack! It's a push."
            # The player gets their bet back
            winnings = int(player_bet)
            # Save the winnings
            # Change working directory for access/create save_file.txt in game_assets folder
            os.chdir(game_assets)
            save(current_player, winnings)
            current_player = load(player_name)
            balance = get_info(current_player)[1]
            # Set the game state to indicate the round is over
            game_state = 'ROUND_OVER'
        # Update the screen with the final state
        update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message, player_bet)
    # If neither the player nor the dealer has a blackjack
    else:
        # Set the game state to indicate it's the player's turn
        game_state = 'PLAYER_TURN'

    # Pygame Loop
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
                # If game_state is valid and game isn't paused
                elif game_state == 'PLAYER_TURN' and not paused:
                    # Listen and respond to 'S' being pressed and carry out stand action/change game states
                    if event.key == pygame.K_s:
                        stand_action()
                        game_state = 'DEALER_TURN'
                        is_dealer = False
                    # Listen and respond to 'H' being pressed and carry out hit action/change game states if appropriate
                    elif event.key == pygame.K_h and not paused:
                        player_hand, player_hand_value = hit_action(card_shoe, player_hand, player_hand_value)
                        if player_hand_value > 21:
                            message = "Bust! You lose"
                            game_state = 'ROUND_OVER'
                # Listen and respond to 'R' being pressed and assign valid_rebet boolean value depending on play_again return value
                elif event.key == pygame.K_r and not paused:
                    valid_rebet = play_again()
                    if valid_rebet:
                        play_again()
                    else:
                        message = "Insufficent Balance"
                # Listen and respond to 'N' being pressed and call new_bet() function
                elif event.key == pygame.K_n and not paused:
                    new_bet()
                # Take the dealers turn if game state appropriate
                elif game_state == 'DEALER_TURN' and not paused:
                    dealer_hand, dealer_hand_value = dealer_turn(card_shoe, dealer_hand, dealer_hand_value)
                    game_state = 'ROUND_OVER'
        # Take dealers turn if game state appropriate
        if game_state == 'DEALER_TURN' and not paused:
            dealer_hand, dealer_hand_value = dealer_turn(card_shoe, dealer_hand, dealer_hand_value)
            game_state = 'ROUND_OVER'
        # Handle game outcomes and issue credits accordingly, along with screen updates
        if game_state == 'ROUND_OVER':
            if not winnings_saved:
                winner = check_winner(player_hand_value, dealer_hand_value)
                if winner == 'player':
                    message = "Congratulations! You won!"
                    winnings = int(player_bet * 2)
                    # Change working directory for access/create save_file.txt in game_assets folder
                    os.chdir(game_assets)
                    save(current_player, winnings)
                    current_player = load(player_name)
                    balance = get_info(current_player)[1]
                    update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message, player_bet)
                elif winner == 'dealer':
                    message = "Dealer won! Better luck next time."
                else:
                    message = "It's a tie!"
                    winnings = int(player_bet)
                    # Change working directory for access/create save_file.txt in game_assets folder
                    os.chdir(game_assets)
                    save(current_player, winnings)
                    current_player = load(player_name)
                    balance = get_info(current_player)[1]
                winnings_saved = True
        # Update screen each loop iteration
        update_screen(dealer_hand_value, player_hand_value, dealer_hand, player_hand, message, player_bet)
    
if __name__ == "__main__":
    main()
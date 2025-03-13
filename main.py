import pygame
import sys
import subprocess
import os


# Initialise pygame
pygame.init()


# Initialise Screen Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")


# Initialise Colour Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (28, 21, 105)

# Initialise Font Variable
font = pygame.font.Font(None, 36)

# Initialise Menu Variables
game_options = {"BLACKJACK": "blackjack/blackjack_game.py",
                "HIGHER OR LOWER": "higher_or_lower/hilo_game.py",
                "LUCKY WHEEL": "lucky_wheel/wheel_game.py",
                "SLOT MACHINE": "slot_machine/slot_machine_game.py"
}
exit_button_rect = pygame.Rect(15, 15, 60, 30)
exit_button_color = (RED)

#  Initialise background image variable with try/except due to behaviour of OS module when testing
try:
    background_image = pygame.image.load("game_assets/Background_Menu.png").convert()
except:
    background_image = pygame.image.load("Background_Menu.png").convert()

# Transform Background Image to fit menu screen resolution
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to quit the menu gracefully
def quit_game():
    pygame.quit()
    sys.exit()

# Function to draw the menu
def draw_menu():
    screen.blit(background_image, (0, 0))
    title_font = pygame.font.Font(None, 56)
    title_surface = title_font.render("GAME MENU ", True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_surface, title_rect)
    
    for i, option in enumerate(game_options):
        text_surface = font.render(option, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, 125 + i * 100))
        pygame.draw.rect(screen, GREEN, (text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20), 2)
        screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, exit_button_color, exit_button_rect)
    exit_text_surface = font.render("EXIT", True, WHITE)
    exit_text_rect = exit_text_surface.get_rect(center=(exit_button_rect.centerx, exit_button_rect.centery))
    screen.blit(exit_text_surface, exit_text_rect)

# Function to handle mouse clicks
def handle_click(mouse_pos):
    for i, option in enumerate(game_options):
        text_surface = font.render(option, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, 100 + i * 100))
        button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 40)
        if button_rect.collidepoint(mouse_pos):
            execute_game(game_options[option])

    if exit_button_rect.collidepoint(mouse_pos):
        quit_game()

# Function to execute a game
def execute_game(file_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.normpath(file_name)
        game_path = os.path.join(current_dir, file_name)
        command = [sys.executable, game_path]
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        quit_game()
    except Exception as e:
        print("Error:", e)
        
# Main function for the menu
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_click(mouse_pos)

        draw_menu()
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()

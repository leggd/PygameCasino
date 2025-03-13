A simple casino-style game suite built with Python and Pygame, featuring a main menu and four games:
Blackjack, Higher or Lower, Lucky Wheel, and Slot Machine. Each game includes betting mechanics, player balance tracking, and interactive graphical interfaces.

Overview
Game Menu: Launch any of the four games from a central menu.
Blackjack: A card game where you aim to beat the dealer without exceeding 21.
Higher or Lower: Guess if the next card will be higher or lower to increase your winnings.
Lucky Wheel: Spin a wheel to land on multipliers and win based on your bet.
Slot Machine: Spin reels to match symbols and win prizes.

Requirements
Python 3.x
Pygame (pip install pygame)

Installation
Clone the repository: git clone https://github.com/leggd/PygameCasino.git

Navigate to the project directory: cd casino-game-suite

Install the required dependency: pip install pygame

Usage
Run the main menu: python game_menu.py
Click a game title to launch it, or click "EXIT" to close the menu.
Follow in-game prompts to enter your name and place bets.

File Structure
PygameCasino/
│
├── game_menu.py           
├── game_assets/             
│   ├── gnu.ttf
│   ├── player.py
│   └── card_deck.py
├── blackjack/           
│   ├── blackjack_game.py
│   └── graphics/
│       ├── Blackjack_Background.png
│       └── Pause_Background.png
├── higher_or_lower/         
│   ├── hilo_game.py
│   └── graphics/
│       ├── Hilo_Background.png
│       └── Pause_Background.png
├── lucky_wheel/           
│   ├── wheel_game.py
│   └── graphics/
│       ├── wheel.png
│       ├── lucky_wheel_background.png
│       ├── lw_pause_background.png
│       └── lw_background.png
├── slot_machine/           
│   ├── slot_machine_game.py
│   └── graphics/
│       ├── grid_white_bg.png
│       ├── background.png
│       ├── menu_background.png
│       └── symbols/
│           ├── elephant.png
│           ├── giraffe.png
│           ├── lion.png
│           ├── zebra.png
│           ├── flamingo.png
│           ├── boar.png
│           ├── paws.png
│           ├── tiger.png
│           ├── tree.png
│           └── turtle.png
└── README.md           

Notes
Ensure all game scripts and assets are in the correct directories as shown above.
Player balances are saved in game_assets/save_file.txt (created automatically).
Games rely on player.py and card_deck.py for shared functionality

Contributing
Feel free to fork this repository and submit pull requests with improvements or bug fixes. Issues can be reported via GitHub Issues.

License
This project is unlicensed and provided as-is for educational or personal use.

Credits

Daniel Legg, Ethan Harper, James Devlin, Charles Gibson-May, Samuel Nnamdi
(Created as a team for Foundation Year Assignement for the module "Development Project")
